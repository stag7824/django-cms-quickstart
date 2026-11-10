from cms.extensions import PageExtension
from cms.extensions.extension_pool import extension_pool
from cms.models import CMSPlugin
from django.db import models
from django.utils.translation import gettext_lazy as _
from djangocms_link.fields import LinkField
from djangocms_text.fields import HTMLField
from filer.fields.image import FilerImageField
from parler.models import TranslatableModel, TranslatedFields


def image_field():
    return FilerImageField(null=True, blank=True, on_delete=models.SET_NULL, related_name="+")


class SpecTable(CMSPlugin):
    title = models.CharField(max_length=100, default="Tech specs")

    def __str__(self):
        return self.title


class SpecRow(CMSPlugin):
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.label}: {self.value}"


class Hero(CMSPlugin):
    LAYOUTS = [("split", "Text beside image"), ("overlay", "Text over full-width image")]

    layout = models.CharField(max_length=10, choices=LAYOUTS, default="split")
    eyebrow = models.CharField(max_length=100, blank=True)
    heading = models.CharField(max_length=120, help_text="The page's only H1.")
    subheading = models.CharField(max_length=240, blank=True)
    price_note = models.CharField(max_length=100, blank=True, help_text='For example "From €2,950".')
    image = image_field()
    image_alt = models.CharField(max_length=200, blank=True, help_text="Describe the image for this language.")
    primary_label = models.CharField(max_length=60, blank=True)
    primary_link = LinkField(blank=True)
    secondary_label = models.CharField(max_length=60, blank=True)
    secondary_link = LinkField(blank=True)

    def __str__(self):
        return self.heading


class Section(CMSPlugin):
    TONES = [("white", "White"), ("light", "Light grey"), ("dark", "Dark")]

    anchor = models.SlugField(max_length=50, blank=True, help_text="Target for jump links, without the #.")
    tone = models.CharField(max_length=10, choices=TONES, default="white")
    eyebrow = models.CharField(max_length=100, blank=True)
    heading = models.CharField(max_length=160, blank=True)
    intro = models.TextField(blank=True)
    cta_label = models.CharField(max_length=60, blank=True)
    cta_link = LinkField(blank=True)

    def __str__(self):
        return self.heading or self.anchor or "Section"


class CardGrid(CMSPlugin):
    columns = models.PositiveSmallIntegerField(choices=[(2, "2"), (3, "3"), (4, "4")], default=3)

    def __str__(self):
        return f"{self.columns} columns"


class Card(CMSPlugin):
    badge = models.CharField(max_length=40, blank=True, help_text='For example "New" or "SLA".')
    title = models.CharField(max_length=120)
    text = models.TextField(blank=True)
    image = image_field()
    image_alt = models.CharField(max_length=200, blank=True)
    link = LinkField(blank=True)
    link_label = models.CharField(max_length=60, blank=True)

    def __str__(self):
        return self.title


class AnchorNav(CMSPlugin):
    def __str__(self):
        return "Jump links"


class AnchorNavItem(CMSPlugin):
    title = models.CharField(max_length=60)
    text = models.CharField(max_length=120, blank=True)
    anchor = models.SlugField(max_length=50, help_text="Matches the anchor of a section on this page.")

    def __str__(self):
        return self.title


class TextMedia(CMSPlugin):
    eyebrow = models.CharField(max_length=100, blank=True)
    heading = models.CharField(max_length=160)
    body = HTMLField(blank=True)
    image = image_field()
    image_alt = models.CharField(max_length=200, blank=True)
    image_first = models.BooleanField(default=False)
    cta_label = models.CharField(max_length=60, blank=True)
    cta_link = LinkField(blank=True)

    def __str__(self):
        return self.heading


class ShowcaseTabs(CMSPlugin):
    def __str__(self):
        return "Tabs"


class ShowcaseTab(CMSPlugin):
    label = models.CharField(max_length=50)
    heading = models.CharField(max_length=120)
    text = models.TextField(blank=True)
    image = image_field()
    image_alt = models.CharField(max_length=200, blank=True)
    link = LinkField(blank=True)
    link_label = models.CharField(max_length=60, blank=True)

    def __str__(self):
        return self.label


class TestimonialGrid(CMSPlugin):
    def __str__(self):
        return "Testimonials"


class Testimonial(CMSPlugin):
    company = models.CharField(max_length=80)
    tag = models.CharField(max_length=80, blank=True)
    quote = models.TextField()
    person = models.CharField(max_length=80)
    role = models.CharField(max_length=120, blank=True)
    link = LinkField(blank=True)
    link_label = models.CharField(max_length=60, blank=True)

    def __str__(self):
        return self.company


class ComparisonTable(CMSPlugin):
    column_one = models.CharField(max_length=60)
    column_two = models.CharField(max_length=60)
    column_three = models.CharField(max_length=60, blank=True)
    footnote = models.CharField(max_length=240, blank=True)

    def __str__(self):
        return f"{self.column_one} vs {self.column_two}"


class ComparisonRow(CMSPlugin):
    label = models.CharField(max_length=100)
    value_one = models.CharField(max_length=100)
    value_two = models.CharField(max_length=100)
    value_three = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.label


class FAQ(CMSPlugin):
    def __str__(self):
        return "FAQ"


class FAQItem(CMSPlugin):
    question = models.CharField(max_length=200)
    answer = models.TextField(help_text="Plain text. It is also published as FAQ structured data.")

    def __str__(self):
        return self.question


class CTABanner(CMSPlugin):
    heading = models.CharField(max_length=160)
    text = models.CharField(max_length=240, blank=True)
    primary_label = models.CharField(max_length=60, blank=True)
    primary_link = LinkField(blank=True)
    secondary_label = models.CharField(max_length=60, blank=True)
    secondary_link = LinkField(blank=True)

    def __str__(self):
        return self.heading


class LinkList(CMSPlugin):
    title = models.CharField(max_length=60)

    def __str__(self):
        return self.title


class LinkItem(CMSPlugin):
    label = models.CharField(max_length=80)
    link = LinkField()

    def __str__(self):
        return self.label


class ResourceMeta(PageExtension):
    """What the resource hub needs to know about an article page."""

    TYPES = [
        ("news", _("News")),
        ("case_study", _("Case study")),
        ("guide", _("Guide")),
        ("white_paper", _("White paper")),
    ]
    INDUSTRIES = [
        ("", _("All industries")),
        ("automotive", _("Automotive")),
        ("manufacturing", _("Manufacturing")),
        ("medical", _("Medical")),
    ]

    resource_type = models.CharField(max_length=20, choices=TYPES, default="news")
    industry = models.CharField(max_length=20, choices=INDUSTRIES, blank=True)
    published_on = models.DateField()
    listing_image = image_field()

    def __str__(self):
        return f"{self.get_resource_type_display()} ({self.published_on})"


extension_pool.register(ResourceMeta)


class ResourceListing(CMSPlugin):
    resource_type = models.CharField(
        max_length=20, choices=ResourceMeta.TYPES, blank=True, help_text="Leave empty to include every type."
    )
    limit = models.PositiveSmallIntegerField(default=12)
    show_filters = models.BooleanField(default=True)

    def __str__(self):
        return self.get_resource_type_display() or "All resources"


class Material(TranslatableModel):
    TECHNOLOGIES = [("sla", "SLA"), ("sls", "SLS")]
    CATEGORIES = [
        ("general-purpose", _("General purpose")),
        ("impact-resistant", _("Impact resistant")),
        ("high-stiffness", _("High stiffness")),
        ("temperature-resistant", _("Temperature resistant")),
        ("elastomeric", _("Elastomeric")),
        ("medical", _("Medical")),
    ]

    translations = TranslatedFields(
        name=models.CharField(max_length=80),
        description=models.TextField(blank=True),
    )
    technology = models.CharField(max_length=3, choices=TECHNOLOGIES)
    category = models.CharField(max_length=30, choices=CATEGORIES)
    tensile_strength_mpa = models.PositiveSmallIntegerField("Tensile strength (MPa)")
    elongation_percent = models.PositiveSmallIntegerField("Elongation at break (%)")
    price_eur = models.DecimalField("Price (EUR)", max_digits=7, decimal_places=2)
    image = image_field()
    is_published = models.BooleanField(default=True)
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["position", "pk"]

    def __str__(self):
        return self.safe_translation_getter("name", any_language=True) or f"Material {self.pk}"


class MaterialCatalogue(CMSPlugin):
    technology = models.CharField(
        max_length=3, choices=Material.TECHNOLOGIES, blank=True, help_text="Leave empty to include both."
    )
    show_filters = models.BooleanField(default=True)

    def __str__(self):
        return self.get_technology_display() or "All materials"


class AppliedContentUpdate(models.Model):
    """A one-off content change that `update_voxelry` has already made on this site."""

    name = models.CharField(max_length=100, unique=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
