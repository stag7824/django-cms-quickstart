"""
Take the public site offline at a set time.

Set SUNSET_AT (an ISO 8601 date and time with a UTC offset, for example
2026-11-16T00:00:00+01:00). Until then every page shows a banner counting down to it.
From then on every public URL returns 410 Gone with a page saying this was a test
project, and robots.txt asks crawlers to drop the site. Pages, images and the database
are left untouched, so the site comes back if SUNSET_AT is removed or moved later.
The Django admin keeps working.
"""
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone

ALWAYS_AVAILABLE = ("/admin/", "/static/")


def is_sunset():
    return settings.SUNSET_AT is not None and timezone.now() >= settings.SUNSET_AT


class SunsetMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not is_sunset() or request.path.startswith(ALWAYS_AVAILABLE):
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
