import json

from cms.models import PageContent
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.translation import get_language
from djangocms_link.helpers import get_link

from backend.models import ResourceMeta

register = template.Library()


@register.filter
def link_url(value):
    return get_link(value) or ""


@register.simple_tag(takes_context=True)
def page_alternates(context):
    """Every published language of the current page, for hreflang tags and the language switcher."""
    request = context["request"]
    page = getattr(request, "current_page", None)
    if not page:
        return []
    names = dict(settings.LANGUAGES)
    published = PageContent.objects.filter(page=page).values_list("language", flat=True)
    return [
        {
            "code": code,
            "name": names[code],
            "active": code == get_language(),
            "url": page.get_absolute_url(code),
            "absolute_url": request.build_absolute_uri(page.get_absolute_url(code)),
        }
        for code in names
        if code in published
    ]


@register.simple_tag(takes_context=True)
def resource_meta(context):
    page = getattr(context["request"], "current_page", None)
    return ResourceMeta.objects.filter(extended_object=page).select_related("listing_image").first() if page else None


@register.simple_tag(takes_context=True)
def article_structured_data(context, meta, headline, description):
    data = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": headline,
        "description": description,
        "inLanguage": get_language(),
        "publisher": {"@type": "Organization", "name": "Voxelry"},
    }
    if meta:
        data["datePublished"] = meta.published_on.isoformat()
        if meta.listing_image:
            data["image"] = context["request"].build_absolute_uri(meta.listing_image.url)
    return mark_safe(json.dumps(data).replace("<", "\\u003c"))
