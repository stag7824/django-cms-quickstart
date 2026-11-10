import io
import os
import random

from cms.api import add_plugin, create_page, create_page_content
from cms.models import Page, PageContent
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from djangocms_alias.models import Alias, AliasContent, Category
from djangocms_versioning.models import Version
from filer.models import Folder, Image as FilerImage
from PIL import Image, ImageDraw

from backend import seed_content as seed
from backend.models import AppliedContentUpdate, Material, ResourceMeta

PALETTES = {
    "ember": ("#26272c", ["#f05a28", "#ff8a4c", "#3a3d45", "#f4d9c6"]),
    "cobalt": ("#171d30", ["#3760f0", "#7d9bff", "#2a3350", "#dfe6ff"]),
    "teal": ("#12262a", ["#129a8f", "#5fd3c6", "#22444a", "#d8f5f1"]),
    "graphite": ("#1d1f24", ["#7f8791", "#c6cbd2", "#3c4048", "#f05a28"]),
    "violet": ("#201a30", ["#7a54e0", "#b398ff", "#3b3158", "#eee6ff"]),
}


def height_at(shape, x, y, size, rng):
    if shape == "skyline":
        return rng.randint(1, 3 + (x * 3) // size + (y * 2) // size)
    if shape == "wave":
        return 1 + (x + y) % 4 + (x % 2)
    if shape == "gear":
        center = size / 2 - 0.5
        distance = ((x - center) ** 2 + (y - center) ** 2) ** 0.5
        if distance < size * 0.16 or distance > size * 0.5:
            return 0
        return 3 if (x + y) % 3 else 1
    if shape == "bracket":
        return 6 if x < size / 3 else (2 if y < size * 0.75 else 0)
    if shape in ("printer", "printer-large"):
        edge = size * (0.15 if shape == "printer-large" else 0.25)
        if not (edge <= x < size - edge and edge <= y < size - edge):
            return 0
        return 5 if shape == "printer" else 7
    return 1


def draw_voxels(palette, shape, name):
    background, colors = PALETTES[palette]
    width, height = 1600, 1100
    rng = random.Random(name)
    image = Image.new("RGB", (width, height), background)
    draw = ImageDraw.Draw(image)
    size = 12
    half_w, half_h, step = 52, 30, 56

    def shade(hex_color, factor):
        value = hex_color.lstrip("#")
        return tuple(min(255, int(int(value[i:i + 2], 16) * factor)) for i in (0, 2, 4))

    for x in range(size):
        for y in range(size):
            for z in range(height_at(shape, x, y, size, rng)):
                cx = width / 2 + (x - y) * half_w
                cy = height / 2 + 190 + (x + y - size) * half_h - z * step
                color = colors[0] if rng.random() < 0.72 else rng.choice(colors)
                if shape.startswith("printer") and z >= 2:
                    color = colors[2] if z < 5 else colors[0]
                top = [(cx, cy - half_h), (cx + half_w, cy), (cx, cy + half_h), (cx - half_w, cy)]
                left = [(cx - half_w, cy), (cx, cy + half_h), (cx, cy + half_h + step), (cx - half_w, cy + step)]
                right = [(cx + half_w, cy), (cx, cy + half_h), (cx, cy + half_h + step), (cx + half_w, cy + step)]
                draw.polygon(left, fill=shade(color, 0.62))
                draw.polygon(right, fill=shade(color, 0.42))
                draw.polygon(top, fill=shade(color, 1.0))
    return image


class Command(BaseCommand):
    help = "Create the Voxelry starter site: page tree, content, footer, materials and images."

    def add_arguments(self, parser):
        parser.add_argument(
            "--username",
            default="voxelry-seed",
            help="Author recorded on the created page versions.",
        )
        parser.add_argument(
            "--skip-existing",
            action="store_true",
            help="Exit quietly instead of failing when the site already exists, for use on every deploy.",
        )

    def handle(self, *args, **options):
        if Page.objects.filter(reverse_id="home").exists():
            message = "The Voxelry starter site already exists, so nothing was changed."
            if options["skip_existing"]:
                self.stdout.write(message)
                return
            raise CommandError(message)

        user, _created = get_user_model().objects.get_or_create(username=options["username"])
        with transaction.atomic():
            self.user = user
            self.images = {}
            self.pages = {}
            self.configure_site()
            self.create_images()
            self.create_pages()
            self.create_materials()
            self.create_footer()
            # The seed already contains every later content update, so none of them should run here.
            from backend.management.commands.update_voxelry import UPDATES
            for name, _method in UPDATES:
                AppliedContentUpdate.objects.get_or_create(name=name)
        published = PageContent.objects.count()
        self.stdout.write(self.style.SUCCESS(
            f"Created {len(self.pages)} pages ({published} published language versions), "
            f"{Material.objects.count()} materials and the footer."
        ))

    def configure_site(self):
        domain = os.environ.get("DOMAIN") or "localhost:8000"
        Site.objects.filter(pk=settings.SITE_ID).update(domain=domain, name=seed.SITE_NAME)

    def create_images(self):
        folder, _created = Folder.objects.get_or_create(name="Voxelry starter artwork", parent=None)
        for name, (palette, shape, alt) in seed.ARTWORK.items():
            buffer = io.BytesIO()
            draw_voxels(palette, shape, name).save(buffer, format="JPEG", quality=86)
            filename = f"{name}.jpg"
            self.images[name] = FilerImage.objects.create(
                owner=self.user,
                folder=folder,
                name=name,
                original_filename=filename,
                default_alt_text=alt,
                file=ContentFile(buffer.getvalue(), name=filename),
            )

    def create_pages(self):
        for row in seed.PAGES:
            self.create_seed_page(row)
        for key in seed.GERMAN_PAGES:
            self.create_german_content(key)

        # Links need every page to exist, so content is added in a second pass.
        for (key, language), build in seed.CONTENT.items():
            content = self.pages[key].get_admin_content(language)
            self.fill(content, build())

        for key, page in self.pages.items():
            self.publish(page.get_admin_content("en"))
        for key, (*_details, publish) in seed.GERMAN_PAGES.items():
            if publish:
                self.publish(self.pages[key].get_admin_content("de"))

    def create_seed_page(self, row):
        key, parent, template, slug, title, description, options = row
        page = create_page(
            title=title,
            template=template,
            language="en",
            slug=slug,
            parent=self.pages.get(parent),
            reverse_id=key,
            meta_description=description,
            overwrite_url=options.get("url"),
            in_navigation=options.get("nav", True),
            created_by=self.user,
        )
        self.pages[key] = page
        # create_page() has no page_title argument, unlike create_page_content().
        PageContent.admin_manager.filter(page=page, language="en").update(
            page_title=options.get("page_title", title)
        )
        if key == "home":
            page.set_as_homepage()
        if options.get("resource"):
            resource_type, industry, published_on, image = options["resource"]
            ResourceMeta.objects.create(
                extended_object=page,
                resource_type=resource_type,
                industry=industry,
                published_on=published_on,
                listing_image=self.images[image],
            )
        return page

    def create_german_content(self, key):
        title, slug, description, options, _publish = seed.GERMAN_PAGES[key]
        english = self.pages[key].get_admin_content("en")
        return create_page_content(
            language="de",
            title=title,
            page=self.pages[key],
            slug=slug,
            meta_description=description,
            page_title=options.get("page_title", title),
            overwrite_url=options.get("url"),
            created_by=self.user,
            template=english.template,
            in_navigation=english.in_navigation,
        )

    def fill(self, content, placeholders):
        for slot, blocks in placeholders.items():
            placeholder = content.get_placeholders().filter(slot=slot).first()
            if placeholder is None:
                content.page.rescan_placeholders(content.language)
                placeholder = content.get_placeholders().get(slot=slot)
            self.add_blocks(placeholder, content.language, blocks)

    def add_blocks(self, placeholder, language, blocks, target=None):
        for plugin_type, fields, children in blocks:
            plugin = add_plugin(
                placeholder, plugin_type, language, target=target,
                **{name: self.resolve(value) for name, value in fields.items()},
            )
            self.add_blocks(placeholder, language, children, target=plugin)

    def resolve(self, value):
        if isinstance(value, seed.page):
            return {"internal_link": f"cms.page:{self.pages[value.key].pk}"}
        if isinstance(value, seed.art):
            return self.images[value.name]
        return value

    def publish(self, content):
        Version.objects.get_for_content(content).publish(self.user)

    def create_materials(self):
        for position, row in enumerate(seed.MATERIALS):
            name, name_de, description, description_de, technology, category, tensile, elongation, price = row
            material = Material(
                technology=technology,
                category=category,
                tensile_strength_mpa=tensile,
                elongation_percent=elongation,
                price_eur=price,
                position=position,
            )
            material.set_current_language("en")
            material.name, material.description = name, description
            material.save()
            material.set_current_language("de")
            material.name, material.description = name_de, description_de
            material.save()

    def create_footer(self):
        category = Category.objects.create(name="Global")
        alias = Alias.objects.create(
            category=category, static_code="footer", creation_method=Alias.CREATION_BY_TEMPLATE
        )
        for language, blocks in seed.FOOTER.items():
            content = AliasContent._base_manager.create(alias=alias, name="footer", language=language)
            version = Version.objects.create(content=content, created_by=self.user)
            self.add_blocks(content.placeholder, language, blocks)
            version.publish(self.user)
