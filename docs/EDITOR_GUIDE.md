# Voxelry editor guide

Voxelry is a fictional 3D printing brand. Its site follows the structure of a typical
manufacturer's site (like formlabs.com/eu): a mega menu, product pages with jump links,
industry and use-case landing pages, a filterable material catalogue, a resource hub and a
blog, in English and German.

## Set up the starter site

```bash
docker compose up -d database_default
docker compose run --rm web python manage.py migrate
docker compose run --rm web python manage.py createsuperuser
docker compose run --rm web python manage.py seed_voxelry
docker compose up
```

Open http://localhost:8000/admin/, log in, then go to http://localhost:8000/en/.
`seed_voxelry` refuses to run twice, so it never overwrites content you have edited.

## Page types

Pick the template under **Page > Templates** in the toolbar.

| Template | Use it for | Areas |
| --- | --- | --- |
| Voxelry home | The home page | Hero, Sections, Regional, Call to action |
| Voxelry product | Printers, stations, software | Hero, Jump links, Sections, Call to action |
| Voxelry industry or application | Industry and use-case landing pages | Hero, Sections, Related, Call to action |
| Voxelry hub or listing | Category hubs, the catalogue, the resource hub, the blog | Hero, Sections, Call to action |
| Voxelry article | Blog posts, case studies, guides | Body, Related, Call to action |
| Voxelry page | Simple pages: contact, support, legal | Hero, Content, Call to action |

Each area only accepts the blocks it was designed for. The Hero area takes one Hero, which
is the page's only H1. Article pages build their H1 from the page title.

## Blocks

Sections hold everything else. A section has a heading, an optional intro, a background tone,
a link, and an optional **anchor** that jump links point to.

| Block | Goes in | Purpose |
| --- | --- | --- |
| Hero | Hero | Headline, subheading, price note, image, two buttons |
| Section | Sections, Regional, Related | Wrapper with heading and background |
| Jump links | Jump links | Sticky "Fast / Versatile / Simple" navigation on product pages |
| Card grid > Card | Section | Product tiles, feature lists, steps, links |
| Text and image | Section | Copy beside an image, either side |
| Showcase tabs > Showcase tab | Section | Switch between applications |
| Testimonials > Testimonial | Section | Customer quotes |
| Comparison table > Comparison row | Section | In-house vs outsourcing, model vs model |
| Spec table > Spec row | Section | Technical specifications |
| FAQ > FAQ item | Section | Questions, also published as FAQ structured data |
| Resource listing | Section | Articles, filterable by type and industry |
| Material catalogue | Section | Materials, filterable by technology and category |
| Call to action banner | Call to action | Closing dark banner |

Link fields can point to a CMS page, an external URL or a file. Prefer page links: they keep
working when a slug changes and point to the right language automatically.

## Publish a page

1. Create the page from the page tree or **Page > Create page**.
2. Fill in the title, slug, page title (the browser tab and search result title) and meta
   description (70–160 characters). Untick **Menu** for pages that should stay out of the
   navigation, such as blog posts.
3. Build the content in edit mode.
4. Preview it, then click **Publish**. The published version stays live while you edit the
   next draft.

To change a published page, click **Edit**. That creates a new draft, and visitors keep
seeing the published version until you publish again. **Manage versions** shows the history
and lets you compare or revert.

## Publish an article

1. Create the page under **Blog** with the **Voxelry article** template, and untick **Menu**.
2. Open **Page > Resource settings** and set the type, industry, date and listing image. This
   is what the resource hub, the blog and every "Latest news" block use.
3. The meta description becomes the teaser on listing cards, so write it for people.
4. Write the body with text blocks, then publish.

## Localise a page

1. Switch the toolbar language to **Deutsch**. An untranslated page offers to create the
   translation.
2. Give it a German slug (for example `3d-drucker/voxel-s1`), page title and meta description.
3. Copy the English content across with **Copy all plugins** from the English version, or
   build it fresh, then translate every block, including image alt text.
4. Publish. Translations are versioned separately, so the German page can stay in draft
   while the English one is live.

The German menu lists only pages that have a published German version, so a German visitor
is never sent to an English page from the navigation. A page joins the German menu as soon
as its translation is published. Links inside content that point to an untranslated page
still work and redirect to the English version, so label them, for example
"Fallstudie lesen (Englisch)". The starter site leaves the German
**Sinter X** page as a draft so you can practise reviewing and publishing it.

Interface text such as filter labels and "Contact sales" lives in
`backend/locale/de/LC_MESSAGES/django.po`. Edit it, then run `python manage.py
compilemessages`.

## Shared content

The footer is a **static alias** called `footer`, one version per language. Edit it under
**Aliases** in the toolbar or on any page in edit mode. Changes appear on every page once the
alias is published. Use aliases for anything that must stay identical across pages.

Materials live in **Admin > Backend > Materials**, with English and German tabs. Unpublishing
a material removes it from every catalogue on the site.

## Check the content before and after publishing

```bash
docker compose run --rm web python manage.py content_audit
```

The audit loads every published page in every language and reports:

- missing or badly sized titles and meta descriptions
- pages without exactly one H1
- images without alt text (mark purely decorative images as decorative instead)
- broken internal links and jump links with no matching section
- missing canonical and hreflang tags
- how many pages each language has, and which drafts are waiting for review

Add `--strict` to make it fail on errors, for example in CI before a deploy.

The sitemap is served at `/sitemap.xml` and lists every published page in every language.
`/robots.txt` points crawlers to it. Both use the domain in the `DOMAIN` environment
variable, which every deploy copies into **Admin > Sites**.

Never publish a test page on the live site. Use a draft and the preview instead: drafts are
not in the menu or the sitemap.

## Search and sharing metadata

Every page gets Open Graph and Twitter tags with the brand name in the title. The sharing
image is the article's listing image, otherwise the page's hero image, otherwise a default
Voxelry image. Pages also carry structured data for search engines: Organization and
WebSite on the home page, Product (with the starting price from the hero) on product pages,
Article on articles, and a breadcrumb trail on every page below the home page.

## Content updates on a live site

`seed_voxelry` only builds a new site. When the starter content changes later, add a step
to `UPDATES` in `backend/management/commands/update_voxelry.py`. Every deploy runs
`update_voxelry`, which applies each new step once by publishing a new page version (the
previous one stays in the page history). A step is skipped, and tried again on the next
deploy, if the page it changes has an unpublished draft.

## Taking the site offline

`SUNSET_AT` in `compose.prod.yaml` sets when the practice site ends (currently
16 November 2026, 00:00 CET). Until then an orange bar at the top of every page says this is
a test project and counts down to that moment. From then on every public address returns
"410 Gone" with a page explaining it was a test project, and `robots.txt` asks search engines
to drop the site.

The first request after that moment **permanently deletes** every page and its version
history, the footer, the materials, and every uploaded image and thumbnail. User accounts and
the admin are kept. Later deploys do not rebuild the starter site. This cannot be undone:
to keep the site, move or remove `SUNSET_AT` and redeploy **before** the deadline.

## Not included yet

These parts of a real site would come next: a store and checkout, site search, lead forms
connected to a CRM, analytics with cookie consent, A/B testing, and email campaigns.
