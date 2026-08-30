"""Shared site constants and helpers, imported by build.py and content.py."""

SITE = {
    "name": "SG Flight School",
    "url": "https://www.sgflightschool.com",
    "email": "info@sgflightschool.com",
    # Publishing the real (Montana) number so the site is functional. Swap to a
    # local 480 number before launch — see README "Phone number" — and this is
    # the only line that needs to change.
    "phone_display": "(480) 757-0522",
    "phone_href": "+14807570522",
    "phone_confirmed": True,
    "street": "4800 E Falcon Dr, Hangar 120",
    "street_confirmed": True,
    "city": "Mesa",
    "state": "AZ",
    "zip": "85215",
    "airport": "Falcon Field Airport (KFFZ)",
    "airport_url": "https://www.falconfieldairport.com/",
    # Cloudflare Turnstile public site key. Blank = widget not rendered and the
    # Function skips verification, so the form keeps working until it is set.
    "turnstile_site_key": "",
    "instagram_url": "https://www.instagram.com/sgflightschool/",
    "instagram_handle": "@sgflightschool",
    "facebook_url": "https://www.facebook.com/profile.php?id=61572830633972",
    # FlightCircle's "associate" link redirects to an account-REGISTRATION form,
    # not a booking screen. That's the wrong destination for a first-time visitor,
    # so new-visitor CTAs point at /book (our own form) and FlightCircle is
    # presented as the existing-student scheduling login.
    "schedule_url": "https://flightcircle.com/associate/dd15a6da8a75",
    "book_path": "/book",
    "shop_url": "https://www.flightcircle.com/shop/dd15a6da8a75",
    "lat": 33.4608,
    "lon": -111.7283,
}


def phone_html(cls=""):
    """Phone link, visibly flagged until the real number is confirmed."""
    c = f' class="{cls}"' if cls else ""
    link = f'<a href="tel:{SITE["phone_href"]}"{c}>{SITE["phone_display"]}</a>'
    if not SITE["phone_confirmed"]:
        return f'{link} <span class="todo">NEEDS REAL NUMBER</span>'
    return link


def address_html():
    s = f'{SITE["street"]}, {SITE["city"]}, {SITE["state"]} {SITE["zip"]}'
    if not SITE["street_confirmed"]:
        return f'{s} <span class="todo">CONFIRM ADDRESS</span>'
    return s
