"""
Take the public site offline at a set time.

Set SUNSET_AT (an ISO 8601 date and time with a UTC offset, for example
2026-11-16T00:00:00+01:00). Until then every page shows a banner counting down to it.
From then on every public URL returns 410 Gone with a page saying this was a test
project, and robots.txt asks crawlers to drop the site.

The first request after SUNSET_AT also wipes the content for good: every page and its
history, the footer, the materials, and every uploaded image and thumbnail. User
accounts and the admin stay, so the owner can still log in. This cannot be undone.
"""
import logging
import shutil
from pathlib import Path

from django.conf import settings
from django.core.cache import cache
from django.db import IntegrityError, transaction
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone

ALWAYS_AVAILABLE = ("/admin/", "/static/")
WIPE_MARKER = "sunset-wipe"

logger = logging.getLogger(__name__)
_wiped = False  # per process, so the database is asked only until the wipe is seen once


def is_sunset():
    return settings.SUNSET_AT is not None and timezone.now() >= settings.SUNSET_AT


def is_wiped():
    from backend.models import AppliedContentUpdate

    return AppliedContentUpdate.objects.filter(name=WIPE_MARKER).exists()


def wipe_content():
    """Delete all site content and uploaded files. Returns False if it was already done."""
    from cms.models import CMSPlugin, Page, PageContent, PageUrl, Placeholder
    from djangocms_alias.models import Alias, AliasContent, Category
    from djangocms_versioning.models import Version
    from easy_thumbnails.models import Source
    from filer.models import File, Folder

    from backend.models import AppliedContentUpdate, Material

    try:
        with transaction.atomic():
            # The unique name means only one process wins; the others wait here, then skip.
            AppliedContentUpdate.objects.create(name=WIPE_MARKER)
            CMSPlugin.objects.all().delete()
            Placeholder.objects.all().delete()
            Version.objects.all().delete()
            PageContent._base_manager.all().delete()
            PageUrl.objects.all().delete()
            Page.objects.all().delete()
            AliasContent._base_manager.all().delete()
            Alias.objects.all().delete()
            Category.objects.all().delete()
            Material.objects.all().delete()
            Source.objects.all().delete()
            File.objects.all().delete()
            Folder.objects.all().delete()
            transaction.on_commit(delete_media_files)
    except IntegrityError:
        return False
    cache.clear()
    logger.warning("Sunset: all site content and uploaded files were deleted.")
    return True


def delete_media_files():
    root = Path(settings.MEDIA_ROOT)
    if not root.is_dir():
        return
    for path in root.iterdir():
        if path.is_dir() and not path.is_symlink():
            shutil.rmtree(path, ignore_errors=True)
        else:
            path.unlink(missing_ok=True)


def ensure_wiped():
    global _wiped
    if _wiped:
        return
    if not is_wiped():
        try:
            wipe_content()
        except Exception:  # keep serving the notice; the next request tries again
            logger.exception("Sunset: wiping the content failed.")
            return
    _wiped = True


class SunsetMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not is_sunset():
            return self.get_response(request)
        ensure_wiped()
        if request.path.startswith(ALWAYS_AVAILABLE):
            return self.get_response(request)
        if request.path == "/robots.txt":
            return HttpResponse("User-agent: *\nDisallow: /\n", content_type="text/plain")
        html = render_to_string("voxelry/sunset.html", sunset(request))
        response = HttpResponse(html, status=410)
        response["X-Robots-Tag"] = "noindex"
        response["Cache-Control"] = "no-store"
        return response


def sunset(request):
    """Template context: when the site goes offline, for the countdown banner.

    The day and ISO string keep SUNSET_AT's own offset; the date filter would convert
    it to UTC and could show the day before.
    """
    if settings.SUNSET_AT is None:
        return {"sunset_at": None}
    return {"sunset_at": settings.SUNSET_AT, "sunset_day": settings.SUNSET_AT.date(), "sunset_iso": settings.SUNSET_AT.isoformat()}
