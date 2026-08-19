# Listings setup pack — SG Flight School

Everything needed to create your Google Business Profile and directory listings.
All copy is written and ready to paste. Prepared 2026-08-16.

> **Do the 480 number first.** Every field below marked PHONE must use the same
> number everywhere, forever. Changing it after listings are indexed and cited
> across the web undoes the consistency that makes local search work. See
> README.md → "Getting a 480 number."

---

## The canonical business facts

Use these **character for character** on every listing. Inconsistent name,
address or phone ("NAP") across directories is the most common reason small
businesses underperform in local search.

| Field | Value |
|---|---|
| Business name | `SG Flight School` |
| Street | `4800 E Falcon Dr, Hangar 120` |
| City / State / ZIP | `Mesa, AZ 85215` |
| Country | United States |
| Phone | **PHONE — pending 480 number** |
| Website | `https://www.sgflightschool.com` |
| Email | `info@sgflightschool.com` |
| Instagram | `https://www.instagram.com/sgflightschool/` |
| Booking | `https://flightcircle.com/associate/dd15a6da8a75` |
| Airport | Falcon Field Airport (KFFZ), Mesa, Arizona |

Do **not** write the name as "SG Flight School | Mesa Flight Training" or any
variation with keywords appended. Google suspends listings for it.

---

## 1. Google Business Profile — business.google.com

This is the one that matters. It is what puts you on Google Maps.

### Categories
- **Primary:** Flight school
- **Secondary:** Aviation training institute
- **Secondary:** Flying club *(only if you actually operate as one — otherwise skip)*

### Service areas
Mesa, Phoenix, Scottsdale, Gilbert, Chandler, Tempe, Apache Junction, Queen Creek

### Description (740 chars — GBP limit is 750)

```
SG Flight School provides friendly, student-first flight training at Falcon
Field Airport (KFFZ) in Mesa, Arizona. We offer discovery flights, Private Pilot
(PPL), Instrument (IFR), Commercial (CPL) and Certified Flight Instructor (CFI)
training, plus aircraft rental and nationwide ferry service.

Our Certified Flight Instructors build a personalized training plan around your
schedule and pace. We train in two Cessna 172 SkyHawks, one equipped with dual
Garmin G5s and a Garmin GNS 650 for IFR work.

New to flying? A $199 discovery flight puts you in the left seat with an
instructor — no experience or medical certificate required. We publish our
rates and training costs openly, so you know what you're getting into.
```

### Services to add
Discovery Flight ($199) · Private Pilot License (PPL) · Instrument Rating (IFR) ·
Commercial Pilot License (CPL) · Certified Flight Instructor (CFI) · Aircraft
Rental · Aircraft Ferry Service · Ground School

### Attributes worth setting
Appointment required · Online booking · LGBTQ+ friendly *(if accurate)* ·
Wheelchair accessible parking *(only if true — check the hangar)*

### Photos to upload (have these ready before you start)
GBP listings with 10+ photos get materially more engagement.

- Exterior of Hangar 120 with any signage
- Both aircraft on the ramp — N61574 (Kraken) and N1287U (Nessie), tail numbers legible
- Panel/avionics shot of N61574 showing the dual G5s
- Jensen with an aircraft
- A student in the left seat
- Air-to-air or aerial over the Superstitions / Salt River
- The logo, as the profile image

Already on your site under `site/assets/img/` — reuse those.

### Verification
A hangar address will likely trigger **video verification** rather than a
postcard. Have ready, in one unbroken take:
- The hangar exterior and any street signage
- Walking inside, showing the aircraft
- Something showing the business name (paperwork, signage, laptop with the site)

---

## 2. Reviews — the biggest lever after existing at all

Review count and recency drive local ranking more than anything else you control.

Once the profile is live, GBP gives you a short review link. Put it:
- In your phone's saved messages
- On a card in each aircraft
- In your email signature
- In FlightCircle booking confirmations, if it allows custom text

### Ask template — after a discovery flight

```
Great flying with you today! If you enjoyed it, a quick Google review would
genuinely help other people find us: [LINK]

Even a sentence about how the flight went makes a difference.
```

### Ask template — after a checkride

```
Congratulations again — you earned it. Would you mind leaving us a Google
review? [LINK]

If you mention what you trained for (private pilot, instrument, etc.) it helps
the right people find us.
```

Ask the moment they land after a discovery flight. That is the happiest they
will ever be about your business.

Never offer anything in exchange for a review — it violates Google's terms and
risks the listing.

---

## 3. Directory listings, in priority order

| Priority | Site | Notes |
|---|---|---|
| 1 | **AOPA Flight School Finder** — aopa.org | Pilots actually use this. Highest-value aviation directory. |
| 2 | **Falcon Field tenant directory** — falconfieldairport.com | You're a tenant. Ask the airport office directly. |
| 3 | **bestaviation.net** | Competitors listed, you aren't. Free. |
| 4 | **Yelp** — biz.yelp.com | You're missing from "Top 10 Flight Schools in Mesa." |
| 5 | **Apple Business Connect** — businessconnect.apple.com | Feeds Apple Maps and Siri. Quick. |
| 6 | **Bing Places** — bingplaces.com | Can import from Google once GBP exists. |
| 7 | Mesa Chamber of Commerce | Local citation + genuine local visibility. |

### Short description (300 chars) for directories with tighter limits

```
Student-first flight training at Falcon Field (KFFZ) in Mesa, AZ. Discovery
flights $199, plus Private, Instrument, Commercial and CFI training in two
Cessna 172s. Aircraft rental and nationwide ferry service. Personalized
instruction, transparent pricing, and a genuinely enjoyable way to learn.
```

### One-liner (150 chars)

```
Friendly, student-first flight training at Falcon Field in Mesa, AZ. Discovery
flights, PPL through CFI, aircraft rental and ferry service.
```

---

## 4. Order of operations

1. Get the 480 number
2. Update `siteconfig.py` with it, rebuild, redeploy *(one line — ask me)*
3. Create the Google Business Profile using the copy above
4. Complete verification
5. Start asking every customer for reviews — this never stops
6. Work down the directory list, using identical NAP each time
7. Add location pages to the site *(ask me — see README)*

Steps 1–2 before step 3. Everything else can happen in any order.
