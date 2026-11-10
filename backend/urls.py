from cms.sitemaps import CMSSitemap
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from django.urls import path, include, re_path
from django.views.decorators.http import require_GET
from django.views.static import serve


@require_GET
def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    return HttpResponse("\n".join(lines) + "\n", content_type="text/plain")


urlpatterns = [
    # Outside i18n_patterns, so crawlers find it at the site root.
    path('robots.txt', robots_txt),
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': {'cmspages': CMSSitemap}}),

    # Serve uploaded media (images, files from Filer) in production too.
    # Fine for a low-traffic practice site; a big site would use nginx or object storage.
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

urlpatterns += i18n_patterns(path('', include('cms.urls')))

# the new django admin sidebar is bad UX in django CMS custom admin views.
admin.site.enable_nav_sidebar = False
