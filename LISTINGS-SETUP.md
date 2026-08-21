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

---

## Google Business Profile — video verification script

Google needs one **continuous, unedited** recording that proves three things:

1. **You are where you say you are** — the location is real and matches the address
2. **The business genuinely operates there** — equipment, signage, activity
3. **You manage it** — you can access areas the public cannot

A hangar at a towered airport is harder than a storefront, because there's no
street signage and access is controlled. That controlled access is actually your
strongest evidence — use it.

### Before you press record

- **Landscape orientation.** Hold the phone sideways.
- **Clean the lens.** Sounds trivial; a smeared lens fails more takes than anything else.
- **Mid-morning.** Arizona midday sun blows out highlights and makes signage unreadable.
- **Have a document ready** — an insurance certificate, aircraft registration, a
  utility or hangar-lease bill with SG Flight School on it. Hold it steady and
  close for a good three seconds; a quick flash won't be readable.
- **Do a practice run.** You cannot pause, cut, or splice. One take, start to finish.
- **Narrate as you go.** Not required, but it helps a reviewer follow what they're
  seeing: "This is Hangar 120 at Falcon Field, 4800 East Falcon Drive."

### The take — roughly two to three minutes

1. **Start outside, wide.** Capture the approach to the hangar with the airport
   environment visible. Say the full address out loud.
2. **Hangar 120 identifier.** Get the number itself in frame, sharp and held for
   several seconds. This is the single most important shot in the video.
3. **Show controlled access.** Film yourself using the gate code, badge, or key to
   get airside or into the hangar. This is what separates an owner from a
   passer-by, and it's the evidence Google weights most heavily.
4. **Walk inside, still recording.** Do not stop. Pan across the space.
5. **The aircraft, tail numbers legible.** N61574 and N1287U. Get close enough
   that the registrations are readable, and hold each one.
6. **Something operational.** A logbook, headsets, the training materials, a
   whiteboard with schedules — anything that shows a flight school working here
   rather than a stored aeroplane.
7. **Your business document.** Held steady, close, in focus, three seconds.
8. **Finish on the aircraft or the hangar.** Confirm the business name aloud.

### Why these fail

- **Cut or edited footage.** Any splice is an automatic rejection.
- **Hangar number never clearly shown.** The most common single failure.
- **No proof of access.** Anyone can film a ramp. Show yourself unlocking something.
- **Too short.** Under about 30 seconds rarely carries enough evidence.
- **Vertical and shaky.** Legible beats cinematic.
- **Documents flashed too fast** to read.

### After you submit

Review typically takes up to about five business days. If it's rejected you can
try again — read the stated reason carefully first, since it usually names the
missing element.

**Do not change the business name, address or phone while verification is
pending.** Edits mid-review restart the process.
