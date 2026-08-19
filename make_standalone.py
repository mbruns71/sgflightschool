#!/usr/bin/env python3
"""
Produce preview-standalone/ — a copy of the built site that works by
double-clicking index.html (no web server), for reviewing the prototype offline.

Rewrites root-relative links (/courses) to flat files (courses.html) and
/assets/... to relative assets/... paths.
"""
import os
import re
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "site")
DST = os.path.join(ROOT, "preview-standalone")


def flat_name(slug):
    return "index.html" if slug == "index" else f"{slug}.html"


def rewrite(htmltext, slugs):
    # /assets/... -> assets/...
    htmltext = htmltext.replace('="/assets/', '="assets/')
    # root-relative page links -> flat filenames
    for slug in slugs:
        if slug == "index":
            continue
        htmltext = htmltext.replace(f'href="/{slug}"', f'href="{flat_name(slug)}"')
    htmltext = re.sub(r'href="/"', 'href="index.html"', htmltext)
    return htmltext


def main():
    import sys
    sys.path.insert(0, ROOT)
    import build
    build.main()
    import content

    slugs = [p["slug"] for p in content.PAGES]

    if os.path.exists(DST):
        shutil.rmtree(DST)
    os.makedirs(DST)
    shutil.copytree(os.path.join(SRC, "assets"), os.path.join(DST, "assets"))

    for slug in slugs:
        src = (os.path.join(SRC, "index.html") if slug == "index"
               else os.path.join(SRC, slug, "index.html"))
        with open(src, encoding="utf-8") as f:
            out = rewrite(f.read(), slugs)
        with open(os.path.join(DST, flat_name(slug)), "w", encoding="utf-8") as f:
            f.write(out)

    print(f"\nStandalone preview: {DST}")
    print("Open preview-standalone/index.html in a browser to click through the site.")


if __name__ == "__main__":
    main()
