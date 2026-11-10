"""
Bring an existing Voxelry site up to date with changes made to the starter content.

`seed_voxelry` only builds a fresh site, so content added to the seed later never
reaches a site that is already live. Each entry in UPDATES makes one such change on
a live site, through the normal versioning workflow (a new version is published and
the old one stays in the page history). Each update runs once and is recorded in
AppliedContentUpdate. A fresh seed records them all as applied, because the seed
already contains them.

The site domain is synced from the DOMAIN environment variable on every run.
"""
import os
import re

from cms.models import Page, PageContent
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.db import transaction
from djangocms_versioning.constants import DRAFT, PUBLISHED
from djangocms_versioning.models import Version
from filer.models import Image as FilerImage

from backend import seed_content as seed
from backend.management.commands.seed_voxelry import Command as SeedCommand
from backend.models import AppliedContentUpdate, Testimonial

TEST_PAGE_TITLE = re.compile(r"^\s*test\b", re.IGNORECASE)


class SkipUpdate(Exception):
    """The update cannot run safely right now; it will be tried again on the next run."""


class Command(SeedCommand):
    help = "Apply content updates to an existing Voxelry site and sync the site domain."

    def add_arguments(self, parser):
        parser.add_argument("--username", default="voxelry-seed", help="Author recorded on new page versions.")

    def handle(self, *args, **options):
        self.sync_site()
        if not Page.objects.filter(reverse_id="home").exists():
            self.stdout.write("No Voxelry site yet, so there is nothing to update.")
            return

        self.user, _created = get_user_model().objects.get_or_create(username=options["username"])
        self.images = {image.name: image for image in FilerImage.objects.filter(folder__name="Voxelry starter artwork")}

        done = set(AppliedContentUpdate.objects.values_list("name", flat=True))
        for name, method in UPDATES:
            if name in done:
                continue
            # Reloaded each time, because a skipped update rolls back any page it created.
            self.pages = {page.reverse_id: page for page in Page.objects.exclude(reverse_id=None)}
            try:
                with transaction.atomic():
                    getattr(self, method)()
                    AppliedContentUpdate.objects.create(name=name)
            except SkipUpdate as reason:
                self.stdout.write(self.style.WARNING(f"Skipped {name}: {reason}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"Applied {name}"))

    def sync_site(self):
        domain = os.environ.get("DOMAIN")
        if domain:
            Site.objects.filter(pk=settings.SITE_ID).update(domain=domain, name=seed.SITE_NAME)

    # Helpers

    def versions(self, page, language):
        contents = PageContent.admin_manager.filter(page=page, language=language)
        return Version.objects.filter_by_content_grouping_values(contents.first()) if contents.exists() else Version.objects.none()

    def revise(self, key, language, change):
        """Publish a new version of a page, made by applying `change` to a copy of the live version."""
        versions = self.versions(self.pages[key], language)
        if versions.filter(state=DRAFT).exists():
            raise SkipUpdate(f'"{key}" ({language}) has an unpublished draft. Publish or discard it first.')
        published = versions.filter(state=PUBLISHED).first()
        if published is None:
            raise SkipUpdate(f'"{key}" ({language}) has no published version.')
        draft = published.copy(self.user)
        change(draft.content)
        draft.publish(self.user)

    def rebuild(self, key, language, *slots):
        """Replace the given placeholders of a page with the current seed content."""
        blocks = seed.CONTENT[(key, language)]()

        def change(content):
            for slot in slots:
                placeholder = content.get_placeholders().get(slot=slot)
                placeholder.clear(language)
                self.add_blocks(placeholder, language, blocks.get(slot, []))

        self.revise(key, language, change)

    # Updates, in the order they run

    def unpublish_test_pages(self):
        for content in PageContent.admin_manager.filter(title__icontains="test").select_related("page"):
            if not TEST_PAGE_TITLE.match(content.title):
                continue
            for version in self.versions(content.page, content.language).filter(state=PUBLISHED):
                version.unpublish(self.user)
                self.stdout.write(f'  Unpublished "{content.title}" ({content.language})')

    def add_harbor_story(self):
        if "harbor" not in self.pages:
            row = next(row for row in seed.PAGES if row[0] == "harbor")
            self.create_seed_page(row)
            content = self.pages["harbor"].get_admin_content("en")
            self.fill(content, seed.CONTENT[("harbor", "en")]())
            self.publish(content)

        def link_testimonial(content):
            for placeholder in content.get_placeholders():
                for quote in Testimonial.objects.filter(placeholder=placeholder, company="Harbor Robotics"):
                    if not quote.link:
                        quote.link = self.resolve(seed.page("harbor"))
                        quote.link_label = "Read the story"
                        quote.save()

        self.revise("home", "en", link_testimonial)

    def expand_sla_vs_sls(self):
        self.rebuild("sla-vs-sls", "en", "Body")

    def add_german_contact_and_support(self):
        for key in ("support", "contact"):
            if not PageContent.admin_manager.filter(page=self.pages[key], language="de").exists():
                content = self.create_german_content(key)
                self.fill(content, seed.CONTENT[(key, "de")]())
                self.publish(content)

    def complete_german_home(self):
        if "harbor" not in self.pages:
            raise SkipUpdate("the Harbor Robotics story it links to does not exist yet.")
        self.rebuild("home", "de", "Sections", "Regional")


UPDATES = [
    ("2026-11-unpublish-test-pages", "unpublish_test_pages"),
    ("2026-11-harbor-story", "add_harbor_story"),
    ("2026-11-expand-sla-vs-sls", "expand_sla_vs_sls"),
    ("2026-11-german-contact-support", "add_german_contact_and_support"),
    ("2026-11-german-home", "complete_german_home"),
]
