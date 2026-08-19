#!/usr/bin/env python3
"""
Static site generator for SG Flight School.

Content lives in content/*.py (one dict per page). Shared chrome (header, nav,
footer, schema) lives here. Run `python3 build.py` to regenerate site/*.html.
"""
import datetime
import glob
import hashlib
import html
import json
import os
import re
import shutil

from siteconfig import SITE, address_html, phone_html

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "site")

CSS_SRC = os.path.join(OUT, "assets", "css", "style.css")

# Filled in by hash_css(). The stylesheet is served with a one-year immutable
# cache header, so its filename must change whenever its contents do — otherwise
# edge caches and returning visitors keep the old CSS indefinitely.
CSS_HREF = "/assets/css/style.css"


EXTERNAL_A = re.compile(r'<a\b([^>]*?)href="(https?://[^"]+)"([^>]*)>', re.I)

# "sgflightschool.com" — used to tell our own absolute links from off-site ones.
OWN_HOST = re.sub(r"^https?://(www\.)?", "", SITE["url"]).rstrip("/")


def external_new_tab(html_text):
    """Make every off-site link open in a new tab.

    Keeps visitors on the site when they follow a booking, shop or reference
    link. rel="noopener noreferrer" is required alongside target="_blank" —
    without noopener the opened page gets a handle on this one via
    window.opener. Applied as a build pass so new links are covered
    automatically rather than relying on each one being written correctly.
    """
    count = 0

    def fix(m):
        nonlocal count
        pre, url, post = m.group(1), m.group(2), m.group(3)
        if OWN_HOST in url:                   # our own absolute links
            return m.group(0)
        attrs = pre + post
        if 'target=' in attrs:
            return m.group(0)
        count += 1
        # Replace any existing rel with the full safe set.
        pre = re.sub(r'\s*rel="[^"]*"', "", pre)
        post = re.sub(r'\s*rel="[^"]*"', "", post)
        return (f'<a{pre}href="{url}"{post} target="_blank" '
                f'rel="noopener noreferrer">')

    return EXTERNAL_A.sub(fix, html_text), count


def check_function_constants():
    """Fail the build if functions/api/book.js has drifted from siteconfig.

    The Pages Function can't import siteconfig.py, so the phone number and email
    are duplicated there. Without this check, changing the phone number in one
    place would silently leave the confirmation emails quoting the old one.
    """
    fn = os.path.join(ROOT, "functions", "api", "book.js")
    if not os.path.exists(fn):
        return
    src = open(fn, encoding="utf-8").read()
    problems = []
    for label, pattern, expected in (
        ("PHONE", r'const PHONE = "([^"]+)"', SITE["phone_display"]),
        ("TO", r'const TO = "([^"]+)"', SITE["email"]),
    ):
        m = re.search(pattern, src)
        if not m:
            problems.append(f"{label} not found in book.js")
        elif m.group(1) != expected:
            problems.append(
                f"{label} in book.js is {m.group(1)!r} but siteconfig says "
                f"{expected!r}"
            )
    if problems:
        print("\n*** functions/api/book.js is out of sync with siteconfig.py ***")
        for p in problems:
            print("   ", p)
        print("    Update the constants at the top of book.js, then redeploy.\n")
        raise SystemExit(1)


def hash_css():
    """Write a content-hashed copy of style.css and return its href."""
    global CSS_HREF
    with open(CSS_SRC, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()[:10]
    name = f"style.{digest}.css"
    dest = os.path.join(os.path.dirname(CSS_SRC), name)
    if not os.path.exists(dest):
        shutil.copyfile(CSS_SRC, dest)
    # drop superseded hashed copies
    for old in glob.glob(os.path.join(os.path.dirname(CSS_SRC), "style.*.css")):
        if os.path.basename(old) != name:
            os.remove(old)
    CSS_HREF = "/assets/css/" + name
    return CSS_HREF

NAV = [
    ("/courses", "Courses"),
    ("/getting-started", "Getting Started"),
    ("/aircraft", "Aircraft"),
    ("/instructors", "Instructors"),
    ("/faq", "FAQ"),
    ("/ferry-service", "Ferry Service"),
    ("/about", "About"),
    ("/contact", "Contact"),
]

FOOTER_TRAINING = [
    ("/courses", "Discovery Flight"),
    ("/courses", "Private Pilot (PPL)"),
    ("/courses", "Instrument Rating (IFR)"),
    ("/courses", "Commercial (CPL)"),
    ("/courses", "Flight Instructor (CFI)"),
]

FOOTER_MORE = [
    ("/getting-started", "How to Start"),
    ("/cost-of-private-pilot-license-arizona", "What It Costs"),
    ("/faq", "Questions & Answers"),
    ("/falcon-field", "About Falcon Field"),
    ("/faa-medical-exam", "FAA Medical Exam"),
    ("/aircraft", "Our Fleet"),
    ("/ferry-service", "Aircraft Ferry Service"),
    (SITE["shop_url"], "Buy SG Flight School Gear"),
    (SITE["schedule_url"], "Student Login (FlightCircle)"),
]

# City pages. Linked from every page's footer so they get crawled — orphaned
# pages sitting only in the sitemap tend to be ignored.
FOOTER_AREAS = [
    ("/flight-school-gilbert-az", "Gilbert"),
    ("/flight-school-scottsdale-az", "Scottsdale"),
    ("/flight-school-chandler-az", "Chandler"),
    ("/flight-school-tempe-az", "Tempe"),
    ("/flight-school-phoenix-az", "Phoenix"),
]


# ---------------------------------------------------------------- structured data
def local_business_schema():
    return {
        "@context": "https://schema.org",
        "@type": ["LocalBusiness", "EducationalOrganization"],
        "@id": SITE["url"] + "/#organization",
        "name": SITE["name"],
        "description": (
            "Flight school at Falcon Field Airport in Mesa, Arizona offering "
            "discovery flights, private pilot, instrument, commercial and CFI "
            "training, plus nationwide aircraft ferry service."
        ),
        "url": SITE["url"],
        "logo": SITE["url"] + "/assets/img/logo.webp",
        "image": SITE["url"] + "/assets/img/az-aerial.webp",
        "email": SITE["email"],
        "telephone": SITE["phone_display"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": SITE["street"],
            "addressLocality": SITE["city"],
            "addressRegion": SITE["state"],
            "postalCode": SITE["zip"],
            "addressCountry": "US",
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": SITE["lat"],
            "longitude": SITE["lon"],
        },
        "areaServed": [
            {"@type": "City", "name": "Mesa"},
            {"@type": "City", "name": "Phoenix"},
            {"@type": "City", "name": "Scottsdale"},
            {"@type": "City", "name": "Gilbert"},
            {"@type": "City", "name": "Chandler"},
            {"@type": "City", "name": "Tempe"},
        ],
        "sameAs": [SITE["instagram_url"], SITE["facebook_url"]],
    }


# ---------------------------------------------------------------- template
def render(page):
    slug = page["slug"]
    path = "/" if slug == "index" else "/" + slug
    canonical = SITE["url"] + ("" if slug == "index" else path)
    title = page["title"]
    full_title = title if slug == "index" else f"{title} | {SITE['name']}"

    nav_items = "".join(
        '<a href="{href}"{cur}>{label}</a>'.format(
            href=href,
            label=html.escape(label),
            cur=' aria-current="page"' if href == path else "",
        )
        for href, label in NAV
    )

    blocks = [local_business_schema()]
    blocks.extend(page.get("schema", []))
    schema_tags = "\n".join(
        '  <script type="application/ld+json">%s</script>'
        % json.dumps(b, separators=(",", ":"))
        for b in blocks
    )

    footer_training = "".join(
        f'<li><a href="{h}">{html.escape(l)}</a></li>' for h, l in FOOTER_TRAINING
    )
    footer_more = "".join(
        f'<li><a href="{h}">{html.escape(l)}</a></li>' for h, l in FOOTER_MORE
    )
    footer_areas = " &middot; ".join(
        f'<a href="{h}">Flight training in {html.escape(l)}</a>'
        for h, l in FOOTER_AREAS
    )

    page_scripts = "".join(
        f'<script src="{src}" defer></script>' for src in page.get("scripts", [])
    )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{html.escape(full_title)}</title>
  <meta name="description" content="{html.escape(page['description'])}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:site_name" content="{SITE['name']}">
  <meta property="og:title" content="{html.escape(full_title)}">
  <meta property="og:description" content="{html.escape(page['description'])}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:type" content="website">
  <meta property="og:image" content="{SITE['url']}/assets/img/{page.get('og_image', 'az-aerial.webp')}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#0093c4">
  <link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
  <link rel="preload" as="image" href="/assets/img/{page.get('og_image', 'az-aerial.webp')}">
  <link rel="stylesheet" href="{CSS_HREF}">
{schema_tags}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

<div class="callbar">
  <div class="wrap">
    <span>Falcon Field Airport (KFFZ) &middot; Mesa, AZ</span>
    <span>Call {phone_html()}</span>
    <span><a href="mailto:{SITE['email']}">{SITE['email']}</a></span>
    <span class="callbar__shop"><a href="{SITE['shop_url']}" rel="noopener">
      <svg viewBox="0 0 24 24" width="15" height="15" aria-hidden="true" focusable="false">
        <path d="M6 8h12l-1 12H7L6 8z" fill="none" stroke="currentColor"
              stroke-width="1.9" stroke-linejoin="round"/>
        <path d="M9.2 9.5V6.6a2.8 2.8 0 0 1 5.6 0v2.9" fill="none"
              stroke="currentColor" stroke-width="1.9" stroke-linecap="round"/>
      </svg>Buy SG Flight School Gear</a></span>
  </div>
</div>

<header class="site-header">
  <div class="wrap">
    <a class="logo" href="/"><img src="/assets/img/logo.webp" width="500" height="172"
         alt="{SITE['name']} home"></a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="nav" aria-label="Menu">&#9776;</button>
    <nav class="nav" id="nav" aria-label="Main">
      {nav_items}
      <a class="ig" href="{SITE['instagram_url']}" rel="noopener"
         aria-label="{SITE['name']} on Instagram ({SITE['instagram_handle']})"
         title="Follow us on Instagram">
        <svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true" focusable="false">
          <rect x="2.5" y="2.5" width="19" height="19" rx="5.5" ry="5.5"
                fill="none" stroke="currentColor" stroke-width="1.9"/>
          <circle cx="12" cy="12" r="4.2" fill="none" stroke="currentColor" stroke-width="1.9"/>
          <circle cx="17.4" cy="6.6" r="1.3" fill="currentColor"/>
        </svg>
        <span class="ig__label">Instagram</span>
      </a>
      <a class="ig" href="{SITE['facebook_url']}" rel="noopener"
         aria-label="{SITE['name']} on Facebook"
         title="Follow us on Facebook">
        <svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true" focusable="false">
          <rect x="2.5" y="2.5" width="19" height="19" rx="5.5" ry="5.5"
                fill="none" stroke="currentColor" stroke-width="1.9"/>
          <path d="M14.9 8.1h-1.2c-.5 0-.7.2-.7.7v1.5h1.9l-.25 2h-1.65v5.4h-2.1v-5.4H9.3v-2h1.6V8.4
                   c0-1.5.85-2.4 2.5-2.4h1.5v2.1z" fill="currentColor"/>
        </svg>
        <span class="ig__label">Facebook</span>
      </a>
      <a class="btn btn--primary" href="{SITE['book_path']}">Book a Flight</a>
    </nav>
  </div>
</header>

<main id="main">
{page['body']}
</main>

<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <span class="logo"><img src="/assets/img/logo.webp" width="500" height="172"
              alt="{SITE['name']}"></span>
        <p>Friendly, student-first flight training at
           <a href="{SITE['airport_url']}" rel="noopener">Falcon Field Airport</a>
           in Mesa, Arizona.</p>
        <p>{address_html()}<br>
           {phone_html()}<br>
           <a href="mailto:{SITE['email']}">{SITE['email']}</a></p>
      </div>
      <div>
        <h4>Training</h4>
        <ul>{footer_training}</ul>
      </div>
      <div>
        <h4>More</h4>
        <ul>{footer_more}</ul>
      </div>
    </div>
    <div class="footer-areas">
      <div class="footer-areas__text">
        <h4>Serving the East Valley</h4>
        <p>{footer_areas}</p>
      </div>
      <a class="footer-dealer" href="https://www.sportys.com/" rel="noopener"
         aria-label="SG Flight School is an authorized Sporty's dealer">
        <img src="/assets/img/sportys-dealer.png" width="310" height="420"
             alt="Authorized Sporty's Dealer" loading="lazy">
      </a>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2026 {SITE['name']}. All rights reserved.</span>
      <span>SG stands for Silly Goose &mdash; flying should be fun.</span>
    </div>
  </div>
</footer>

<script>
(function(){{
  var b=document.querySelector('.nav-toggle'),n=document.getElementById('nav');
  if(!b||!n)return;
  b.addEventListener('click',function(){{
    var open=n.classList.toggle('open');
    b.setAttribute('aria-expanded',open?'true':'false');
  }});
}})();
</script>
{page_scripts}
</body>
</html>
"""


def main():
    import content

    os.makedirs(OUT, exist_ok=True)
    check_function_constants()
    print("stylesheet:", hash_css())
    for page in content.PAGES:
        slug = page["slug"]
        if slug == "index":
            dest = os.path.join(OUT, "index.html")
        else:
            os.makedirs(os.path.join(OUT, slug), exist_ok=True)
            dest = os.path.join(OUT, slug, "index.html")
        markup, n_ext = external_new_tab(render(page))
        with open(dest, "w", encoding="utf-8") as f:
            f.write(markup)
        print("wrote", os.path.relpath(dest, ROOT), f"({n_ext} external links -> new tab)")

    # sitemap
    urls = []
    for page in content.PAGES:
        loc = SITE["url"] + ("" if page["slug"] == "index" else "/" + page["slug"])
        pri = "1.0" if page["slug"] == "index" else "0.8"
        # lastmod from the file we just wrote, so it reflects real page changes
        # rather than the date of every build.
        dest = os.path.join(
            OUT, "index.html" if page["slug"] == "index"
            else os.path.join(page["slug"], "index.html")
        )
        lastmod = ""
        if os.path.exists(dest):
            ts = datetime.date.fromtimestamp(os.path.getmtime(dest)).isoformat()
            lastmod = f"<lastmod>{ts}</lastmod>"
        urls.append(
            f"  <url><loc>{loc}</loc>{lastmod}<priority>{pri}</priority></url>"
        )
    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap)
    print("wrote site/sitemap.xml")

    with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE['url']}/sitemap.xml\n")
    print("wrote site/robots.txt")


if __name__ == "__main__":
    main()
