#!/usr/bin/env python3
"""
Build the SEO pages for deltapharma.com.pk from the product list in index.html.

Run from the repository root whenever a product, price or photo changes:

    python tools/build_pages.py

It reads the `product-data` JSON block in index.html (the same data the
homepage popup uses) and writes:

    products/index.html            all products, grouped by dosage form
    products/<name>/index.html     one page per product (33 pages)
    sitemap.xml                    every page, with product photos
    robots.txt                     lets search engines crawl everything
    404.html                       "page not found" page

Only the Python standard library is used.
"""
import html
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://deltapharma.com.pk"
CSS_V = "9"  # keep in step with styles.css?v= in index.html
JS_V = "8"   # keep in step with main.js?v= in index.html
TODAY = date.today().isoformat()

CATEGORY_SLUG = {"Tablets": "tablets", "Capsules": "capsules", "Syrup": "syrup", "Dry Suspension": "dry-suspension"}
CATEGORY_TITLE = {"Tablets": "Tablets", "Capsules": "Capsules", "Syrup": "Syrups & oral suspensions", "Dry Suspension": "Dry suspensions"}
CONTAINS_LABEL = {"Tablets": "Each tablet contains", "Capsules": "Each capsule contains"}

# Other spellings people search for (as listed by Pakistani pharmacy sites).
ALSO_LISTED_AS = {"Levetazet": "Levatazet"}

ICONS = {
    "Tablets": '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill-rule="evenodd" d="M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18ZM6 11v2h12v-2H6Z"/></svg>',
    "Capsules": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4.2 13.4a5 5 0 0 1 7.1-7.1l6.4 6.4a5 5 0 0 1-7.1 7.1l-6.4-6.4Zm1.4-5.7a3 3 0 0 0 0 4.3l3 3 4.3-4.3-3-3a3 3 0 0 0-4.3 0Z"/></svg>',
    "Syrup": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 2h6v3h-1v2.1A5 5 0 0 1 18 12v8a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2v-8a5 5 0 0 1 4-4.9V5H9V2Zm-1 12v4h8v-4H8Z"/></svg>',
    "Dry Suspension": '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill-rule="evenodd" d="M8 3h8v3l-1 1v2h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-9a2 2 0 0 1 2-2h2V7L8 6V3Zm1 11a1 1 0 1 0 2 0 1 1 0 0 0-2 0Zm4 1a1 1 0 1 0 2 0 1 1 0 0 0-2 0Zm-3 3a1 1 0 1 0 2 0 1 1 0 0 0-2 0Z"/></svg>',
}

e = html.escape


def slug(name):
    """'Excip 500 mg' -> 'excip-500mg'. Must match slug() in js/products.js."""
    s = name.lower().replace(" mg/5 ml", "mg-5ml").replace(" mg", "mg")
    s = re.sub(r"(\d)\.(\d)", r"\1-\2", s)
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def generic(p):
    """Short ingredient name(s) for titles: 'Ciprofloxacin', 'Paracetamol + Caffeine'."""
    if p["name"].startswith("Delvitis"):
        return "11 vitamins"
    names = []
    for ing, _ in p["composition"]:
        if ing.startswith("equivalent to"):
            continue
        n = re.sub(r"\s*\(.*?\)", "", ing).split(",")[0].strip()
        n = n.replace(" hydroxide polymaltose complex", " polymaltose")
        n = re.sub(r"\s+(HCl|hydrochloride)$", "", n)
        n = n.replace("Piroxicam beta-cyclodextrin", "Piroxicam")
        names.append(n)
    return " + ".join(names)


def form_word(p):
    f = p["form"].lower()
    if "suspension" in f and "powder" in f:
        return "Dry Suspension"
    if "capsule" in f:
        return "Capsules"
    if "tablet" in f:
        return "Tablets"
    if "suspension" in f:
        return "Suspension"
    return "Syrup"


def img(name):
    return f"/assets/images/products/{name}.jpg"


def load_products():
    src = (ROOT / "index.html").read_text(encoding="utf-8")
    m = re.search(r'<script type="application/json" id="product-data">(.*?)</script>', src, re.S)
    products = json.loads(m.group(1))
    for p in products:
        p["slug"] = slug(p["name"])
        p["url"] = f"/products/{p['slug']}/"
        p["generic"] = generic(p)
        p["brand"] = re.split(r"\s(?=\d)|\s(?:Suspension|Dry|Syrup|Forte|Extra|Multivitamin|CR|FA)\b", p["name"])[0]
    return products


# ------------------------------------------------------------------ layout

def head(title, description, canonical, og_image, jsonld=None, noindex=False):
    robots = '\n  <meta name="robots" content="noindex">' if noindex else ""
    canon = f'\n  <link rel="canonical" href="{SITE}{canonical}">' if canonical else ""
    ld = ""
    if jsonld:
        ld = '\n  <script type="application/ld+json">\n' + json.dumps(jsonld, indent=2, ensure_ascii=False) + "\n  </script>"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)}</title>
  <meta name="description" content="{e(description)}">{canon}{robots}
  <meta name="theme-color" content="#102F67">

  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Delta Pharma (Pvt.) Limited">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(description)}">
  <meta property="og:url" content="{SITE}{canonical or '/'}">
  <meta property="og:image" content="{SITE}{og_image}">
  <meta property="og:locale" content="en_PK">
  <meta name="twitter:card" content="summary_large_image">

  <link rel="icon" href="/favicon.ico?v=2" sizes="16x16 32x32 48x48">
  <link rel="apple-touch-icon" href="/assets/images/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700&family=Open+Sans:wght@400;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/styles.css?v={CSS_V}">{ld}
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>

  <header class="site-header" id="top">
    <div class="container header-inner">
      <a href="/" class="brand" aria-label="Delta Pharma – go to Home" title="Home">
        <img src="/assets/images/delta-pharma-logo-trim.jpg" alt="Delta Pharma (Pvt.) Limited" width="950" height="576">
      </a>

      <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav" aria-label="Open menu">
        <span></span><span></span><span></span>
      </button>

      <nav class="site-nav" id="site-nav" aria-label="Main">
        <ul>
          <li><a href="/" class="nav-link">Home</a></li>
          <li><a href="/#about" class="nav-link">About</a></li>
          <li><a href="/#leadership" class="nav-link">Leadership</a></li>
          <li><a href="/#quality" class="nav-link">Quality</a></li>
          <li><a href="/products/" class="nav-link">Products</a></li>
          <li><a href="/#why-us" class="nav-link">Why Delta</a></li>
          <li><a href="/#contact" class="button button-primary nav-cta">Contact us</a></li>
        </ul>
      </nav>
    </div>
  </header>
"""


FOOT = f"""
  <footer class="site-footer">
    <div class="container footer-inner">
      <div class="footer-brand">
        <div class="footer-logo">
          <img src="/assets/images/delta-pharma-logo-trim.jpg" alt="Delta Pharma (Pvt.) Limited" width="950" height="576" loading="lazy">
        </div>
        <div>
          <p>Quality. Science. Trust.</p>
          <address class="footer-address">Plot No. 9 (SIZ), Nowshera Industrial Estate, Risalpur, Nowshera, Khyber Pakhtunkhwa, Pakistan<br>
            <a href="tel:+92937842655">0937-842655</a> · <a href="tel:+923439104456">0343-9104456</a><br>
            Licence to Manufacture No. 000446</address>
        </div>
      </div>
      <nav class="footer-nav" aria-label="Footer">
        <a href="/">Home</a>
        <a href="/#about">About</a>
        <a href="/#leadership">Leadership</a>
        <a href="/#quality">Quality</a>
        <a href="/products/">Products</a>
        <a href="/#contact">Contact</a>
      </nav>
    </div>
    <div class="container footer-bottom">
      <small>© <span id="year">{date.today().year}</span> Delta Pharma (Pvt.) Limited. All rights reserved.</small>
      <a href="#top" class="back-to-top">Back to top ↑</a>
    </div>
  </footer>

  <script src="/js/main.js?v={JS_V}" defer></script>
</body>
</html>
"""

NOTE = ('<p class="product-note">Product information is provided for healthcare professionals, distributors and franchise '
        'partners. Use medicines only as prescribed by a registered medical practitioner. M.R.P. in Pakistani rupees, '
        'subject to change.</p>')


def breadcrumb_html(items):
    lis = []
    for name, url in items:
        lis.append(f'<li><a href="{url}">{e(name)}</a></li>' if url else f'<li aria-current="page">{e(name)}</li>')
    return '<nav class="breadcrumb" aria-label="Breadcrumb"><ol>' + "".join(lis) + "</ol></nav>"


def breadcrumb_ld(items):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, **({"item": SITE + url} if url else {})}
            for i, (name, url) in enumerate(items)
        ],
    }


ORG_REF = {"@id": f"{SITE}/#organization"}
ORG_LD = {
    "@type": "Organization",
    "@id": f"{SITE}/#organization",
    "name": "Delta Pharma (Pvt.) Limited",
    "url": f"{SITE}/",
    "logo": f"{SITE}/assets/images/delta-pharma-logo.jpg",
}


def card(p, heading="h3"):
    if p["images"]:
        media = (f'<img src="{img(p["images"][0])}" alt="{e(p["name"])} ({e(p["generic"])}) pack, Delta Pharma" '
                 f'width="900" height="675" loading="lazy">')
        if len(p["images"]) > 1:
            media += f'<span class="product-more">{len(p["images"])} photos</span>'
    else:
        media = (f'<span class="product-noimg">{ICONS[p["category"]]}<b>{e(p["name"])}</b>'
                 f'<small>Photo coming soon</small></span>')
    meta = f'<span>{e(p["pack"]) or "&nbsp;"}</span><span>{"Rs " + str(int(float(p["mrp"]))) if p["mrp"] else ""}</span>'
    return f"""<li><a class="product" href="{p['url']}">
            <span class="product-media">{media}</span>
            <span class="product-body">
              <span class="product-form">{e(p['form'])}</span>
              <span class="product-name">{e(p['name'])}</span>
              <span class="product-generic">{e(p['composition'][0][0]) if not p['name'].startswith('Delvitis') else '11 vitamins'}</span>
              <span class="product-meta">{meta}</span>
            </span>
          </a></li>"""


# ------------------------------------------------------------------ pages

def product_page(p, products):
    cat = p["category"]
    fw = form_word(p)
    title = f"{p['name']} ({p['generic']}) {fw if fw not in p['name'] else ''}".replace("  ", " ").strip()
    title = f"{title} | Delta Pharma Pakistan"
    pack = f", pack of {p['pack']}" if p["pack"] else ""
    price = f", M.R.P. Rs {p['mrp'].replace('.00', '')}" if p["mrp"] else ""
    desc = (f"{p['name']}: {p['generic']} {p['form'].lower()}{pack}{price}. {p['cls']}. "
            f"Manufactured by Delta Pharma (Pvt.) Ltd., Nowshera, Pakistan. DRAP Reg. No. {p['reg']}.")
    crumbs = [("Home", "/"), ("Products", "/products/"), (CATEGORY_TITLE[cat], f"/products/#{CATEGORY_SLUG[cat]}"), (p["name"], None)]

    images = p["images"]
    if images:
        main = f'<img src="{img(images[0])}" alt="{e(p["name"])} ({e(p["generic"])}) pack, front, Delta Pharma" width="900" height="675">'
        thumbs = "".join(
            f'<a href="{img(im)}"><img src="{img(im)}" alt="{e(p["name"])} pack, photo {k + 2}" width="900" height="675" loading="lazy"></a>'
            for k, im in enumerate(images[1:])
        )
        thumbs = f'<div class="pp-thumbs">{thumbs}</div>' if thumbs else ""
    else:
        main = f'<span class="product-noimg">{ICONS[cat]}<b>{e(p["name"])}</b><small>Photo coming soon</small></span>'
        thumbs = ""

    comp = "".join(f"<li><span>{e(a)}</span><span>{e(b)}</span></li>" for a, b in p["composition"])
    spec_word = p["spec"] + ("" if p["spec"].startswith("International") else " specification")
    specs = [
        ("Dosage form", p["form"]),
        ("Pack size", p["pack"] or "On request"),
        ("Specification", spec_word),
        ("DRAP registration no.", p["reg"]),
        ("M.R.P.", f"Rs {p['mrp']}" if p["mrp"] else "On request"),
        ("Category", cat),
    ]
    specs_html = "".join(f"<div><dt>{e(a)}</dt><dd>{e(b)}</dd></div>" for a, b in specs)

    aka = ""
    for k, v in ALSO_LISTED_AS.items():
        if p["name"].startswith(k):
            aka = f'<p class="pp-aka">Also listed by pharmacies as {e(p["name"].replace(k, v))}.</p>'

    wa_text = f"Hello Delta Pharma, I would like to enquire about {p['name']}."
    wa = "https://wa.me/923439104456?text=" + re.sub(r"[^A-Za-z0-9.\-]", lambda m: "%%%02X" % ord(m.group(0)), wa_text)

    # Related: same brand first, then others in the same category
    same_brand = [q for q in products if q is not p and q["brand"] == p["brand"]]
    same_cat = [q for q in products if q is not p and q not in same_brand and q["category"] == cat]
    related = (same_brand + same_cat)[:4]
    related_html = "\n          ".join(card(q) for q in related)

    drug = {
        "@type": "Drug",
        "@id": f"{SITE}{p['url']}#drug",
        "name": p["name"],
        "url": f"{SITE}{p['url']}",
        "description": f"{p['cls']}. {p['form']}.",
        "nonProprietaryName": p["generic"],
        "activeIngredient": [f"{a} {b}" for a, b in p["composition"] if not a.startswith("equivalent to")],
        "dosageForm": p["form"],
        "administrationRoute": "Oral",
        "manufacturer": ORG_REF,
        "identifier": {"@type": "PropertyValue", "propertyID": "DRAP Registration No.", "value": p["reg"]},
    }
    if images:
        drug["image"] = [SITE + img(im) for im in images]
    ld = {"@context": "https://schema.org", "@graph": [drug, breadcrumb_ld(crumbs), ORG_LD]}

    body = f"""
  <main id="main">
    <section class="page-intro">
      <div class="container">
        {breadcrumb_html(crumbs)}
        <p class="eyebrow">{e(p['form'])}</p>
        <h1>{e(p['name'])}</h1>
        <p class="lead">{e(p['generic'])} · {e(p['cls'])}</p>
      </div>
    </section>

    <section class="section">
      <div class="container pp-layout">
        <div class="pp-gallery">
          <div class="pp-main">{main}</div>
          {thumbs}
        </div>
        <div class="pp-info">
          {aka}
          <p class="pd-label">{CONTAINS_LABEL.get(cat, 'Composition')}</p>
          <ul class="pd-composition">{comp}</ul>
          <dl class="pd-specs">{specs_html}</dl>
          <p class="caption">Dispense on prescription. Store as directed on the pack, out of reach of children.
            Manufactured by Delta Pharma (Pvt.) Limited, Nowshera, Khyber Pakhtunkhwa, Pakistan.</p>
          <h2>Order or enquire</h2>
          <p>Distributors, pharmacies and hospitals can order {e(p['name'])} directly from Delta Pharma.</p>
          <div class="pp-cta">
            <a class="button button-primary" href="{wa}" target="_blank" rel="noopener">Enquire on WhatsApp <span aria-hidden="true">→</span></a>
            <a class="button button-ghost" href="tel:+92937842655">Call 0937-842655</a>
          </div>
        </div>
      </div>
    </section>

    <section class="section section-mist pp-related">
      <div class="container">
        <h2>Related products</h2>
        <ul class="product-grid">
          {related_html}
        </ul>
        <p class="product-pages-link"><a href="/products/" class="text-link">See all 33 products <span aria-hidden="true">→</span></a></p>
        {NOTE}
      </div>
    </section>
  </main>
"""
    og = img(images[0]) if images else "/assets/images/delta-pharma-logo.jpg"
    return head(title, desc, p["url"], og, ld) + body + FOOT


def catalogue_page(products):
    crumbs = [("Home", "/"), ("Products", None)]
    groups = []
    for cat in CATEGORY_SLUG:
        items = [p for p in products if p["category"] == cat]
        cards = "\n          ".join(card(p) for p in items)
        groups.append(f"""<div class="product-group" id="{CATEGORY_SLUG[cat]}">
          <h2 class="product-group-title">{CATEGORY_TITLE[cat]} <span>{len(items)} products</span></h2>
          <ul class="product-grid">
          {cards}
          </ul>
        </div>""")
    jump = "".join(f'<a href="#{CATEGORY_SLUG[c]}">{CATEGORY_TITLE[c]}</a>' for c in CATEGORY_SLUG)
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "CollectionPage",
                "@id": f"{SITE}/products/",
                "name": "Delta Pharma products",
                "url": f"{SITE}/products/",
                "publisher": ORG_REF,
                "mainEntity": {
                    "@type": "ItemList",
                    "numberOfItems": len(products),
                    "itemListElement": [
                        {"@type": "ListItem", "position": i + 1, "url": SITE + p["url"], "name": p["name"]}
                        for i, p in enumerate(products)
                    ],
                },
            },
            breadcrumb_ld(crumbs),
            ORG_LD,
        ],
    }
    body = f"""
  <main id="main">
    <section class="page-intro">
      <div class="container">
        {breadcrumb_html(crumbs)}
        <p class="eyebrow">Our products</p>
        <h1>Delta Pharma products</h1>
        <p class="lead">{len(products)} registered medicines made in Nowshera, Pakistan: tablets, capsules, syrups and dry suspensions. Select a product for its composition, pack size, DRAP registration number and M.R.P.</p>
        <nav class="category-jump" aria-label="Jump to dosage form">{jump}</nav>
      </div>
    </section>

    <section class="section">
      <div class="container product-catalogue-static">
        {chr(10).join(groups)}
        {NOTE}
      </div>
    </section>
  </main>
"""
    title = "Products – Tablets, Capsules, Syrups & Dry Suspensions | Delta Pharma Pakistan"
    desc = (f"All {len(products)} registered medicines from Delta Pharma (Pvt.) Ltd., Nowshera: antibiotics such as Excip, "
            "Levetazet, D-Zeth and Reloxidel, plus Delmol, Eso-Del, Karzole and more, with composition, pack size and M.R.P.")
    return head(title, desc, "/products/", "/assets/images/delta-pharma-logo.jpg", ld) + body + FOOT


def not_found_page():
    body = """
  <main id="main">
    <section class="notfound">
      <div class="container">
        <p class="eyebrow">Error 404</p>
        <h1>This page could not be found.</h1>
        <p class="lead" style="margin: 0 auto;">The address may be mistyped, or the page may have moved.</p>
        <div class="hero-actions">
          <a href="/products/" class="button button-primary">Browse our products <span aria-hidden="true">→</span></a>
          <a href="/" class="button button-ghost">Go to the homepage</a>
        </div>
      </div>
    </section>
  </main>
"""
    return head("Page not found | Delta Pharma", "This page could not be found.", None,
                "/assets/images/delta-pharma-logo.jpg", noindex=True) + body + FOOT


def sitemap(products):
    def url(loc, priority, images=()):
        ims = "".join(f"\n    <image:image><image:loc>{SITE}{i}</image:loc></image:image>" for i in images)
        return f"  <url>\n    <loc>{SITE}{loc}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <priority>{priority}</priority>{ims}\n  </url>"
    rows = [
        url("/", "1.0", ["/assets/images/delta-pharma-logo.jpg"]),
        url("/products/", "0.9"),
    ]
    rows += [url(p["url"], "0.8", [img(i) for i in p["images"]]) for p in products]
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
            '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
            + "\n".join(rows) + "\n</urlset>\n")


ROBOTS = f"""User-agent: *
Allow: /
Disallow: /tools/
# Licence document: shown only through the footer "Document verification" flow
Disallow: /assets/images/v/

Sitemap: {SITE}/sitemap.xml
"""


def main():
    products = load_products()
    slugs = [p["slug"] for p in products]
    assert len(set(slugs)) == len(slugs), "two products share a page address"

    out = ROOT / "products"
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text(catalogue_page(products), encoding="utf-8")
    for p in products:
        d = out / p["slug"]
        d.mkdir(exist_ok=True)
        (d / "index.html").write_text(product_page(p, products), encoding="utf-8")
    (ROOT / "404.html").write_text(not_found_page(), encoding="utf-8")
    (ROOT / "sitemap.xml").write_text(sitemap(products), encoding="utf-8")
    (ROOT / "robots.txt").write_text(ROBOTS, encoding="utf-8")
    print(f"Built {len(products)} product pages, products/index.html, 404.html, sitemap.xml, robots.txt")


if __name__ == "__main__":
    main()
