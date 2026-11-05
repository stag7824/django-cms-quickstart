import json

from cms.models import PageContent
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.safestring import mark_safe
from django.utils.translation import get_language

from .models import (
    AnchorNav,
    AnchorNavItem,
    Card,
    CardGrid,
    ComparisonRow,
    ComparisonTable,
    CTABanner,
    FAQ,
    FAQItem,
    Hero,
    LinkItem,
    LinkList,
    Material,
    MaterialCatalogue,
    ResourceListing,
    ResourceMeta,
    Section,
    ShowcaseTab,
    ShowcaseTabs,
    SpecRow,
    SpecTable,
    Testimonial,
    TestimonialGrid,
    TextMedia,
)


class VoxelryPlugin(CMSPluginBase):
    module = "Voxelry"

    def get_render_template(self, context, instance, placeholder):
        return self.render_template or f"backend/plugins/{self.model.__name__.lower()}.html"


@plugin_pool.register_plugin
class SpecTablePlugin(CMSPluginBase):
    model = SpecTable
    name = "Spec table"
    module = "Voxelry"
    render_template = "backend/plugins/spec_table.html"
    allow_children = True
    child_classes = ["SpecRowPlugin"]


@plugin_pool.register_plugin
class SpecRowPlugin(CMSPluginBase):
    model = SpecRow
    name = "Spec row"
    module = "Voxelry"
    render_template = "backend/plugins/spec_row.html"
    require_parent = True
    parent_classes = ["SpecTablePlugin"]


@plugin_pool.register_plugin
class HeroPlugin(VoxelryPlugin):
    model = Hero
    name = "Hero"


@plugin_pool.register_plugin
class SectionPlugin(VoxelryPlugin):
    model = Section
    name = "Section"
    allow_children = True
    child_classes = [
        "CardGridPlugin",
        "TextMediaPlugin",
        "ShowcaseTabsPlugin",
        "TestimonialGridPlugin",
        "ComparisonTablePlugin",
        "SpecTablePlugin",
        "FAQPlugin",
        "ResourceListingPlugin",
        "MaterialCataloguePlugin",
        "TextPlugin",
        "Alias",
    ]


@plugin_pool.register_plugin
class CardGridPlugin(VoxelryPlugin):
    model = CardGrid
    name = "Card grid"
    allow_children = True
    child_classes = ["VoxelCardPlugin"]


@plugin_pool.register_plugin
class VoxelCardPlugin(VoxelryPlugin):
    model = Card
    name = "Card"
    require_parent = True
    parent_classes = ["CardGridPlugin"]


@plugin_pool.register_plugin
class AnchorNavPlugin(VoxelryPlugin):
    model = AnchorNav
    name = "Jump links"
    allow_children = True
    child_classes = ["AnchorNavItemPlugin"]


@plugin_pool.register_plugin
class AnchorNavItemPlugin(VoxelryPlugin):
    model = AnchorNavItem
    name = "Jump link"
    require_parent = True
    parent_classes = ["AnchorNavPlugin"]


@plugin_pool.register_plugin
class TextMediaPlugin(VoxelryPlugin):
    model = TextMedia
    name = "Text and image"


@plugin_pool.register_plugin
class ShowcaseTabsPlugin(VoxelryPlugin):
    model = ShowcaseTabs
    name = "Showcase tabs"
    allow_children = True
    child_classes = ["ShowcaseTabPlugin"]


@plugin_pool.register_plugin
class ShowcaseTabPlugin(VoxelryPlugin):
    model = ShowcaseTab
    name = "Showcase tab"
    require_parent = True
    parent_classes = ["ShowcaseTabsPlugin"]


@plugin_pool.register_plugin
class TestimonialGridPlugin(VoxelryPlugin):
    model = TestimonialGrid
    name = "Testimonials"
    allow_children = True
    child_classes = ["TestimonialPlugin"]


@plugin_pool.register_plugin
class TestimonialPlugin(VoxelryPlugin):
    model = Testimonial
    name = "Testimonial"
    require_parent = True
    parent_classes = ["TestimonialGridPlugin"]


@plugin_pool.register_plugin
class ComparisonTablePlugin(VoxelryPlugin):
    model = ComparisonTable
    name = "Comparison table"
    allow_children = True
    child_classes = ["ComparisonRowPlugin"]


@plugin_pool.register_plugin
class ComparisonRowPlugin(VoxelryPlugin):
    model = ComparisonRow
    name = "Comparison row"
    require_parent = True
    parent_classes = ["ComparisonTablePlugin"]


@plugin_pool.register_plugin
class FAQPlugin(VoxelryPlugin):
    model = FAQ
    name = "FAQ"
    allow_children = True
    child_classes = ["FAQItemPlugin"]

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        items = instance.child_plugin_instances or []
        data = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": item.question,
                    "acceptedAnswer": {"@type": "Answer", "text": item.answer},
                }
                for item in items
            ],
        }
        context["structured_data"] = mark_safe(json.dumps(data).replace("<", "\\u003c"))
        return context


@plugin_pool.register_plugin
class FAQItemPlugin(VoxelryPlugin):
    model = FAQItem
    name = "FAQ item"
    require_parent = True
    parent_classes = ["FAQPlugin"]


@plugin_pool.register_plugin
class CTABannerPlugin(VoxelryPlugin):
    model = CTABanner
    name = "Call to action banner"


@plugin_pool.register_plugin
class LinkListPlugin(VoxelryPlugin):
    model = LinkList
    name = "Link list"
    allow_children = True
    child_classes = ["LinkItemPlugin"]


@plugin_pool.register_plugin
class LinkItemPlugin(VoxelryPlugin):
    model = LinkItem
    name = "Link"
    require_parent = True
    parent_classes = ["LinkListPlugin"]


@plugin_pool.register_plugin
class ResourceListingPlugin(VoxelryPlugin):
    model = ResourceListing
    name = "Resource listing"
    cache = False  # the result depends on the query string

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        params = context["request"].GET
        language = get_language()

        selected_type = instance.resource_type
        selected_industry = ""
        resources = ResourceMeta.objects.select_related("extended_object", "listing_image")
        if instance.show_filters:
            selected_type = params.get("type", selected_type)
            selected_industry = params.get("industry", "")
        if selected_type:
            resources = resources.filter(resource_type=selected_type)
        if selected_industry:
            resources = resources.filter(industry=selected_industry)
        resources = resources.order_by("-published_on")

        # Only list pages with a published version in the visitor's language.
        contents = {
            content.page_id: content
            for content in PageContent.objects.filter(
                language=language, page__in=resources.values("extended_object")
            )
        }
        items = []
        for resource in resources:
            content = contents.get(resource.extended_object_id)
            if content:
                items.append(
                    {
                        "meta": resource,
                        "title": content.title,
                        "teaser": content.meta_description,
                        "url": resource.extended_object.get_absolute_url(language),
                    }
                )
        context.update(
            {
                "items": items[: instance.limit],
                "types": ResourceMeta.TYPES,
                "industries": [choice for choice in ResourceMeta.INDUSTRIES if choice[0]],
                "selected_type": selected_type,
                "selected_industry": selected_industry,
            }
        )
        return context


@plugin_pool.register_plugin
class MaterialCataloguePlugin(VoxelryPlugin):
    model = MaterialCatalogue
    name = "Material catalogue"
    cache = False  # the result depends on the query string

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        params = context["request"].GET

        selected_technology = instance.technology
        selected_category = ""
        if instance.show_filters:
            selected_technology = params.get("print-technology", selected_technology)
            selected_category = params.get("categories", "")

        materials = Material.objects.filter(is_published=True).select_related("image")
        if selected_technology:
            materials = materials.filter(technology=selected_technology)
        if selected_category:
            materials = materials.filter(category=selected_category)
        context.update(
            {
                "materials": materials,
                "technologies": Material.TECHNOLOGIES,
                "categories": Material.CATEGORIES,
                "selected_technology": selected_technology,
                "selected_category": selected_category,
            }
        )
        return context
