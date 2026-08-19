# Improvement plan — sgflightschool.com

From the 19 Aug 2026 critique, filtered against what's actually live.
Verified 2026-08-17 against the deployed site.

## First: what the critique got wrong, and why it matters

The reviewer audited **Google's cached copy of the old Squarespace site**, not the
live site. Verified false:

- "Five pages on an old template" — all 17 pages share one template
- "Courses has seven 'Contact Us Now' links" — zero; that text doesn't exist
- "Contact has no phone, address or form" — has all three
- "/new-page still serves instructors" — 301s to /instructors
- "/cart is indexed" — 301s to FlightCircle
- "You already have Squarespace commerce" — site is on Cloudflare Pages
- "Fix robots.txt in Squarespace settings" — no Squarespace involved

**This is the real signal:** Google has not recrawled since the migration. Same
root cause as "Discovered — currently not indexed." Off-site authority is the
bottleneck, not on-site work.

Performance, which the reviewer couldn't measure: TTFB 73ms, critical path
~188 KB, hero prioritised, below-fold images lazy. Not a problem.

---

## Tier 1 — do these first (highest return)

| # | Item | Who | Notes |
|---|---|---|---|
| 1 | **Google Business Profile** | Mike | Blocked on the 480 number. Single biggest lever. Copy ready in LISTINGS-SETUP.md |
| 2 | **Collect 10+ Google reviews** | Mike | Ask every past/current student. Templates in LISTINGS-SETUP.md |
| 3 | **480 phone number** | Mike | Gates #1 and #2 |
| 4 | **Unblock AI crawlers** | Claude | Cloudflare setting, not Squarespace |
| 5 | **Directory listings** | Mike | AOPA, FlightSchoolList, Yelp, Bing, Apple, Falcon Field tenant directory |

## Tier 2 — site work (Claude can do all of it)

| # | Item | Why |
|---|---|---|
| 6 | **Standalone PPL cost page** at `/cost-of-private-pilot-license-arizona` | Best content we have, currently inside an FAQ accordion. Can outrank far bigger schools because almost nobody publishes real numbers |
| 7 | **Testimonials on the homepage** | Needs real quotes from Mike — structure ready to fill |
| 8 | **Lead form on the homepage** | Reuse the /book form under the hero |
| 9 | **Price ranges on PPL/IFR/CPL/CFI** | Only the discovery flight shows a price; vagueness reads as expensive |
| 10 | **Lean into the single-instructor story** | "Same instructor every lesson, not someone building hours until the airlines call" — a real advantage over ATP/CAE |
| 11 | **Move the Silly Goose story to the homepage** | Best differentiator, currently only on /about |
| 12 | **Content gaps** | Financing, VA/GI Bill, Part 61 vs 141, cancellation/weather policy — all need Mike's answers first |
| 13 | **Sitemap lastmod dates** | Minor crawl-scheduling help |
| 14 | **Recompress kraken.webp** (402 KB) | Lazy-loaded so it doesn't hit LCP, but oversized |

## Tier 3 — bigger efforts

| # | Item | Notes |
|---|---|---|
| 15 | **Discovery flight video** (60–90s POV) | Highest-converting asset available. Needs filming |
| 16 | **Gift certificates** for the $199 flight | Real seasonal demand. Needs a payment path — no Squarespace commerce any more |
| 17 | **Blog, one post a month** | Start with "Training in Phoenix Heat" — genuinely unserved locally |
| 18 | **Student photo strip** (post-solo, shirt-tail) | Highest-trust image a flight school can publish |
| 19 | **Strengthen city pages** with student stories per city | |

## Explicitly rejected

- Rebuilding Courses/Getting Started/Aircraft/About/Contact — already on the
  current template
- /new-page redirect, /cart noindex — already done
- Structured data — already present (LocalBusiness, FAQPage, Course, HowTo,
  Person, Service, ItemList, WebSite)
- Performance work beyond image recompression — already fast
