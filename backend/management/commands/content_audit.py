from collections import Counter
from html.parser import HTMLParser
from urllib.parse import urldefrag, urlsplit

from cms.models import Page, PageContent
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.test import Client
from djangocms_versioning.constants import DRAFT
from djangocms_versioning.models import Version

TITLE_RANGE = (15, 60)
DESCRIPTION_RANGE = (70, 160)


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.description = None
        self.h1_count = 0
        self.images_without_alt = []
        self.empty_links = 0
        self.links = set()
        self.anchors = set()
        self.fragments = set()
        self.hreflangs = set()
        self.canonical = None
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.anchors.add(attrs["id"])
        if tag == "title":
            self.in_title = True
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "meta" and attrs.get("name") == "description":
            self.description = attrs.get("content") or ""
        elif tag == "link" and attrs.get("rel") == "canonical":
            self.canonical = attrs.get("href")
        elif tag == "link" and attrs.get("rel") == "alternate" and attrs.get("hreflang"):
            self.hreflangs.add(attrs["hreflang"])
        elif tag == "img" and not attrs.get("alt") and attrs.get("role") != "presentation":
            # An empty alt is valid only for images marked as decorative.
            self.images_without_alt.append(attrs.get("src", "?"))
        elif tag == "a":
            href = attrs.get("href")
            if href is None or href == "":
                self.empty_links += 1
            elif href.startswith("#"):
                self.fragments.add(href[1:])
            else:
                self.links.add(href)

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data


class Command(BaseCommand):
    help = "Check every published page for common SEO, accessibility, link and translation problems."

    def add_arguments(self, parser):
        parser.add_argument("--strict", action="store_true", help="Exit with an error if there are any errors.")
        parser.add_argument("--host", default=None, help="Host name to request pages with.")

    def handle(self, *args, **options):
        host = options["host"] or self.default_host()
        self.client = Client(headers={"host": host}, secure=settings.SECURE_SSL_REDIRECT)
        self.link_status = {}
        errors, warnings = [], []
        contents = PageContent.objects.select_related("page").order_by("page__path", "language")

        for content in contents:
            url = content.page.get_absolute_url(content.language, fallback=False)
            problems = self.check_page(url, content.language)
            errors += [(url, problem) for problem in problems["errors"]]
            warnings += [(url, problem) for problem in problems["warnings"]]

        self.report(contents, errors, warnings)
        if errors and options["strict"]:
            raise CommandError(f"{len(errors)} errors found.")

    def default_host(self):
        hosts = [host for host in settings.ALLOWED_HOSTS if host and host != "*"]
        return hosts[0] if hosts else "localhost"

    def check_page(self, url, language):
        errors, warnings = [], []
        response = self.client.get(url)
        if response.status_code != 200:
            return {"errors": [f"returned HTTP {response.status_code}"], "warnings": []}

        parsed = PageParser()
        parsed.feed(response.content.decode())

        title_length = len(parsed.title.strip())
        if not parsed.title.strip():
            errors.append("has no title")
        elif not TITLE_RANGE[0] <= title_length <= TITLE_RANGE[1]:
            warnings.append(f"title is {title_length} characters (aim for {TITLE_RANGE[0]}-{TITLE_RANGE[1]})")

        description_length = len(parsed.description or "")
        if not description_length:
            errors.append("has no meta description")
        elif not DESCRIPTION_RANGE[0] <= description_length <= DESCRIPTION_RANGE[1]:
            warnings.append(
                f"meta description is {description_length} characters "
                f"(aim for {DESCRIPTION_RANGE[0]}-{DESCRIPTION_RANGE[1]})"
            )

        if parsed.h1_count != 1:
            errors.append(f"has {parsed.h1_count} H1 headings (expected 1)")
        if not parsed.canonical:
            errors.append("has no canonical link")
        if language not in parsed.hreflangs:
            errors.append(f"has no hreflang link for its own language ({language})")

        for source in parsed.images_without_alt:
            errors.append(f"image has no alt text: {source}")
        if parsed.empty_links:
            errors.append(f"has {parsed.empty_links} links with no target")
        for fragment in sorted(parsed.fragments - parsed.anchors):
            errors.append(f"jump link has no matching section: #{fragment}")

        for link in sorted(parsed.links):
            status = self.check_link(link)
            if status is not None and status >= 400:
                errors.append(f"broken link ({status}): {link}")
        return {"errors": errors, "warnings": warnings}

    def check_link(self, link):
        target, _fragment = urldefrag(link)
        parts = urlsplit(target)
        if parts.scheme or parts.netloc or not parts.path.startswith("/"):
            return None  # external links would need network access
        if target not in self.link_status:
            self.link_status[target] = self.client.get(target, follow=True).status_code
        return self.link_status[target]

    def report(self, contents, errors, warnings):
        counts = Counter(content.language for content in contents)
        total_pages = Page.objects.count()
        self.stdout.write("Published language versions")
        for code, name in settings.LANGUAGES:
            self.stdout.write(f"  {name}: {counts[code]} of {total_pages} pages")

        drafts = Version.objects.filter(
            state=DRAFT, content_type__app_label="cms", content_type__model="pagecontent"
        )
        self.stdout.write(f"Drafts awaiting review: {drafts.count()}")
        for draft in drafts:
            self.stdout.write(f"  [{draft.content.language}] {draft.content.title}")

        self.write_section("Errors", errors, self.style.ERROR)
        self.write_section("Warnings", warnings, self.style.WARNING)
        summary = f"{len(errors)} errors and {len(warnings)} warnings across {contents.count()} pages."
        self.stdout.write(self.style.ERROR(summary) if errors else self.style.SUCCESS(summary))

    def write_section(self, title, problems, style):
        if problems:
            self.stdout.write(style(f"\n{title} ({len(problems)})"))
            for url, problem in problems:
                self.stdout.write(f"  {url} {problem}")
