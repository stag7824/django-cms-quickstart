"""
Starter content for the Voxelry site.

Voxelry, its products, figures, people and customers are invented. The page tree,
URL patterns and page types follow a typical 3D printing manufacturer's site, but
no copy, images or quotes come from a real company.

A page is a dict of placeholder name -> list of blocks. A block is
(plugin type, fields, children). `page("key")` links to another seeded page, and
`art("name")` refers to a generated image from ARTWORK.
"""
from datetime import date


class page:
    def __init__(self, key):
        self.key = key


class art:
    def __init__(self, name):
        self.name = name


def external(url):
    return {"external_link": url}


def hero(heading, sub="", eyebrow="", image=None, alt="", layout="split", price="", primary=None, secondary=None):
    return ("HeroPlugin", {
        "heading": heading, "subheading": sub, "eyebrow": eyebrow, "image": image, "image_alt": alt,
        "layout": layout, "price_note": price,
        "primary_label": primary[0] if primary else "", "primary_link": primary[1] if primary else {},
        "secondary_label": secondary[0] if secondary else "", "secondary_link": secondary[1] if secondary else {},
    }, [])


def section(heading="", *children, intro="", eyebrow="", anchor="", tone="white", cta=None):
    return ("SectionPlugin", {
        "heading": heading, "intro": intro, "eyebrow": eyebrow, "anchor": anchor, "tone": tone,
        "cta_label": cta[0] if cta else "", "cta_link": cta[1] if cta else {},
    }, list(children))


def cards(columns, *children):
    return ("CardGridPlugin", {"columns": columns}, list(children))


def card(title, text="", badge="", image=None, alt="", link=None, label=""):
    return ("VoxelCardPlugin", {
        "title": title, "text": text, "badge": badge, "image": image, "image_alt": alt,
        "link": link or {}, "link_label": label,
    }, [])


def jump_links(*items):
    return ("AnchorNavPlugin", {}, [
        ("AnchorNavItemPlugin", {"title": title, "text": text, "anchor": anchor}, [])
        for title, text, anchor in items
    ])


def text_media(heading, body, image=None, alt="", eyebrow="", image_first=False, cta=None):
    return ("TextMediaPlugin", {
        "heading": heading, "body": body, "image": image, "image_alt": alt, "eyebrow": eyebrow,
        "image_first": image_first,
        "cta_label": cta[0] if cta else "", "cta_link": cta[1] if cta else {},
    }, [])


def tabs(*children):
    return ("ShowcaseTabsPlugin", {}, list(children))


def tab(label, heading, text, image=None, alt="", link=None, link_label=""):
    return ("ShowcaseTabPlugin", {
        "label": label, "heading": heading, "text": text, "image": image, "image_alt": alt,
        "link": link or {}, "link_label": link_label,
    }, [])


def quotes(*items):
    return ("TestimonialGridPlugin", {}, [
        ("TestimonialPlugin", {
            "company": company, "tag": tag, "quote": quote, "person": person, "role": role,
            "link": link or {}, "link_label": link_label,
        }, [])
        for company, tag, quote, person, role, link, link_label in items
    ])


def comparison(columns, rows, footnote=""):
    columns = list(columns) + [""] * (3 - len(columns))
    return ("ComparisonTablePlugin", {
        "column_one": columns[0], "column_two": columns[1], "column_three": columns[2], "footnote": footnote,
    }, [
        ("ComparisonRowPlugin", {
            "label": row[0], "value_one": row[1], "value_two": row[2],
            "value_three": row[3] if len(row) > 3 else "",
        }, [])
        for row in rows
    ])


def specs(title, rows):
    return ("SpecTablePlugin", {"title": title}, [
        ("SpecRowPlugin", {"label": label, "value": value}, []) for label, value in rows
    ])


def faq(*items):
    return ("FAQPlugin", {}, [
        ("FAQItemPlugin", {"question": question, "answer": answer}, []) for question, answer in items
    ])


def cta(heading, text="", primary=None, secondary=None):
    return ("CTABannerPlugin", {
        "heading": heading, "text": text,
        "primary_label": primary[0] if primary else "", "primary_link": primary[1] if primary else {},
        "secondary_label": secondary[0] if secondary else "", "secondary_link": secondary[1] if secondary else {},
    }, [])


def text(body):
    return ("TextPlugin", {"body": body}, [])


def resources(resource_type="", limit=12, filters=True):
    return ("ResourceListingPlugin", {"resource_type": resource_type, "limit": limit, "show_filters": filters}, [])


def materials(technology="", filters=True):
    return ("MaterialCataloguePlugin", {"technology": technology, "show_filters": filters}, [])


def default_cta(lang="en"):
    if lang == "de":
        return [cta(
            "Sprechen Sie mit einem Voxelry-Experten",
            "Wir helfen Ihnen, den passenden Drucker und das richtige Material für Ihre Anwendung zu finden.",
            ("Vertrieb kontaktieren", page("contact")),
            ("Drucker ansehen", page("printers")),
        )]
    return [cta(
        "Talk to a Voxelry specialist",
        "Tell us what you make and we will help you choose the right printer and material.",
        ("Contact sales", page("contact")),
        ("Explore printers", page("printers")),
    )]


# Generated images: name -> (palette, shape, alt text used in Filer)
ARTWORK = {
    "hero": ("ember", "skyline", "Abstract city of stacked orange and graphite voxels"),
    "voxel-s1": ("ember", "printer", "Illustration of the compact Voxel S1 resin printer"),
    "voxel-s1l": ("cobalt", "printer-large", "Illustration of the large-format Voxel S1L resin printer"),
    "sinter-x": ("graphite", "printer-large", "Illustration of the Sinter X powder printer"),
    "rinse-cure": ("teal", "printer", "Illustration of the Rinse + Cure post-processing station"),
    "prototype": ("cobalt", "gear", "Voxel model of a gear prototype"),
    "tooling": ("graphite", "bracket", "Voxel model of a machined bracket"),
    "parts": ("ember", "bracket", "Voxel model of a batch of end-use parts"),
    "aids": ("teal", "gear", "Voxel model of an assembly jig"),
    "models": ("violet", "skyline", "Voxel architectural model"),
    "speed": ("ember", "wave", "Layers of voxels rising in a wave"),
    "accuracy": ("cobalt", "wave", "Precise voxel surface"),
    "workflow": ("teal", "skyline", "Row of voxel towers representing workflow steps"),
    "software": ("violet", "wave", "Voxel surface representing a print preview"),
    "materials": ("teal", "bracket", "Parts printed in several materials"),
    "events": ("violet", "gear", "Voxel model on a trade show stand"),
    "office": ("graphite", "skyline", "Voxel model of the Budapest skyline"),
}

SITE_NAME = "Voxelry"

# key, parent, template, slug, English title, meta description, options
LONG = "voxelry/landing.html"
PAGES = [
    ("home", None, "voxelry/home.html", "home", "Professional 3D printers",
     "Voxelry makes SLA and SLS 3D printers, materials and software for teams that prototype and produce in-house.",
     {"nav": False}),
    ("printers", None, "voxelry/listing.html", "3d-printers", "3D Printers",
     "Compare Voxelry SLA and SLS 3D printers and find the right system for prototypes, tooling and production parts.", {}),
    ("sla", "printers", "voxelry/listing.html", "sla", "SLA Printers",
     "Voxelry SLA resin printers deliver smooth surfaces and fine detail, from desktop models to large-format parts.", {}),
    ("voxel-s1", "sla", "voxelry/product.html", "voxel-s1", "Voxel S1",
     "Voxel S1 is a fast desktop SLA 3D printer with a wide resin library, simple workflow and reliable print results.",
     {"url": "3d-printers/voxel-s1", "page_title": "Voxel S1: Fast Desktop SLA 3D Printer"}),
    ("voxel-s1l", "sla", "voxelry/product.html", "voxel-s1l", "Voxel S1L",
     "Voxel S1L brings the speed of the Voxel S1 to a large build volume for full-size prototypes and big batches.",
     {"url": "3d-printers/voxel-s1l", "page_title": "Voxel S1L: Large-Format SLA 3D Printer"}),
    ("sls", "printers", "voxelry/listing.html", "sls", "SLS Printers",
     "Voxelry SLS powder printers produce strong nylon parts without support structures, ready for end use and batches.", {}),
    ("sinter-x", "sls", "voxelry/product.html", "sinter-x", "Sinter X",
     "Sinter X is an SLS 3D printer for durable nylon parts and small-batch production, with no support structures.",
     {"url": "3d-printers/sinter-x", "page_title": "Sinter X: SLS 3D Printer for Production Parts"}),
    ("post", "printers", "voxelry/listing.html", "post-processing", "Post-Processing",
     "Clean and cure printed parts consistently with Voxelry post-processing stations for SLA and SLS workflows.",
     {"url": "post-processing"}),
    ("rinse-cure", "post", "voxelry/product.html", "rinse-cure", "Rinse + Cure Station",
     "The Rinse + Cure Station automates part cleaning and post-curing so resin parts reach their full properties.",
     {}),
    ("materials", None, "voxelry/listing.html", "materials", "Materials",
     "Browse Voxelry SLA resins and SLS powders. Filter by technology and category and compare key mechanical properties.", {}),
    ("software", None, "voxelry/listing.html", "software", "Software",
     "Voxelry software prepares models, manages printers and tracks every job from a single, simple workflow.", {}),
    ("voxelprep", "software", "voxelry/product.html", "voxelprep", "VoxelPrep",
     "VoxelPrep orients, supports and checks your models automatically so every job is ready to print in minutes.", {}),
    ("voxelfleet", "software", "voxelry/product.html", "voxelfleet", "VoxelFleet",
     "VoxelFleet shows the status of every printer, queues jobs and tracks material use across teams and locations.", {}),
    ("solutions", None, "voxelry/listing.html", "solutions", "Applications",
     "See how teams in automotive, manufacturing and medical use Voxelry 3D printers for prototypes, tools and parts.", {}),
    ("industries", "solutions", "voxelry/listing.html", "industries", "Industries",
     "Explore how Voxelry 3D printers support automotive, manufacturing and medical teams from prototype to production.",
     {"url": "industries"}),
    ("automotive", "industries", LONG, "automotive", "Automotive",
     "See how automotive teams use in-house 3D printing to validate designs sooner and reduce tooling lead times.",
     {"page_title": "3D Printing for Automotive and Transportation"}),
    ("manufacturing", "industries", LONG, "manufacturing", "Manufacturing",
     "Use 3D printing to produce jigs, fixtures and spare parts on demand and keep your production lines running.",
     {"page_title": "3D Printing for Manufacturing"}),
    ("medical", "industries", LONG, "medical", "Medical",
     "Support clinical teams with in-house anatomical models and research devices using Voxelry 3D printers.",
     {"page_title": "3D Printing for Medical Teams"}),
    ("applications", "solutions", "voxelry/listing.html", "applications", "Use Cases",
     "From rapid prototyping to rapid tooling, explore the most common ways teams put Voxelry 3D printers to work.",
     {"url": "applications"}),
    ("rapid-prototyping", "applications", LONG, "rapid-prototyping", "Rapid Prototyping",
     "Move from concept to validated design faster by printing realistic, functional prototypes in-house.",
     {"page_title": "Rapid Prototyping With 3D Printing"}),
    ("rapid-tooling", "applications", LONG, "rapid-tooling", "Rapid Tooling",
     "Print molds, patterns and short-run tools in-house to reduce lead times and test designs before hard tooling.",
     {"page_title": "Rapid Tooling With 3D Printing"}),
    ("learn", None, "voxelry/listing.html", "resources", "Learn",
     "Read guides, customer stories, white papers and news about professional 3D printing from the Voxelry team.", {}),
    ("library", "learn", "voxelry/listing.html", "library", "Resources",
     "Filter Voxelry guides, customer stories and white papers by content type and industry to find what you need.",
     {}),
    ("blog", "learn", "voxelry/listing.html", "blog", "Blog",
     "The latest Voxelry product news, material launches and stories from customers who print in-house.",
     {"url": "blog", "page_title": "The Voxelry Blog"}),
    ("sinter-nylon", "blog", "voxelry/article.html", "pa11-pro-powder", "Introducing PA11 Pro Powder for Sinter X",
     "A new ductile nylon for Sinter X gives snap fits, clips and living hinges the durability they need in daily use.",
     {"nav": False, "resource": ("news", "manufacturing", date(2026, 10, 14), "parts")}),
    ("northline", "blog", "voxelry/article.html", "northline-cycles", "How Northline Cycles Tests Frames in Days",
     "A fictional customer story: how a small bicycle maker cut validation time by printing fixtures and test parts.",
     {"nav": False, "resource": ("case_study", "manufacturing", date(2026, 9, 2), "prototype")}),
    ("alpenrad", "blog", "voxelry/article.html", "alpenrad-validation", "How Alpenrad Validates Interior Parts In-House",
     "A fictional customer story: how a German automotive supplier validates interior parts before cutting any tools.",
     {"nav": False, "resource": ("case_study", "automotive", date(2026, 7, 21), "tooling")}),
    ("harbor", "blog", "voxelry/article.html", "harbor-robotics", "How Harbor Robotics Prints Its Gripper Fingers",
     "A fictional customer story: how a robotics start-up moved its gripper fingers from machined parts to SLS nylon.",
     {"nav": False, "resource": ("case_study", "manufacturing", date(2026, 10, 28), "parts")}),
    ("sla-vs-sls", "blog", "voxelry/article.html", "sla-vs-sls", "SLA vs SLS: How to Choose a Print Technology",
     "A practical guide to choosing between resin and powder 3D printing based on your part, budget and workflow.",
     {"nav": False, "resource": ("guide", "", date(2026, 5, 11), "materials")}),
    ("events", "learn", "voxelry/listing.html", "events", "Events",
     "Meet the Voxelry team at trade shows and workshops across Europe and see printed parts up close.", {"url": "events"}),
    ("support", None, "voxelry.html", "support", "Support",
     "Find setup guides, troubleshooting help and service plans to keep your Voxelry printers running.", {}),
    ("contact", None, "voxelry.html", "contact", "Contact",
     "Talk to the Voxelry team about printers, materials, sample parts or a demonstration for your application.", {}),
    ("about", None, "voxelry.html", "company", "About Voxelry",
     "Voxelry is a fictional 3D printing brand created as a practice project for building a multi-language CMS site.",
     {"nav": False}),
    ("privacy", None, "voxelry.html", "privacy-policy", "Privacy Policy",
     "This practice site does not sell anything or collect personal data beyond what the CMS needs for its editors.",
     {"nav": False}),
]

GERMAN_PAGES = {
    "home": ("Professionelle 3D-Drucker", "startseite",
             "Voxelry entwickelt SLA- und SLS-3D-Drucker, Materialien und Software für Teams, die im eigenen Haus fertigen.",
             {}, True),
    "printers": ("3D-Drucker", "3d-drucker",
                 "Vergleichen Sie die SLA- und SLS-3D-Drucker von Voxelry und finden Sie das passende System für Ihre Teile.",
                 {}, True),
    "voxel-s1": ("Voxel S1", "voxel-s1",
                 "Voxel S1 ist ein schneller SLA-Desktop-3D-Drucker mit großer Harzauswahl und einem einfachen Arbeitsablauf.",
                 {"url": "3d-drucker/voxel-s1", "page_title": "Voxel S1: Schneller SLA-Desktop-3D-Drucker"}, True),
    "materials": ("Materialien", "materialien",
                  "Entdecken Sie die SLA-Harze und SLS-Pulver von Voxelry. Filtern Sie nach Technologie und Kategorie.",
                  {}, True),
    "automotive": ("Automobilindustrie", "automobilindustrie",
                   "So nutzen Automobilteams den 3D-Druck im eigenen Haus, um Entwürfe früher zu prüfen und Werkzeugzeiten zu senken.",
                   {"url": "branchen/automobilindustrie", "page_title": "3D-Druck für die Automobilindustrie"}, True),
    "support": ("Support", "support",
                "Einrichtungsanleitungen, Hilfe bei Druckproblemen und Servicepläne, damit Ihre Voxelry-Drucker zuverlässig laufen.",
                {}, True),
    "contact": ("Kontakt", "kontakt",
                "Sprechen Sie mit dem Voxelry-Team über Drucker, Materialien, Musterteile oder eine Vorführung für Ihre Anwendung.",
                {"page_title": "Kontakt zu Voxelry"}, True),
    # Left as a draft so the editor guide has a real page to review and publish.
    "sinter-x": ("Sinter X", "sinter-x",
                 "Sinter X ist ein SLS-3D-Drucker für robuste Nylonteile und Kleinserien, ganz ohne Stützstrukturen.",
                 {"url": "3d-drucker/sinter-x", "page_title": "Sinter X: SLS-3D-Drucker für Serienteile"}, False),
}


def printer_card(key, name, text, badge, label="See details"):
    return card(name, text, badge, art(key), f"{name} 3D printer", page(key), label)


def home_en():
    return {
        "Hero": [hero(
            "Tools that bring ideas to life",
            "SLA and SLS 3D printers for teams that would rather make it today than wait for it next month.",
            "New: Sinter X",
            art("hero"), "Abstract city of stacked orange and graphite voxels", "overlay",
            primary=("Explore Sinter X", page("sinter-x")), secondary=("All 3D printers", page("printers")),
        )],
        "Sections": [
            section(
                "Find your printer",
                cards(
                    3,
                    printer_card("voxel-s1", "Voxel S1", "Fast, precise resin printing that fits on a desk.", "SLA"),
                    printer_card("voxel-s1l", "Voxel S1L", "The same workflow, with room for much larger parts.", "SLA"),
                    printer_card("sinter-x", "Sinter X", "Strong nylon parts with no support structures.", "SLS · New"),
                ),
                intro="Professional resin and powder systems, all prepared with the same software.",
                cta=("Compare all printers", page("printers")),
            ),
            section(
                "Latest news",
                resources(limit=3, filters=False),
                tone="light",
                cta=("Read all news", page("blog")),
            ),
            section(
                "Make anything with Voxelry",
                tabs(
                    tab("Rapid prototyping", "See it and test it within a day",
                        "Turn a concept into a realistic, functional prototype overnight, then change it again tomorrow.",
                        art("prototype"), "Voxel model of a gear prototype", page("rapid-prototyping"), "Learn more"),
                    tab("Rapid tooling", "Test the tool before you pay for it",
                        "Print molds and patterns in-house to prove out a design before you commit to hard tooling.",
                        art("tooling"), "Voxel model of a machined bracket", page("rapid-tooling"), "Learn more"),
                    tab("End-use parts", "Produce parts on demand",
                        "Make small batches and spare parts when you need them, without minimum order quantities.",
                        art("parts"), "Voxel model of a batch of end-use parts", page("manufacturing"), "Learn more"),
                ),
                cta=("Explore applications", page("solutions")),
            ),
            section(
                "Materials for every application",
                cards(
                    4,
                    card("General purpose", "Everyday resins for models and concept parts.", link=page("materials"), label="Browse"),
                    card("Impact resistant", "Tough materials for parts that take a knock.", link=page("materials"), label="Browse"),
                    card("Temperature resistant", "Keep your shape when the heat is on.", link=page("materials"), label="Browse"),
                    card("Elastomeric", "Soft, flexible parts that bounce back.", link=page("materials"), label="Browse"),
                ),
                intro="Filter the full library of resins and powders by technology, category and properties.",
                tone="light",
                cta=("All materials", page("materials")),
            ),
        ],
        "Regional": [
            section(
                "Voxelry in Europe",
                cards(
                    3,
                    card("Meet us at events", "See printed parts up close at a show near you.", image=art("events"), alt="Voxel model on a trade show stand", link=page("events"), label="See upcoming events"),
                    card("Read customer stories", "How European teams use Voxelry every day.", image=art("tooling"), alt="Voxel model of a machined bracket", link=page("alpenrad"), label="Read the story"),
                    card("Visit our Budapest office", "Book a demonstration with our specialists.", image=art("office"), alt="Voxel model of the Budapest skyline", link=page("contact"), label="Schedule a visit"),
                ),
            ),
            section(
                "Trusted by teams that make things",
                quotes(
                    ("Northline Cycles", "Manufacturing aids",
                     "We used to plan around the supplier's calendar. Now we plan around the next test ride.",
                     "Ana Kovács", "Head of Engineering", page("northline"), "Read the story"),
                    ("Alpenrad", "Rapid prototyping",
                     "We find the fit problems on Tuesday, fix them on Wednesday and never pay for them in tooling.",
                     "Jonas Weber", "Interior Development Lead", page("alpenrad"), "Read the story"),
                    ("Harbor Robotics", "End-use parts",
                     "Most of our gripper fingers now start and finish on Sinter X. No one has asked to go back.",
                     "Mei Tan", "Mechanical Engineer", page("harbor"), "Read the story"),
                ),
                tone="light",
                cta=("All customer stories", page("library")),
            ),
        ],
        "Call to action": default_cta(),
    }


def home_de():
    return {
        "Hero": [hero(
            "Werkzeuge, die Ideen Wirklichkeit werden lassen",
            "SLA- und SLS-3D-Drucker für Teams, die lieber heute fertigen, als bis zum nächsten Monat zu warten.",
            "Neu: Sinter X",
            art("hero"), "Abstrakte Stadt aus gestapelten orangefarbenen und grafitgrauen Voxeln", "overlay",
            primary=("Sinter X entdecken", page("sinter-x")), secondary=("Alle 3D-Drucker", page("printers")),
        )],
        "Sections": [
            section(
                "Finden Sie Ihren Drucker",
                cards(
                    3,
                    card("Voxel S1", "Schneller, präziser Harzdruck, der auf jeden Schreibtisch passt.", "SLA", art("voxel-s1"), "Voxel S1 3D-Drucker", page("voxel-s1"), "Details ansehen"),
                    card("Voxel S1L", "Derselbe Arbeitsablauf mit Platz für deutlich größere Teile.", "SLA", art("voxel-s1l"), "Voxel S1L 3D-Drucker", page("voxel-s1l"), "Details ansehen"),
                    card("Sinter X", "Robuste Nylonteile ganz ohne Stützstrukturen.", "SLS · Neu", art("sinter-x"), "Sinter X 3D-Drucker", page("sinter-x"), "Details ansehen"),
                ),
                intro="Professionelle Harz- und Pulversysteme, alle mit derselben Software vorbereitet.",
                cta=("Alle Drucker vergleichen", page("printers")),
            ),
            # The use-case pages are English only, so these tabs carry no links. The
            # section links to the one application page that exists in German.
            section(
                "Fertigen Sie alles mit Voxelry",
                tabs(
                    tab("Rapid Prototyping", "Heute sehen, morgen testen",
                        "Machen Sie aus einem Konzept über Nacht einen realistischen, funktionsfähigen Prototyp und ändern Sie ihn am nächsten Tag erneut.",
                        art("prototype"), "Voxel-Modell eines Zahnrad-Prototyps"),
                    tab("Rapid Tooling", "Das Werkzeug testen, bevor Sie dafür bezahlen",
                        "Drucken Sie Formen und Modelle im eigenen Haus und prüfen Sie einen Entwurf, bevor Sie in Serienwerkzeuge investieren.",
                        art("tooling"), "Voxel-Modell einer gefrästen Halterung"),
                    tab("Endteile", "Teile nach Bedarf fertigen",
                        "Fertigen Sie Kleinserien und Ersatzteile genau dann, wenn Sie sie brauchen, ganz ohne Mindestbestellmengen.",
                        art("parts"), "Voxel-Modell einer Serie von Endteilen"),
                ),
                tone="light",
                cta=("3D-Druck in der Automobilindustrie", page("automotive")),
            ),
            section(
                "Materialien für jede Anwendung",
                cards(
                    4,
                    card("Allzweck", "Harze für Modelle und Konzeptteile.", link=page("materials"), label="Ansehen"),
                    card("Schlagfest", "Zähe Materialien für stark beanspruchte Teile.", link=page("materials"), label="Ansehen"),
                    card("Temperaturbeständig", "Formstabil auch bei hoher Hitze.", link=page("materials"), label="Ansehen"),
                    card("Elastomer", "Weiche, flexible Teile, die in Form zurückkehren.", link=page("materials"), label="Ansehen"),
                ),
                intro="Filtern Sie die gesamte Bibliothek nach Technologie und Kategorie.",
                tone="light",
                cta=("Alle Materialien", page("materials")),
            ),
        ],
        "Regional": [
            section(
                "Voxelry in Europa",
                cards(
                    2,
                    card("Treffen Sie uns auf Messen", "Sehen Sie gedruckte Teile aus der Nähe.", image=art("events"), alt="Voxel-Modell auf einem Messestand", link=page("events"), label="Termine ansehen"),
                    card("Besuchen Sie unser Büro in Budapest", "Vereinbaren Sie eine Vorführung mit unseren Fachleuten.", image=art("office"), alt="Voxel-Modell der Budapester Skyline", link=page("contact"), label="Besuch vereinbaren"),
                ),
            ),
            # The customer stories are only published in English, and the labels say so.
            section(
                "Teams, die Dinge herstellen, vertrauen uns",
                quotes(
                    ("Northline Cycles", "Fertigungshilfen",
                     "Früher haben wir uns nach dem Kalender des Zulieferers gerichtet. Heute richten wir uns nach der nächsten Testfahrt.",
                     "Ana Kovács", "Leitung Entwicklung", page("northline"), "Fallstudie lesen (Englisch)"),
                    ("Alpenrad", "Rapid Prototyping",
                     "Passungsprobleme finden wir am Dienstag, beheben sie am Mittwoch und bezahlen nie mit einem Werkzeug dafür.",
                     "Jonas Weber", "Leitung Interieur-Entwicklung", page("alpenrad"), "Fallstudie lesen (Englisch)"),
                    ("Harbor Robotics", "Endteile",
                     "Die meisten unserer Greiferfinger entstehen heute komplett auf dem Sinter X. Niemand will zurück.",
                     "Mei Tan", "Mechanische Konstruktion", page("harbor"), "Fallstudie lesen (Englisch)"),
                ),
                tone="light",
            ),
        ],
        "Call to action": default_cta("de"),
    }


PRODUCTS = {
    "voxel-s1": {
        "en": {
            "eyebrow": "Desktop SLA 3D printer",
            "heading": "Voxel S1",
            "sub": "Industrial results at desktop size, with most prints finished before your next meeting.",
            "price": "From €2,950",
            "buy": "Request a quote", "expert": "Talk to an expert",
            "highlights": [("Fast", "Most prints under three hours", "speed"),
                           ("Versatile", "A resin for every job", "materials"),
                           ("Simple", "Learn it in an afternoon", "workflow"),
                           ("Accurate", "Parts that fit first time", "accuracy")],
            "speed_h": "Get more done with most prints in under three hours",
            "speed_i": "An even, high-power light source cures each layer at once, so a full build takes about as long as a single part.",
            "speed_t": "Iterate during the day, not overnight",
            "speed_b": "<p>Print, test and change a design several times before you go home. Illustrative figures are shown for a typical 50 mm part.</p>",
            "compare_cols": ["Voxel S1", "Previous generation"],
            "compare_rows": [("Typical print time", "2 h 40 min", "7 h 15 min"), ("Parts per day", "9", "3"), ("Hands-on time", "10 min", "25 min")],
            "foot": "Illustrative figures for a fictional product.",
            "materials_h": "Tackle any problem with one resin library",
            "materials_i": "Swap cartridges in seconds and move between rigid, tough and flexible parts.",
            "workflow_h": "So simple that anyone can print",
            "steps": [("1. Prepare", "Import your model. VoxelPrep orients and supports it automatically."),
                      ("2. Print", "Load a cartridge and press start. Settings are validated for each resin."),
                      ("3. Rinse and cure", "Move the build to the Rinse + Cure Station for automatic finishing."),
                      ("4. Finish", "Remove supports and sand, coat or paint if the job needs it.")],
            "accuracy_t": "Parts that always fit",
            "accuracy_b": "<ul><li>Fine detail from a 40 µm pixel size</li><li>Smooth surfaces straight from the printer</li><li>Consistent dimensions across the build platform</li></ul>",
            "specs_t": "Tech specs",
            "specs": [("Technology", "Masked SLA"), ("Build volume", "200 × 125 × 210 mm"), ("Layer height", "25–200 µm"), ("Connectivity", "Wi-Fi, Ethernet, USB")],
            "eco_h": "Complete your workflow",
            "eco": [("Rinse + Cure Station", "Automated cleaning and post-curing.", "rinse-cure"),
                    ("VoxelPrep", "Automatic orientation and supports.", "voxelprep"),
                    ("VoxelFleet", "Track every printer and every job.", "voxelfleet")],
            "see": "See details",
            "alt": "Illustration of the compact Voxel S1 resin printer",
            "speed_alt": "Layers of voxels rising in a wave",
            "accuracy_alt": "Close-up of a precise voxel surface",
            "technology": "sla",
        },
        "de": {
            "eyebrow": "SLA-Desktop-3D-Drucker",
            "heading": "Voxel S1",
            "sub": "Industrielle Ergebnisse im Desktop-Format. Die meisten Drucke sind vor Ihrem nächsten Termin fertig.",
            "price": "Ab 2.950 €",
            "buy": "Angebot anfordern", "expert": "Mit Fachleuten sprechen",
            "highlights": [("Schnell", "Die meisten Drucke unter drei Stunden", "tempo"),
                           ("Vielseitig", "Das passende Harz für jede Aufgabe", "materialien"),
                           ("Einfach", "An einem Nachmittag erlernt", "ablauf"),
                           ("Präzise", "Teile, die auf Anhieb passen", "genauigkeit")],
            "speed_h": "Mehr schaffen, mit Drucken unter drei Stunden",
            "speed_i": "Eine gleichmäßige, starke Lichtquelle härtet jede Schicht auf einmal aus. Ein voller Druckauftrag dauert daher kaum länger als ein einzelnes Teil.",
            "speed_t": "Tagsüber iterieren statt über Nacht",
            "speed_b": "<p>Drucken, testen und ändern Sie einen Entwurf mehrmals am Tag. Die Beispielwerte gelten für ein typisches Teil von 50 mm.</p>",
            "compare_cols": ["Voxel S1", "Vorgängergeneration"],
            "compare_rows": [("Typische Druckzeit", "2 Std. 40 Min.", "7 Std. 15 Min."), ("Teile pro Tag", "9", "3"), ("Arbeitszeit", "10 Min.", "25 Min.")],
            "foot": "Beispielwerte für ein fiktives Produkt.",
            "materials_h": "Eine Harzbibliothek für jede Aufgabe",
            "materials_i": "Wechseln Sie Kartuschen in Sekunden und drucken Sie steife, zähe und flexible Teile.",
            "workflow_h": "So einfach, dass jeder drucken kann",
            "steps": [("1. Vorbereiten", "Modell importieren. VoxelPrep richtet es aus und stützt es automatisch."),
                      ("2. Drucken", "Kartusche einsetzen und starten. Die Einstellungen sind für jedes Harz geprüft."),
                      ("3. Spülen und härten", "Die Rinse + Cure Station übernimmt die automatische Nachbearbeitung."),
                      ("4. Fertigstellen", "Stützen entfernen und bei Bedarf schleifen, beschichten oder lackieren.")],
            "accuracy_t": "Teile, die immer passen",
            "accuracy_b": "<ul><li>Feine Details dank 40 µm Pixelgröße</li><li>Glatte Oberflächen direkt aus dem Drucker</li><li>Gleichbleibende Maße auf der gesamten Bauplattform</li></ul>",
            "specs_t": "Technische Daten",
            "specs": [("Technologie", "Masked SLA"), ("Bauvolumen", "200 × 125 × 210 mm"), ("Schichthöhe", "25–200 µm"), ("Anschlüsse", "WLAN, Ethernet, USB")],
            "eco_h": "Vervollständigen Sie Ihren Arbeitsablauf",
            "eco": [("Rinse + Cure Station", "Automatische Reinigung und Nachhärtung.", "rinse-cure"),
                    ("VoxelPrep", "Automatische Ausrichtung und Stützen.", "voxelprep"),
                    ("VoxelFleet", "Jeden Drucker und jeden Auftrag im Blick.", "voxelfleet")],
            "see": "Details ansehen",
            "alt": "Illustration des kompakten Voxel S1 Harzdruckers",
            "speed_alt": "Voxel-Schichten, die wellenförmig ansteigen",
            "accuracy_alt": "Nahaufnahme einer präzisen Voxel-Oberfläche",
            "technology": "sla",
        },
    },
    "sinter-x": {
        "en": {
            "eyebrow": "SLS 3D printer",
            "heading": "Sinter X",
            "sub": "Strong nylon parts in batches, with no support structures and no tooling to wait for.",
            "price": "From €24,500",
            "buy": "Request a quote", "expert": "Talk to an expert",
            "highlights": [("Strong", "Isotropic nylon parts", "speed"),
                           ("Productive", "Pack the whole chamber", "materials"),
                           ("Clean", "Closed powder handling", "workflow"),
                           ("Economical", "Reuse unsintered powder", "accuracy")],
            "speed_h": "Parts that are ready for real use",
            "speed_i": "Printed nylon holds up to repeated stress, so the part you test can be the part you ship.",
            "speed_t": "From prototype to production on one machine",
            "speed_b": "<p>Validate a design with a few parts, then fill the chamber and run a batch with the same settings.</p>",
            "compare_cols": ["Sinter X", "Outsourced parts"],
            "compare_rows": [("Lead time", "2 days", "2 weeks"), ("Cost per part", "€6", "€22"), ("Design changes", "Same day", "New order")],
            "foot": "Illustrative figures for a fictional product.",
            "materials_h": "Powders for demanding parts",
            "materials_i": "Choose general-purpose nylon or a ductile grade for snap fits and hinges.",
            "workflow_h": "A cleaner powder workflow",
            "steps": [("1. Pack", "Nest parts automatically to fill the build chamber."),
                      ("2. Sinter", "No supports are needed because the powder holds each part."),
                      ("3. Recover", "Separate parts and return unused powder to the system."),
                      ("4. Finish", "Media blast the parts, then dye or coat them if needed.")],
            "accuracy_t": "Less waste, lower cost per part",
            "accuracy_b": "<ul><li>Reuse a large share of unsintered powder</li><li>Reduce labour with closed-loop handling</li><li>Run batches overnight</li></ul>",
            "specs_t": "Tech specs",
            "specs": [("Technology", "Selective laser sintering"), ("Build volume", "300 × 300 × 350 mm"), ("Layer height", "110 µm"), ("Materials", "PA12, PA11 Pro")],
            "eco_h": "Complete your workflow",
            "eco": [("VoxelPrep", "Automatic nesting for full builds.", "voxelprep"),
                    ("VoxelFleet", "Track powder use and every job.", "voxelfleet"),
                    ("Materials", "Compare all SLS powders.", "materials")],
            "see": "See details",
            "alt": "Illustration of the Sinter X powder printer",
            "speed_alt": "Layers of voxels rising in a wave",
            "accuracy_alt": "Close-up of a precise voxel surface",
            "technology": "sls",
        },
        "de": {
            "eyebrow": "SLS-3D-Drucker",
            "heading": "Sinter X",
            "sub": "Robuste Nylonteile in Serie, ohne Stützstrukturen und ohne Wartezeit auf Werkzeuge.",
            "price": "Ab 24.500 €",
            "buy": "Angebot anfordern", "expert": "Mit Fachleuten sprechen",
            "highlights": [("Robust", "Isotrope Nylonteile", "tempo"),
                           ("Produktiv", "Die ganze Kammer nutzen", "materialien"),
                           ("Sauber", "Geschlossene Pulverführung", "ablauf"),
                           ("Wirtschaftlich", "Ungesintertes Pulver wiederverwenden", "genauigkeit")],
            "speed_h": "Teile für den echten Einsatz",
            "speed_i": "Gedrucktes Nylon hält wiederholter Belastung stand. Das getestete Teil kann also auch das ausgelieferte Teil sein.",
            "speed_t": "Vom Prototyp zur Serie auf einer Maschine",
            "speed_b": "<p>Prüfen Sie einen Entwurf mit wenigen Teilen und starten Sie dann mit denselben Einstellungen eine Serie.</p>",
            "compare_cols": ["Sinter X", "Fremdbezug"],
            "compare_rows": [("Lieferzeit", "2 Tage", "2 Wochen"), ("Kosten pro Teil", "6 €", "22 €"), ("Designänderungen", "Am selben Tag", "Neue Bestellung")],
            "foot": "Beispielwerte für ein fiktives Produkt.",
            "materials_h": "Pulver für anspruchsvolle Teile",
            "materials_i": "Wählen Sie Allzweck-Nylon oder eine duktile Sorte für Schnappverbindungen und Scharniere.",
            "workflow_h": "Ein sauberer Pulverprozess",
            "steps": [("1. Anordnen", "Teile automatisch anordnen und die Baukammer füllen."),
                      ("2. Sintern", "Keine Stützen nötig, denn das Pulver hält jedes Teil."),
                      ("3. Zurückgewinnen", "Teile trennen und ungenutztes Pulver zurückführen."),
                      ("4. Fertigstellen", "Teile strahlen und bei Bedarf färben oder beschichten.")],
            "accuracy_t": "Weniger Abfall, geringere Kosten pro Teil",
            "accuracy_b": "<ul><li>Einen großen Teil des Pulvers wiederverwenden</li><li>Weniger Handarbeit dank geschlossenem Kreislauf</li><li>Serien über Nacht fertigen</li></ul>",
            "specs_t": "Technische Daten",
            "specs": [("Technologie", "Selektives Lasersintern"), ("Bauvolumen", "300 × 300 × 350 mm"), ("Schichthöhe", "110 µm"), ("Materialien", "PA12, PA11 Pro")],
            "eco_h": "Vervollständigen Sie Ihren Arbeitsablauf",
            "eco": [("VoxelPrep", "Automatische Anordnung für volle Baukammern.", "voxelprep"),
                    ("VoxelFleet", "Pulververbrauch und Aufträge im Blick.", "voxelfleet"),
                    ("Materialien", "Alle SLS-Pulver vergleichen.", "materials")],
            "see": "Details ansehen",
            "alt": "Illustration des Sinter X Pulverdruckers",
            "speed_alt": "Voxel-Schichten, die wellenförmig ansteigen",
            "accuracy_alt": "Nahaufnahme einer präzisen Voxel-Oberfläche",
            "technology": "sls",
        },
    },
}
PRODUCTS["voxel-s1l"] = {"en": {
    **PRODUCTS["voxel-s1"]["en"],
    "eyebrow": "Large-format SLA 3D printer",
    "heading": "Voxel S1L",
    "sub": "The Voxel S1 workflow with a much larger build volume, for full-size prototypes and big batches.",
    "price": "From €9,800",
    "speed_h": "Print large parts without waiting days",
    "compare_cols": ["Voxel S1L", "Voxel S1"],
    "compare_rows": [("Build volume", "340 × 200 × 360 mm", "200 × 125 × 210 mm"), ("Full build time", "7 h", "3 h"), ("Parts per build", "48", "16")],
    "specs": [("Technology", "Masked SLA"), ("Build volume", "340 × 200 × 360 mm"), ("Layer height", "25–200 µm"), ("Connectivity", "Wi-Fi, Ethernet, USB")],
    "alt": "Illustration of the large-format Voxel S1L resin printer",
}}
PRODUCTS["rinse-cure"] = {"en": {
    **PRODUCTS["voxel-s1"]["en"],
    "eyebrow": "SLA post-processing",
    "heading": "Rinse + Cure Station",
    "sub": "Automated cleaning and post-curing, so every resin part reaches its full material properties.",
    "price": "From €890",
    "highlights": [("Automatic", "Hands-off rinsing", "speed"), ("Consistent", "Validated curing cycles", "accuracy"), ("Compact", "Fits beside the printer", "workflow")],
    "speed_h": "Finish parts without standing over them",
    "speed_t": "Start the cycle and walk away",
    "speed_b": "<p>The build platform rinses and lifts out automatically when the cycle ends, so parts never soak too long.</p>",
    "compare_cols": ["Rinse + Cure", "Manual finishing"],
    "compare_rows": [("Hands-on time", "2 min", "20 min"), ("Consistency", "Validated", "Operator dependent")],
    "specs": [("Rinse volume", "8.5 L"), ("Cure wavelength", "405 nm"), ("Max. temperature", "80 °C"), ("Compatibility", "Voxel S1")],
    "speed_i": "Rinsing and curing are where many good prints get ruined. Automating both removes the guesswork.",
    "workflow_h": "Three steps from printer to finished part",
    "steps": [("1. Rinse", "Lift the build platform straight into the rinse bucket and start the cycle."),
              ("2. Dry", "Parts lift out automatically when the cycle ends, so they never soak too long."),
              ("3. Cure", "Choose the resin and the station sets the right time and temperature.")],
    "accuracy_t": "Consistent results on every build",
    "accuracy_b": "<ul><li>Validated cycles for every Voxelry resin</li><li>Even light and heat across the whole chamber</li><li>Less solvent wasted on each build</li></ul>",
    "technology": None,
    "eco": [("Voxel S1", "The desktop printer this station is made for.", "voxel-s1"),
            ("VoxelPrep", "Automatic orientation and supports.", "voxelprep"),
            ("VoxelFleet", "Track every printer and every job.", "voxelfleet")],
    "alt": "Illustration of the Rinse + Cure post-processing station",
}}
for _key, _name, _sub, _eyebrow, _spec in [
    ("voxelprep", "VoxelPrep", "Import a model and get a print-ready job in minutes, with orientation and supports handled for you.", "Print preparation software",
     [("Platforms", "Windows, macOS"), ("File types", "STL, OBJ, 3MF"), ("Price", "Free with every printer")]),
    ("voxelfleet", "VoxelFleet", "Every printer, every queue and every litre of material, visible in one place from any browser.", "Fleet management software",
     [("Access", "Web and mobile"), ("Team roles", "Admin, operator, viewer"), ("Price", "Free with every printer")]),
]:
    PRODUCTS[_key] = {"en": {
        **PRODUCTS["voxel-s1"]["en"],
        "eyebrow": _eyebrow, "heading": _name, "sub": _sub, "price": "",
        "buy": "Download for free", "expert": "Book a demo",
        "highlights": [("Automatic", "Smart defaults", "speed"), ("Simple", "No training required", "workflow"), ("Connected", "Works across the team", "accuracy")],
        "speed_h": f"{_name} takes care of the routine work",
        "speed_i": "Spend your time on the part, not on setting up the job.",
        "speed_t": "Good results by default, full control when you want it",
        "speed_b": "<p>Start with validated settings and adjust the details only when a job calls for it.</p>",
        "compare_cols": [_name, "Manual setup"],
        "compare_rows": [("Job setup", "2 min", "30 min"), ("Failed prints", "Rare", "Common")],
        "specs": _spec,
        "alt": f"Abstract illustration of {_name}",
        "workflow_h": "From file to finished job",
        "steps": [("1. Import", "Open a model file or pick up a job from your team's queue."),
                  ("2. Review", "Check the suggested settings, or change them when a job calls for it."),
                  ("3. Send", "Send the job to any printer on your network, or queue it for later.")],
        "accuracy_t": "Built for working teams",
        "accuracy_b": "<ul><li>One account for every printer and every user</li><li>A shared history of jobs, settings and results</li><li>Updates included at no extra cost</li></ul>",
        "technology": None,
        "eco": [(name, body, target) for name, body, target in [
            ("Voxel S1", "Fast desktop resin printing.", "voxel-s1"),
            ("Sinter X", "Nylon parts without supports.", "sinter-x"),
            ("VoxelPrep", "Automatic orientation and supports.", "voxelprep"),
            ("VoxelFleet", "Track every printer and every job.", "voxelfleet"),
        ] if target != _key],
    }}


def product_page(key, lang):
    c = PRODUCTS[key][lang]
    image = {"voxelprep": "software", "voxelfleet": "software"}.get(key, key)
    anchors = {"speed": "speed", "materials": "materials", "workflow": "workflow", "accuracy": "accuracy"}
    if lang == "de":
        anchors = {"speed": "tempo", "materials": "materialien", "workflow": "ablauf", "accuracy": "genauigkeit"}
    sections = [
        section(c["speed_h"],
                text_media(c["speed_t"], c["speed_b"], art("speed"), c["speed_alt"], image_first=True),
                comparison(c["compare_cols"], c["compare_rows"], c["foot"]),
                intro=c["speed_i"], anchor=anchors["speed"]),
        section(c["workflow_h"],
                cards(len(c["steps"]), *[card(title, body) for title, body in c["steps"]]),
                tone="light", anchor=anchors["workflow"]),
    ]
    # Only printers have materials to compare.
    if c["technology"]:
        sections.append(section(c["materials_h"], materials(c["technology"], filters=False),
                                intro=c["materials_i"], anchor=anchors["materials"]))
    sections += [
        section(c["accuracy_t"],
                text_media(c["heading"], c["accuracy_b"], art("accuracy"), c["accuracy_alt"]),
                specs(c["specs_t"], c["specs"]),
                tone="light", anchor=anchors["accuracy"]),
        section(c["eco_h"],
                cards(3, *[card(title, body, link=page(target), label=c["see"]) for title, body, target in c["eco"]])),
    ]
    return {
        "Hero": [hero(c["heading"], c["sub"], c["eyebrow"], art(image), c["alt"], price=c["price"],
                      primary=(c["buy"], page("contact")), secondary=(c["expert"], page("contact")))],
        "Highlights": [jump_links(*c["highlights"])],
        "Sections": sections,
        "Call to action": default_cta(lang),
    }


LANDINGS = {
    "automotive": {
        "en": dict(
            eyebrow="Automotive and transportation",
            heading="3D printing that keeps programmes on schedule",
            benefits_h="Faster from concept to production",
            sub="Validate designs sooner, cut tooling lead times and produce fixtures on demand.",
            benefits=[("End-use and custom parts", "Produce brackets, clips and low-volume parts for prototypes, motorsport and aftermarket programmes."),
                      ("From concept to pre-production", "Check fit and function with realistic parts, and keep sensitive designs inside your organisation."),
                      ("Tools and aids for any supplier", "Reduce overhead with custom jigs and respond quickly to low-volume orders.")],
            save="Save time and money on every iteration",
            save_i="An illustrative comparison for a dashboard vent prototype.",
            columns=["In-house printing", "Outsourcing"],
            rows=[("Time", "24 hours", "8 days"), ("Cost", "€45", "€260")],
            foot="Illustrative figures for a fictional product.",
            quote=("Alpenrad", "Rapid prototyping",
                   "We find the fit problems on Tuesday, fix them on Wednesday and never pay for them in tooling.",
                   "Jonas Weber", "Interior Development Lead", page("alpenrad"), "Read the story"),
            suite="A full suite of printing solutions",
            faq_h="FAQ",
            faqs=[("Which automotive applications can Voxelry printers support?", "Common uses include prototypes, end-use and aftermarket parts, custom jigs and fixtures, and rapid tooling."),
                  ("How quickly does a printer pay for itself?", "That depends on your volume. Compare what you spend on outsourced parts with the running cost of printing in-house."),
                  ("Which printer should an automotive team start with?", "Voxel S1 suits small prototypes and tools, Voxel S1L handles larger parts, and Sinter X produces durable nylon parts.")],
            printers=[("voxel-s1", "Voxel S1", "Maximum versatility for prototypes and small tools."),
                      ("voxel-s1l", "Voxel S1L", "Think big, with room for large prototypes and jigs."),
                      ("sinter-x", "Sinter X", "Durable nylon for functional and end-use parts.")],
            see="See details",
            related="See also",
            alt="Illustration of a printed prototype",
            image="prototype",
        ),
        "de": dict(
            eyebrow="Automobilindustrie und Transport",
            heading="3D-Druck, der Projekte im Zeitplan hält",
            benefits_h="Schneller vom Konzept zur Serie",
            sub="Prüfen Sie Entwürfe früher, verkürzen Sie Werkzeugzeiten und fertigen Sie Vorrichtungen nach Bedarf.",
            benefits=[("Endverbrauchs- und Sonderteile", "Fertigen Sie Halter, Clips und Kleinserien für Prototypen, Motorsport und Aftermarket."),
                      ("Vom Konzept zur Vorserie", "Prüfen Sie Passform und Funktion mit realistischen Teilen und behalten Sie sensible Entwürfe im Haus."),
                      ("Werkzeuge und Hilfsmittel für jeden Zulieferer", "Senken Sie Gemeinkosten mit eigenen Vorrichtungen und reagieren Sie schnell auf Kleinaufträge.")],
            save="Bei jeder Iteration Zeit und Geld sparen",
            save_i="Ein beispielhafter Vergleich für den Prototyp einer Lüftungsdüse.",
            columns=["3D-Druck im Haus", "Fremdvergabe"],
            rows=[("Zeit", "24 Stunden", "8 Tage"), ("Kosten", "45 €", "260 €")],
            foot="Beispielwerte für ein fiktives Produkt.",
            quote=("Alpenrad", "Rapid Prototyping",
                   "Passformprobleme finden wir am Dienstag, beheben sie am Mittwoch und bezahlen nie dafür im Werkzeugbau.",
                   "Jonas Weber", "Leiter Innenraumentwicklung", None, ""),
            suite="Ein komplettes Angebot an Drucklösungen",
            faq_h="Häufige Fragen",
            faqs=[("Welche Anwendungen unterstützen Voxelry-Drucker in der Automobilindustrie?", "Üblich sind Prototypen, Endverbrauchsteile, Vorrichtungen und Rapid Tooling."),
                  ("Wie schnell amortisiert sich ein Drucker?", "Das hängt von Ihrem Volumen ab. Vergleichen Sie Ihre Ausgaben für Fremdteile mit den laufenden Kosten im eigenen Haus."),
                  ("Mit welchem Drucker sollte ein Team beginnen?", "Voxel S1 eignet sich für kleine Prototypen, Voxel S1L für größere Teile und Sinter X für robuste Nylonteile.")],
            printers=[("voxel-s1", "Voxel S1", "Maximale Vielseitigkeit für Prototypen und kleine Werkzeuge."),
                      ("voxel-s1l", "Voxel S1L", "Platz für große Prototypen und Vorrichtungen."),
                      ("sinter-x", "Sinter X", "Robustes Nylon für funktionale Teile und Endverbrauchsteile.")],
            see="Details ansehen",
            related="Weitere Inhalte",
            alt="Illustration eines gedruckten Prototyps",
            image="prototype",
        ),
    },
}


def simple_landing(eyebrow, heading, sub, benefits, image, quote=None, faqs=None):
    automotive = LANDINGS["automotive"]["en"]
    return dict(
        automotive, eyebrow=eyebrow, heading=heading, sub=sub, benefits=benefits, image=image,
        alt=f"Illustration for {eyebrow.lower()}", quote=quote, faqs=faqs or [],
        benefits_h=f"Where {eyebrow.lower()} teams start",
        save="Compare the options", save_i="An illustrative comparison for a typical small batch.",
    )


LANDINGS["manufacturing"] = {"en": simple_landing(
    "Manufacturing", "Keep production lines moving",
    "Make jigs, fixtures and spare parts on demand, on the same day the need appears.",
    [("Jigs and fixtures", "Replace slow machined fixtures with printed versions shaped for the job."),
     ("Spare parts on demand", "Reduce downtime by printing replacements rather than waiting for deliveries."),
     ("Short production runs", "Produce low volumes without the cost of hard tooling.")],
    "aids",
    ("Northline Cycles", "Manufacturing aids",
     "We used to plan around the supplier's calendar. Now we plan around the next test ride.",
     "Ana Kovács", "Head of Engineering", page("northline"), "Read the story"),
)}
LANDINGS["medical"] = {"en": simple_landing(
    "Medical", "Bring research models in-house",
    "Give clinical and research teams quick access to anatomical models and study devices.",
    [("Anatomical models", "Create models from imaging data for planning and education."),
     ("Research devices", "Iterate on study devices with short turnaround times."),
     ("Teaching aids", "Give students and trainees tactile models to learn from.")],
    "models",
    faqs=[("Are these products certified medical devices?", "No. Voxelry is a fictional brand, and nothing on this site is medical guidance.")],
)}
LANDINGS["rapid-prototyping"] = {"en": simple_landing(
    "Rapid prototyping", "See it and test it within a day",
    "Turn ideas into realistic, functional prototypes and bring better products to market sooner.",
    [("Concept exploration", "Print several directions at once and put them on the table."),
     ("Looks-like prototypes", "Review appearance and ergonomics with realistic parts."),
     ("Works-like prototypes", "Test function with engineering-grade materials.")],
    "prototype",
)}
LANDINGS["rapid-tooling"] = {"en": simple_landing(
    "Rapid tooling", "Test the tool before you pay for it",
    "Print molds, patterns and short-run tools in-house and shorten the path to production.",
    [("Injection mold inserts", "Prove out a design in the final material with a low-cost insert."),
     ("Casting patterns", "Produce detailed patterns without carving or machining."),
     ("Thermoforming tools", "Make forming tools in hours for short runs and trials.")],
    "tooling",
)}


def landing_page(key, lang):
    c = LANDINGS[key][lang]
    blocks = [
        section(c["benefits_h"], cards(3, *[card(title, body) for title, body in c["benefits"]])),
        section(c["save"], comparison(c["columns"], c["rows"], c["foot"]), intro=c["save_i"], tone="light"),
    ]
    if c.get("quote"):
        blocks.append(section("", quotes(c["quote"])))
    blocks.append(section(
        c["suite"],
        cards(3, *[card(name, body, image=art(target), alt=f"{name} 3D printer", link=page(target), label=c["see"])
                   for target, name, body in c["printers"]]),
        tone="light",
    ))
    if c.get("faqs"):
        blocks.append(section(c["faq_h"], faq(*c["faqs"])))
    return {
        "Hero": [hero(c["heading"], c["sub"], c["eyebrow"], art(c["image"]), c["alt"],
                      primary=("Vertrieb kontaktieren" if lang == "de" else "Contact sales", page("contact")))],
        "Sections": blocks,
        "Related": [section(c["related"], resources(limit=3, filters=False), tone="light")] if lang == "en" else [],
        "Call to action": default_cta(lang),
    }


def hub(heading, sub, *blocks, lang="en", image=None, alt=""):
    return {
        "Hero": [hero(heading, sub, image=image, alt=alt)],
        "Sections": list(blocks),
        "Call to action": default_cta(lang),
    }


def article(*body, related=True):
    return {
        "Body": [text(block) for block in body],
        "Related": [section("Keep reading", resources(limit=3, filters=False), tone="light")] if related else [],
        "Call to action": default_cta(),
    }


CONTENT = {
    ("home", "en"): home_en,
    ("home", "de"): home_de,
    ("printers", "en"): lambda: hub(
        "Professional 3D printers",
        "Resin for fine detail and smooth surfaces, powder for strong parts and batches.",
        section("All printers", cards(
            3,
            printer_card("voxel-s1", "Voxel S1", "Fast desktop resin printing.", "SLA"),
            printer_card("voxel-s1l", "Voxel S1L", "Large-format resin printing.", "SLA"),
            printer_card("sinter-x", "Sinter X", "Nylon parts without supports.", "SLS"),
        )),
        section("Compare at a glance", comparison(
            ["Voxel S1", "Voxel S1L", "Sinter X"],
            [("Technology", "SLA", "SLA", "SLS"),
             ("Build volume", "200 × 125 × 210 mm", "340 × 200 × 360 mm", "300 × 300 × 350 mm"),
             ("Best for", "Prototypes, small tools", "Large parts, batches", "End-use nylon parts"),
             ("Starting price", "€2,950", "€9,800", "€24,500")],
            "Illustrative figures for fictional products.",
        ), tone="light"),
        image=art("voxel-s1l"), alt="Illustration of a large-format 3D printer",
    ),
    ("printers", "de"): lambda: hub(
        "Professionelle 3D-Drucker",
        "Harz für feine Details und glatte Oberflächen, Pulver für robuste Teile und Serien.",
        section("Alle Drucker", cards(
            3,
            card("Voxel S1", "Schneller Harzdruck auf dem Desktop.", "SLA", art("voxel-s1"), "Voxel S1 3D-Drucker", page("voxel-s1"), "Details ansehen"),
            card("Voxel S1L", "Harzdruck im Großformat.", "SLA", art("voxel-s1l"), "Voxel S1L 3D-Drucker", page("voxel-s1l"), "Details ansehen"),
            card("Sinter X", "Nylonteile ohne Stützstrukturen.", "SLS", art("sinter-x"), "Sinter X 3D-Drucker", page("sinter-x"), "Details ansehen"),
        )),
        lang="de", image=art("voxel-s1l"), alt="Illustration eines großformatigen 3D-Druckers",
    ),
    ("sla", "en"): lambda: hub(
        "SLA 3D printers", "Smooth surfaces and fine detail, from desktop models to large-format parts.",
        section("Choose your size", cards(
            2,
            printer_card("voxel-s1", "Voxel S1", "Fast desktop resin printing.", "SLA"),
            printer_card("voxel-s1l", "Voxel S1L", "The same workflow, with a much larger build volume.", "SLA"),
        )),
        image=art("voxel-s1"), alt="Illustration of a compact resin printer",
    ),
    ("sls", "en"): lambda: hub(
        "SLS 3D printers", "Strong nylon parts with no support structures, ready for end use.",
        section("Our SLS system", cards(2, printer_card("sinter-x", "Sinter X", "Durable nylon parts for functional testing and batches.", "SLS"))),
        image=art("sinter-x"), alt="Illustration of a powder printer",
    ),
    ("post", "en"): lambda: hub(
        "Post-processing", "Consistent cleaning and curing, without standing over the sink.",
        section("Stations", cards(2, printer_card("rinse-cure", "Rinse + Cure Station", "Automated finishing for SLA parts.", "SLA"))),
        image=art("rinse-cure"), alt="Illustration of a post-processing station",
    ),
    ("materials", "en"): lambda: hub(
        "Materials", "Every Voxelry resin and powder in one place. Filter by technology and category.",
        section("", materials()),
        image=art("materials"), alt="Parts printed in several materials",
    ),
    ("materials", "de"): lambda: hub(
        "Materialien", "Alle Harze und Pulver von Voxelry an einem Ort. Filtern Sie nach Technologie und Kategorie.",
        section("", materials()),
        lang="de", image=art("materials"), alt="In verschiedenen Materialien gedruckte Teile",
    ),
    ("software", "en"): lambda: hub(
        "Software", "One workflow from the first file to the last finished part.",
        section("Our tools", cards(
            2,
            card("VoxelPrep", "Prepare models and send them to print.", image=art("software"), alt="Illustration of a print preview", link=page("voxelprep"), label="See details"),
            card("VoxelFleet", "Manage printers, queues and materials.", image=art("workflow"), alt="Illustration of a printer fleet", link=page("voxelfleet"), label="See details"),
        )),
        image=art("software"), alt="Illustration of a print preview",
    ),
    ("solutions", "en"): lambda: hub(
        "Make anything with Voxelry", "Explore by industry or by the job you need to get done.",
        section("By industry", cards(
            3,
            card("Automotive", "Keep vehicle programmes on schedule.", image=art("prototype"), alt="Voxel model of a gear prototype", link=page("automotive"), label="Explore"),
            card("Manufacturing", "Jigs, fixtures and spare parts on demand.", image=art("aids"), alt="Voxel model of an assembly jig", link=page("manufacturing"), label="Explore"),
            card("Medical", "Research models and study devices in-house.", image=art("models"), alt="Voxel anatomical model", link=page("medical"), label="Explore"),
        )),
        section("By use case", cards(
            2,
            card("Rapid prototyping", "See it and test it within a day.", image=art("speed"), alt="Layers of voxels rising in a wave", link=page("rapid-prototyping"), label="Explore"),
            card("Rapid tooling", "Test the tool before you pay for it.", image=art("tooling"), alt="Voxel model of a machined bracket", link=page("rapid-tooling"), label="Explore"),
        ), tone="light"),
        image=art("workflow"), alt="Row of voxel towers",
    ),
    ("industries", "en"): lambda: hub(
        "Industries", "Teams in very different fields use the same printers to move faster.",
        section("Explore", cards(
            3,
            card("Automotive", "Keep vehicle programmes on schedule.", link=page("automotive"), label="Explore"),
            card("Manufacturing", "Jigs, fixtures and spare parts on demand.", link=page("manufacturing"), label="Explore"),
            card("Medical", "Research models and study devices in-house.", link=page("medical"), label="Explore"),
        )),
        image=art("aids"), alt="Voxel model of an assembly jig",
    ),
    ("applications", "en"): lambda: hub(
        "Use cases", "The most common ways teams put a printer to work.",
        section("Explore", cards(
            2,
            card("Rapid prototyping", "See it and test it within a day.", link=page("rapid-prototyping"), label="Explore"),
            card("Rapid tooling", "Test the tool before you pay for it.", link=page("rapid-tooling"), label="Explore"),
        )),
        image=art("tooling"), alt="Voxel model of a machined bracket",
    ),
    ("learn", "en"): lambda: hub(
        "Learn", "Guides, customer stories and news from the Voxelry team.",
        section("Start here", cards(
            3,
            card("Resources", "Filter guides, stories and white papers.", link=page("library"), label="Browse resources"),
            card("Blog", "The latest product and customer news.", link=page("blog"), label="Read the blog"),
            card("Events", "Meet us at a show near you.", link=page("events"), label="See events"),
        )),
        section("Latest", resources(limit=3, filters=False), tone="light"),
        image=art("speed"), alt="Layers of voxels rising in a wave",
    ),
    ("library", "en"): lambda: hub(
        "Resources", "Filter every guide, customer story and white paper by type and industry.",
        section("", resources()),
        image=art("materials"), alt="Parts printed in several materials",
    ),
    ("blog", "en"): lambda: hub(
        "Blog", "Product launches, material news and stories from customers who print in-house.",
        section("", resources(limit=24, filters=False)),
        image=art("speed"), alt="Layers of voxels rising in a wave",
    ),
    ("events", "en"): lambda: hub(
        "Events", "Hold printed parts in your hands and talk to the people who made the printer.",
        section("Upcoming", cards(
            2,
            card("Practice Expo, Budapest", "A fictional trade show. Find us at stand 7.", "March 2027", art("events"), "Voxel model on a trade show stand", page("contact"), "Book a meeting"),
            card("Additive Workshop, Berlin", "A fictional hands-on workshop for new users.", "May 2027", art("office"), "Voxel model of a skyline", page("contact"), "Save a seat"),
        )),
        image=art("events"), alt="Voxel model on a trade show stand",
    ),
    ("sinter-nylon", "en"): lambda: article(
        "<p>PA11 Pro Powder is a new ductile nylon for Sinter X. It is built for parts that need to bend, absorb impact and survive daily handling.</p>"
        "<h2>When to use it</h2><ul><li>Snap fits, clips and living hinges</li><li>Thin-walled ducts and enclosures</li><li>Impact-resistant functional prototypes</li></ul>"
        "<p>Use PA12 when stiffness matters most, and PA11 Pro when a part has to flex without cracking.</p>"
        "<h2>Availability</h2><p>This is a fictional product launch, written as practice content for the blog template.</p>"
    ),
    ("northline", "en"): lambda: article(
        "<p>Northline Cycles is a fictional bicycle maker with a small engineering team. Testing a new frame used to mean waiting weeks for machined fixtures.</p>"
        "<h2>The challenge</h2><p>Every design change restarted the wait, so the team made fewer changes than it wanted to.</p>"
        "<h2>The approach</h2><p>The team now prints fixtures on a Voxel S1 and functional parts on Sinter X.</p>"
        "<blockquote>We used to plan around the supplier's calendar. Now we plan around the next test ride.</blockquote>"
        "<h2>The result</h2><p>A fixture that once took weeks now arrives the next morning, and the team tests more designs in every cycle.</p>"
    ),
    ("alpenrad", "en"): lambda: article(
        "<p>Alpenrad is a fictional German automotive supplier that makes interior components for small-series vehicles.</p>"
        "<h2>The challenge</h2><p>Fit problems found late in a programme are expensive, because each one can mean changing a tool.</p>"
        "<h2>The approach</h2><p>Alpenrad prints interior parts on a Voxel S1L and test-fits them in the vehicle before releasing any tooling.</p>"
        "<blockquote>We find the fit problems on Tuesday, fix them on Wednesday and never pay for them in tooling.</blockquote>"
    ),
    ("harbor", "en"): lambda: article(
        "<p>Harbor Robotics is a fictional start-up that builds pick-and-place robots for small warehouses. "
        "Every robot ends in a gripper, and every gripper needs fingers shaped for the parcels it handles.</p>"
        "<h2>The challenge</h2>"
        "<p>The team used to machine each finger from aluminium. A new customer often meant a new parcel shape, "
        "and a new finger design took two weeks to arrive. Fingers also wore out, so spares had to be ordered in bulk "
        "and kept on a shelf in case a design changed.</p>"
        "<h2>The approach</h2>"
        "<p>Harbor now designs fingers in-house and prints them on a Sinter X in PA11 Pro Powder. The material flexes "
        "enough to grip soft packaging without tearing it, and it does not crack when a robot misjudges a box. "
        "Because SLS needs no support structures, one build holds fingers for several customers, nested together "
        "and printed overnight.</p>"
        "<blockquote>Most of our gripper fingers now start and finish on Sinter X. No one has asked to go back.</blockquote>"
        "<h2>The result</h2>"
        "<p>A new finger design goes from CAD to a test on the robot in two days. Spares are printed when a customer "
        "needs them instead of being stocked. The team still machines the metal wrist that holds the fingers, "
        "and prints everything that touches a parcel.</p>"
        "<p>Harbor Robotics, its people and its figures are invented for this practice site.</p>"
    ),
    ("sla-vs-sls", "en"): lambda: article(
        "<p>Resin (SLA) and powder (SLS) printers both build parts layer by layer, but they solve different problems. "
        "This guide explains how each one works, where each one is the better choice, and how to decide for a "
        "specific part. Start with what the part has to do, not with the printer.</p>",

        "<h2>How SLA works</h2>"
        "<p>Stereolithography (SLA) cures liquid resin with light. In the Voxel S1 and Voxel S1L, a masked light source "
        "hardens a whole layer at once, then the build platform lifts and the next layer is cured. Parts hang from the "
        "platform on thin supports, which are removed after printing. Each part is then rinsed in solvent and post-cured "
        "with heat and light, which the Rinse + Cure Station handles automatically.</p>"
        "<p>Because each layer is cured from a liquid, SLA parts are smooth and very detailed. A 40 µm pixel size reproduces "
        "fine text, thin walls and small features that other processes blur. The range of resins is wide: rigid, tough, "
        "clear, flexible, heat-resistant and glass-filled grades all run on the same printer.</p>",

        "<h2>How SLS works</h2>"
        "<p>Selective laser sintering (SLS) fuses nylon powder with a laser. The Sinter X spreads a thin layer of powder "
        "across the build chamber, the laser melts the cross-section of every part in that layer, and the process repeats. "
        "The unfused powder around the parts holds them in place, so SLS needs no support structures at all.</p>"
        "<p>That has two big effects. Parts can have internal channels, interlocking features and shapes that no support "
        "could reach. And the whole chamber can be filled with parts stacked in three dimensions, which makes SLS well suited "
        "to batches. After printing, the parts are removed from the powder and blasted clean. Most of the unused powder is "
        "sieved and mixed with fresh powder for the next build.</p>",

        "<h2>The differences that matter</h2>"
        "<ul>"
        "<li><strong>Surface finish.</strong> SLA parts come off the printer smooth and ready for paint or polishing. SLS parts "
        "have a slightly grainy, matte surface that hides layer lines but feels textured.</li>"
        "<li><strong>Detail.</strong> SLA holds sharper edges and finer features. SLS is accurate for functional parts, but "
        "very small text or knife-edge details soften.</li>"
        "<li><strong>Strength.</strong> SLS nylon is tough and slightly flexible in every direction, so it survives impact, "
        "fatigue and snap fits. Most SLA resins are stiffer and more brittle, although tough and elastic resins close much of the gap.</li>"
        "<li><strong>Materials.</strong> SLA offers more variety, including clear and heat-resistant resins. SLS offers fewer "
        "materials, mainly PA12, PA11 Pro and TPU, but they are engineering thermoplastics.</li>"
        "<li><strong>Throughput.</strong> An SLA build is limited to the platform area. An SLS build uses the full chamber volume, "
        "so it can produce far more parts in one run.</li>"
        "<li><strong>Workflow and space.</strong> A desktop SLA printer and a finishing station fit in an office. SLS needs room "
        "for powder handling and a separate cleaning step, so it suits a workshop.</li>"
        "<li><strong>Cost.</strong> The Voxel S1 starts at €2,950 and the Sinter X at €24,500. Per part, SLS often becomes the "
        "cheaper option once the chamber is filled regularly.</li>"
        "</ul>",

        "<h2>Choose SLA when</h2>"
        "<ul>"
        "<li>The part has to look right: appearance models, presentation pieces and consumer product prototypes</li>"
        "<li>You need fine detail, such as dental and medical models, jewellery patterns or small connectors</li>"
        "<li>You need a special material, such as a clear housing, a soft gasket or a mold that sees high temperatures</li>"
        "<li>You print one or a few parts at a time and want them the same day</li>"
        "</ul>",

        "<h2>Choose SLS when</h2>"
        "<ul>"
        "<li>The part has to work: brackets, clips, ducts, housings and other functional prototypes</li>"
        "<li>The part will be used, not just tested, such as jigs, fixtures, spare parts and short production runs</li>"
        "<li>The design has internal channels or moving parts printed in one piece</li>"
        "<li>You want to fill a build with dozens of parts and run it overnight</li>"
        "</ul>",

        "<h2>Three examples</h2>"
        "<p><strong>A handheld device housing.</strong> For the first appearance model, use SLA in a grey or clear resin so the "
        "surface can be painted and shown to customers. When the design moves to drop tests and assembly trials, switch to SLS in "
        "PA12 for parts that behave more like the final moulded housing.</p>"
        "<p><strong>An assembly fixture.</strong> A fixture that locates parts on a production line takes knocks every day. SLS in "
        "PA12 is the usual choice. If the fixture has to hold very tight tolerances on a small feature, a glass-filled SLA resin is stiffer.</p>"
        "<p><strong>A batch of 200 clips.</strong> SLS in PA11 Pro, nested in a single build. The clips need to flex without cracking, "
        "and printing them together keeps the cost per part low.</p>",

        "<h2>Questions to ask about your part</h2>"
        "<ol>"
        "<li>Does it need to look finished or work under load?</li>"
        "<li>What is the smallest feature it has?</li>"
        "<li>Does it need a property only one material family offers, such as clarity or ductility?</li>"
        "<li>How many do you need, and how often?</li>"
        "<li>Where will the printer sit, and who will run it?</li>"
        "</ol>"
        "<p>If the answers point both ways, that is common. Many teams use both technologies, with SLA for detailed and visual parts "
        "and SLS for functional parts and batches. VoxelPrep prepares jobs for both printers, so files and habits carry over.</p>"
        "<p>Not sure which fits? Send us a part file and we will print a sample in both technologies so you can compare them side by side.</p>"
        "<p>Voxelry and its products are fictional, and the figures in this guide are illustrative.</p>"
    ),
    ("support", "en"): lambda: {
        "Hero": [hero("How can we help?", "Setup guides, troubleshooting and service plans for your printers.", image=art("aids"), alt="Voxel model of an assembly jig")],
        "Content": [section("Support options", cards(
            3,
            card("Getting started", "Unbox, install and run your first print."),
            card("Troubleshooting", "Diagnose print issues step by step."),
            card("Service plans", "Priority support and replacement cover."),
        ))],
        "Call to action": default_cta(),
    },
    ("contact", "en"): lambda: {
        "Hero": [hero("Contact Voxelry", "This is a practice site, so the sales team is fictional too. In a real build, this page would hold the lead form.", image=art("office"), alt="Voxel model of the Budapest skyline")],
        "Content": [section("Ways to reach us", cards(
            3,
            card("Sales", "Discuss printers, pricing and a demonstration."),
            card("Sample parts", "See and test printed material samples."),
            card("Resellers", "Find or become a local partner."),
        ))],
    },
    ("support", "de"): lambda: {
        "Hero": [hero("Wie können wir helfen?", "Einrichtungsanleitungen, Fehlerbehebung und Servicepläne für Ihre Drucker.", image=art("aids"), alt="Voxel-Modell einer Montagevorrichtung")],
        "Content": [section("Unterstützung", cards(
            3,
            card("Erste Schritte", "Auspacken, einrichten und den ersten Druck starten."),
            card("Fehlerbehebung", "Druckprobleme Schritt für Schritt lösen."),
            card("Servicepläne", "Bevorzugter Support und Ersatzgeräte."),
        ))],
        "Call to action": default_cta("de"),
    },
    ("contact", "de"): lambda: {
        "Hero": [hero("Kontakt zu Voxelry", "Dies ist eine Übungswebsite, daher ist auch das Vertriebsteam fiktiv. Auf einer echten Website stünde hier das Kontaktformular.", image=art("office"), alt="Voxel-Modell der Budapester Skyline")],
        "Content": [section("So erreichen Sie uns", cards(
            3,
            card("Vertrieb", "Sprechen Sie mit uns über Drucker, Preise und eine Vorführung."),
            card("Musterteile", "Sehen und testen Sie gedruckte Materialmuster."),
            card("Händler", "Finden Sie einen Partner in Ihrer Nähe oder werden Sie selbst einer."),
        ))],
    },
    ("about", "en"): lambda: {
        "Hero": [hero("About Voxelry", "A fictional 3D printing brand, created to practise building a multi-language site in django CMS.", image=art("hero"), alt="Abstract city of stacked voxels")],
        "Content": [section("What this project shows", text("<p>Reusable page templates, a block library, localized content, publishing with drafts, and automated content QA. All products, figures, customers and quotes are invented.</p>"))],
    },
    ("privacy", "en"): lambda: {
        "Hero": [hero("Privacy Policy", "This practice site sells nothing and has no marketing trackers.", image=art("office"), alt="Voxel model of a skyline")],
        "Content": [section("Summary", text("<p>The CMS stores login details for its editors and sets the cookies it needs to work. A real site would need a reviewed policy here.</p>"))],
    },
}

for _key in ["voxel-s1", "voxel-s1l", "sinter-x", "rinse-cure", "voxelprep", "voxelfleet"]:
    for _lang in PRODUCTS[_key]:
        CONTENT[(_key, _lang)] = lambda key=_key, lang=_lang: product_page(key, lang)
for _key in LANDINGS:
    for _lang in LANDINGS[_key]:
        CONTENT[(_key, _lang)] = lambda key=_key, lang=_lang: landing_page(key, lang)


def link_list(title, *links):
    return ("LinkListPlugin", {"title": title}, [
        ("LinkItemPlugin", {"label": label, "link": target}, []) for label, target in links
    ])


FOOTER = {
    "en": [
        link_list("3D Printers", ("Voxel S1", page("voxel-s1")), ("Voxel S1L", page("voxel-s1l")), ("Sinter X", page("sinter-x")), ("Rinse + Cure Station", page("rinse-cure"))),
        link_list("Materials and software", ("All materials", page("materials")), ("VoxelPrep", page("voxelprep")), ("VoxelFleet", page("voxelfleet"))),
        link_list("Learn", ("Applications", page("solutions")), ("Blog", page("blog")), ("Resources", page("library")), ("Events", page("events"))),
        link_list("Company", ("About", page("about")), ("Support", page("support")), ("Contact", page("contact")), ("Privacy Policy", page("privacy"))),
    ],
    "de": [
        link_list("3D-Drucker", ("Voxel S1", page("voxel-s1")), ("Voxel S1L", page("voxel-s1l")), ("Sinter X", page("sinter-x")), ("Rinse + Cure Station", page("rinse-cure"))),
        link_list("Materialien und Software", ("Alle Materialien", page("materials")), ("VoxelPrep", page("voxelprep")), ("VoxelFleet", page("voxelfleet"))),
        link_list("Wissen", ("Anwendungen", page("solutions")), ("Blog", page("blog")), ("Ressourcen", page("library")), ("Veranstaltungen", page("events"))),
        link_list("Unternehmen", ("Über uns", page("about")), ("Support", page("support")), ("Kontakt", page("contact")), ("Datenschutz", page("privacy"))),
    ],
}

# name (en), name (de), description (en), description (de), technology, category, tensile, elongation, price
MATERIALS = [
    ("Everyday Grey Resin", "Everyday Grey Harz", "A dependable default for models and concept parts.", "Eine zuverlässige Wahl für Modelle und Konzeptteile.", "sla", "general-purpose", 62, 6, "79.00"),
    ("Crystal Clear Resin", "Crystal Clear Harz", "Polishes to near-optical clarity for light pipes and housings.", "Lässt sich für Lichtleiter und Gehäuse nahezu glasklar polieren.", "sla", "general-purpose", 58, 7, "89.00"),
    ("Tough 2K Resin", "Tough 2K Harz", "An ABS-like resin for parts that need to take a knock.", "Ein ABS-ähnliches Harz für stark beanspruchte Teile.", "sla", "impact-resistant", 46, 48, "129.00"),
    ("Stiff 10G Resin", "Stiff 10G Harz", "Glass-filled and very rigid, for tools and jigs.", "Glasgefüllt und sehr steif, für Werkzeuge und Vorrichtungen.", "sla", "high-stiffness", 88, 2, "169.00"),
    ("HeatShield Resin", "HeatShield Harz", "Holds its shape in molds and hot-air testing.", "Bleibt in Formen und bei Heißlufttests formstabil.", "sla", "temperature-resistant", 70, 3, "189.00"),
    ("Flex 70A Resin", "Flex 70A Harz", "Soft and elastic, for gaskets and overmold prototypes.", "Weich und elastisch, für Dichtungen und Prototypen.", "sla", "elastomeric", 8, 140, "169.00"),
    ("Bio Model Resin", "Bio Model Harz", "A fictional resin for research and teaching models.", "Ein fiktives Harz für Forschungs- und Lehrmodelle.", "sla", "medical", 54, 5, "229.00"),
    ("PA12 Powder", "PA12 Pulver", "The general-purpose nylon for functional parts.", "Das Allzweck-Nylon für funktionale Teile.", "sls", "general-purpose", 50, 11, "95.00"),
    ("PA11 Pro Powder", "PA11 Pro Pulver", "A ductile nylon for snap fits and living hinges.", "Ein duktiles Nylon für Schnappverbindungen und Scharniere.", "sls", "impact-resistant", 47, 45, "119.00"),
    ("TPU 90A Powder", "TPU 90A Pulver", "Flexible, supportless parts with strong rebound.", "Flexible Teile ohne Stützen mit starker Rückstellung.", "sls", "elastomeric", 9, 110, "139.00"),
]
