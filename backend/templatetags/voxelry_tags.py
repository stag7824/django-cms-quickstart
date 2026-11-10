import json
import re
from decimal import Decimal

from cms.models import PageContent
from django import template
from django.conf import settings
from django.templatetags.static import static
from django.utils.safestring import mark_safe
from django.utils.translation import get_language
from djangocms_link.helpers import get_link
from easy_thumbnails.files import get_thumbnailer

from backend.models import Hero, ResourceMeta

BRAND = "Voxelry"
SHARE_SIZE = (1200, 630)

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


def json_ld(data):
    """Serialise structured data so it is safe inside a <script> element."""
    return mark_safe(json.dumps(data, ensure_ascii=False).replace("<", "\\u003c"))


def organization(request):
    return {
        "@type": "Organization",
        "name": BRAND,
        "url": request.build_absolute_uri("/"),
        "logo": request.build_absolute_uri(static("voxelry/share.jpg")),
    }


def current_content(request):
    page = getattr(request, "current_page", None)
    if not page:
        return None
    return PageContent.objects.filter(page=page, language=get_language()).first()


def hero_of(content):
    if content is None:
        return None
    return Hero.objects.filter(placeholder__in=content.get_placeholders()).select_related("image").first()


def share_crop(request, image):
    thumb = get_thumbnailer(image).get_thumbnail({"size": SHARE_SIZE, "crop": True})
    return request.build_absolute_uri(thumb.url)


@register.simple_tag(takes_context=True)
def share_image(context):
    """Absolute URL of a 1200 x 630 image for social sharing previews."""
    request = context["request"]
    meta = resource_meta(context)
    image = meta.listing_image if meta and meta.listing_image else None
    if image is None:
        hero = hero_of(current_content(request))
        image = hero.image if hero and hero.image else None
    if image is not None:
        try:
            return share_crop(request, image)
        except Exception:  # a missing or unreadable file should not break the page
            pass
    return request.build_absolute_uri(static("voxelry/share.jpg"))


@register.simple_tag(takes_context=True)
def article_structured_data(context, meta, headline, description):
    request = context["request"]
    data = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": headline,
        "description": description,
        "inLanguage": get_language(),
        "mainEntityOfPage": request.build_absolute_uri(request.path),
        "author": organization(request),
        "publisher": organization(request),
        "image": share_image(context),
    }
    if meta:
        data["datePublished"] = meta.published_on.isoformat()
    return json_ld(data)


@register.simple_tag(takes_context=True)
def product_structured_data(context):
    """Product markup built from the page's hero: name, description, image and starting price."""
    request = context["request"]
    content = current_content(request)
    if content is None:
        return ""
    hero = hero_of(content)
    data = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": hero.heading if hero else content.title,
        "description": content.meta_description,
        "brand": {"@type": "Brand", "name": BRAND},
        "image": share_image(context),
        "url": request.build_absolute_uri(request.path),
    }
    price = re.search(r"\d[\d,.]*", hero.price_note) if hero and hero.price_note else None
    if price:
        data["offers"] = {
            "@type": "Offer",
            # Drop thousands separators in either style: "€2,950" and "2.950 €" are both 2950.
            "price": str(Decimal(re.sub(r"[,.](?=\d{3}\b)", "", price.group()).replace(",", "."))),
            "priceCurrency": "EUR",
            "url": request.build_absolute_uri(request.path),
            "seller": organization(request),
        }
    return json_ld(data)


@register.simple_tag(takes_context=True)
def site_structured_data(context):
    """Organization and WebSite markup for the home page."""
    request = context["request"]
    home = request.build_absolute_uri(request.path)
    return json_ld({
        "@context": "https://schema.org",
        "@graph": [
            {**organization(request), "@id": request.build_absolute_uri("/#organization")},
            {
                "@type": "WebSite",
                "name": BRAND,
                "url": home,
                "inLanguage": get_language(),
                "publisher": {"@id": request.build_absolute_uri("/#organization")},
            },
        ],
    })


@register.simple_tag(takes_context=True)
def breadcrumb_structured_data(context):
    """BreadcrumbList for every page below the home page, in the visitor's language."""
    request = context["request"]
    page = getattr(request, "current_page", None)
    if not page or page.is_home:
        return ""
    language = get_language()
    trail = [*page.get_ancestor_pages(), page]
    titles = dict(
        PageContent.objects.filter(page__in=trail, language=language).values_list("page_id", "title")
    )
    items = [
        {"@type": "ListItem", "name": titles[item.pk], "item": request.build_absolute_uri(item.get_absolute_url(language))}
        for item in trail
        if item.pk in titles and not item.is_home
    ]
    if not items:
        return ""
    for position, item in enumerate(items, start=1):
        item["position"] = position
    return json_ld({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items})
