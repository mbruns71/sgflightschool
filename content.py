"""Page content for SG Flight School. Edit here, then run `python3 build.py`."""

from siteconfig import SITE, address_html, phone_html

SCHED = SITE["schedule_url"]
BOOK = SITE["book_path"]
EMAIL = SITE["email"]


def cta(heading, text, primary=("Book a Discovery Flight", BOOK)):
    return f"""
<section class="cta">
  <div class="wrap">
    <h2>{heading}</h2>
    <p>{text}</p>
    <div class="btn-row btn-row--center">
      <a class="btn btn--light" href="{primary[1]}">{primary[0]}</a>
      <a class="btn btn--outline-light" href="/contact">Ask Us a Question</a>
    </div>
  </div>
</section>"""


# Banner image per page, with the scrim opacity each one needs. The values come
# from measuring each photo's brightest region where the text sits: white text
# needs the composite under ~0.18 luminance to clear 4.5:1. Brighter photo,
# heavier scrim.
BANNERS = {
    # Solved per image against each page's real heading and subtitle boxes, with
    # a 0.4 margin over the WCAG minimum. Darker photos are not automatically
    # safer: dual-instruction is dim overall but its windscreen is bright, and
    # that is exactly where the subtitle lands.
    "student-controls.webp": 0.92,
    "falcon-sunset.jpg": 0.72,
    "dual-instruction.webp": 0.90,
    "ferry-enroute.jpg": 0.84,
    "student-smile.webp": 0.80,
    "az-aerial.webp": 0.79,
    "sedona.webp": 0.73,
    "coastline.webp": 0.70,
}


def pagehead(title, sub, badge=False, image="az-aerial.webp"):
    """Interior page banner.

    `badge` adds the Sporty's dealer mark on the right. `image` selects the
    background photo; its scrim strength comes from BANNERS.
    """
    scrim = BANNERS.get(image, 0.78)
    aside = ""
    if badge:
        aside = (
            '<a class="pagehead__badge" href="https://www.sportys.com/" rel="noopener"'
            ' aria-label="SG Flight School is an authorized Sporty\'s dealer">'
            '<img src="/assets/img/sportys-dealer.png" width="310" height="420"'
            ' alt="Authorized Sporty\'s Dealer"></a>'
        )
    return f"""
<section class="pagehead" style="--ph-img:url('/assets/img/{image}');--ph-scrim:{scrim}">
  <div class="wrap pagehead__inner">
    <div class="pagehead__text"><h1>{title}</h1><p>{sub}</p></div>
    {aside}
  </div>
</section>"""


def sportys_dealer(body):
    """Authorized Sporty's Dealer callout.

    Placed where Sporty's is actually relevant — beside the ground-school
    recommendation — rather than in the header, where the badge is only ~41px
    wide and its text is illegible.
    """
    return f"""
<section class="section section--alt">
  <div class="wrap narrow">
    <div class="dealer">
      <img class="dealer__badge" src="/assets/img/sportys-dealer.png"
           width="310" height="420" alt="Authorized Sporty's Dealer"
           loading="lazy">
      <div class="dealer__body">
        <span class="eyebrow">Authorized dealer</span>
        <h2>We're a Sporty's dealer</h2>
        {body}
      </div>
    </div>
  </div>
</section>"""


# --------------------------------------------------------------------- HOME
HOME = {
    "slug": "index",
    "title": "SG Flight School | Flight Training at Falcon Field, Mesa AZ",
    "description": (
        "Learn to fly at Falcon Field Airport in Mesa, Arizona. Discovery flights "
        "from $199, plus private pilot, instrument, commercial and CFI training "
        "with friendly, student-first instructors."
    ),
    "og_image": "az-aerial.webp",
    "scripts": ["/assets/js/book.js"],
    "schema": [{
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": SITE["name"],
        "url": SITE["url"],
    }],
    "body": f"""
<section class="hero">
  <div class="wrap hero__grid">
    <div>
      <span class="eyebrow" style="color:#8fd4ec">Falcon Field Airport &middot; Mesa, Arizona</span>
      <h1>Where your journey into the skies begins</h1>
      <p>Friendly, student-first flight training in the Phoenix East Valley.
         Start with a $199 discovery flight &mdash; no experience needed &mdash;
         and take the controls yourself.</p>
      <div class="btn-row">
        <a class="btn btn--light" href="{BOOK}">Book a Discovery Flight &mdash; $199</a>
        <a class="btn btn--outline-light" href="/getting-started">How to Get Started</a>
      </div>
      <p class="hero__note">Questions? Call {phone_html()} or email
         <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
    </div>
    <div class="hero__img">
      <img src="/assets/img/az-aerial.webp" width="1000" height="750"
           alt="View from a Cessna wing over the Superstition Mountains and Salt River near Mesa, Arizona"
           fetchpriority="high">
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="narrow center" style="margin:0 auto 44px">
      <span class="eyebrow">Training that fits your life</span>
      <h2>Ready to earn your certificate in Arizona?</h2>
      <p class="lead">Our Certified Flight Instructors build a personalized training
         plan around your schedule and your goals &mdash; whether you want to be a
         weekend flyer or fly for the airlines.</p>
    </div>
    <div class="grid grid--3">
      <div class="card">
        <span class="price price--sun">$199</span>
        <h3>Discovery Flight</h3>
        <div class="card__body"><p>Your first lesson. Sit up front with a CFI,
          take the controls, and see the Valley from the air. No experience required.</p></div>
        <a class="btn btn--primary" href="{BOOK}">Book Now</a>
      </div>
      <div class="card">
        <span class="price">Most popular</span>
        <h3>Private Pilot (PPL)</h3>
        <div class="card__body"><p>Ground school plus flight training, from your
          first takeoff through your checkride. Carry passengers and fly for fun.</p></div>
        <a class="btn btn--ghost" href="/courses">See Courses</a>
      </div>
      <div class="card">
        <span class="price">Career track</span>
        <h3>IFR, Commercial &amp; CFI</h3>
        <div class="card__body"><p>Keep going. Add an instrument rating, get paid
          to fly with a commercial certificate, then teach as a CFI.</p></div>
        <a class="btn btn--ghost" href="/courses">See Courses</a>
      </div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="grid grid--2" style="align-items:center;gap:48px">
      <div>
        <span class="eyebrow">Why SG</span>
        <h2>SG stands for Silly Goose</h2>
        <p>That is not an accident, and it is not a joke at the expense of the
           flying. It is a reminder that learning to fly should be rigorous
           <em>and</em> genuinely enjoyable &mdash; because the students who
           finish are the ones who still want to show up on week thirty.</p>
        <p><strong>You'll fly with the same instructor every lesson.</strong> Not
           a rotating cast, not someone counting hours until the airlines call.
           He'll remember what you struggled with last time, so nothing gets
           re-explained and no lesson is spent catching somebody new up.</p>
        <p>We are also straightforward about money. Our rates are published, and
           our <a href="/cost-of-private-pilot-license-arizona">full cost
           breakdown</a> gives a realistic total instead of the FAA-minimum
           figure almost nobody actually hits.</p>
        <a class="btn btn--ghost" href="/about">More About Us</a>
      </div>
      <div><img src="/assets/img/student-smile.webp" width="750" height="562"
           alt="A smiling SG Flight School student in the cockpit before takeoff"
           style="border-radius:12px" loading="lazy"></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="narrow center" style="margin:0 auto 44px">
      <span class="eyebrow">Our fleet</span>
      <h2>Two well-equipped Cessna 172s</h2>
      <p class="lead">Transparent hourly rates, glass instrumentation, and aircraft
         suited to both VFR and IFR training.</p>
    </div>
    <div class="grid grid--2">
      <div class="card card--media">
        <img src="/assets/img/kraken-ramp.jpg" width="1100" height="825" alt="N61574 &quot;Kraken&quot;, a Cessna 172M SkyHawk II, on the ramp at Falcon Field" loading="lazy">
        <div class="card__inner">
          <span class="aircraft__tail">N61574 &middot; "Kraken"</span>
          <h3>Cessna 172M SkyHawk II</h3>
          <p>Dual Garmin G5s and a Garmin GNS 650 avionics suite &mdash; ideal for
             IFR training and cross-country navigation.</p>
          <ul class="rates">
            <li><strong>$165</strong><span>per hour, wet</span></li>
            <li><strong>$60</strong><span>per hour, instruction</span></li>
          </ul>
        </div>
      </div>
      <div class="card card--media">
        <img src="/assets/img/nessie-sunset.jpg" width="1100" height="825" alt="N1287U &quot;Nessie&quot; on the Falcon Field ramp at sunset, cabin door open" loading="lazy">
        <div class="card__inner">
          <span class="aircraft__tail">N1287U &middot; "Nessie"</span>
          <h3>Cessna 172M SkyHawk II</h3>
          <p>A dependable trainer for VFR and IFR work, and the most affordable
             way to build hours in our fleet.</p>
          <ul class="rates">
            <li><strong>$160</strong><span>per hour, wet</span></li>
            <li><strong>$60</strong><span>per hour, instruction</span></li>
          </ul>
        </div>
      </div>
    </div>
    <div class="center" style="margin-top:34px">
      <a class="btn btn--ghost" href="/aircraft">Fleet Details</a>
    </div>
  </div>
</section>


<section class="section section--alt" id="enquire">
  <div class="wrap narrow">
    <div class="center" style="margin-bottom:30px">
      <span class="eyebrow">Get in touch</span>
      <h2>Ask us anything, or book your first flight</h2>
      <p class="lead">Call {phone_html()} for the fastest answer &mdash; or leave
         your details and we'll come back to you, usually the same day.</p>
    </div>
    <form class="form" id="book-form" method="POST" action="/api/book" novalidate>
      <div class="form__grid">
        <div class="form__row">
          <label for="h-name">Your name <span aria-hidden="true">*</span></label>
          <input id="h-name" name="name" type="text" autocomplete="name" required maxlength="120">
        </div>
        <div class="form__row">
          <label for="h-phone">Phone <span aria-hidden="true">*</span></label>
          <input id="h-phone" name="phone" type="tel" autocomplete="tel" required maxlength="40" inputmode="tel">
        </div>
      </div>
      <div class="form__grid">
        <div class="form__row">
          <label for="h-email">Email</label>
          <input id="h-email" name="email" type="email" autocomplete="email" maxlength="160">
        </div>
        <div class="form__row">
          <label for="h-interest">Interested in</label>
          <select id="h-interest" name="interest">
            <option value="Discovery flight ($199)">Discovery flight ($199)</option>
            <option value="Private pilot (PPL)">Private pilot certificate</option>
            <option value="Instrument rating (IFR)">Instrument rating</option>
            <option value="Commercial (CPL)">Commercial certificate</option>
            <option value="CFI">Flight instructor (CFI)</option>
            <option value="Aircraft rental">Aircraft rental</option>
            <option value="Ferry service">Aircraft ferry service</option>
            <option value="Something else">Something else</option>
          </select>
        </div>
      </div>
      <div class="form__row">
        <label for="h-notes">Anything we should know?</label>
        <textarea id="h-notes" name="notes" rows="3" maxlength="2000"
                  placeholder="Optional — questions, previous experience, when you're free."></textarea>
      </div>
      <div class="form__trap" aria-hidden="true">
        <label for="h-website">Website</label>
        <input id="h-website" name="website" type="text" tabindex="-1" autocomplete="off">
      </div>
      <button class="btn btn--primary" type="submit" id="book-submit">Send &mdash; we'll be in touch</button>
      <p class="form__note">No mailing list, and we won't pass your details on.
         Prefer the longer form? <a href="{BOOK}">Full booking page.</a></p>
      <div class="form__status" id="book-status" role="status" aria-live="polite"></div>
    </form>
  </div>
</section>

{cta("Let's schedule your flight adventure",
     "Book a discovery flight online, or reach out and we'll answer every question "
     "you have about learning to fly at Falcon Field.")}
""",
}

# ------------------------------------------------------------------ COURSES
COURSE_DATA = [
    ("Discovery Flight", "$199", "student-smile.webp",
     "An introductory flying experience designed to give you a taste of what it's "
     "like to be a pilot &mdash; no previous experience required. You'll sit in the "
     "cockpit with a Certified Flight Instructor who walks you through the basic "
     "controls and maneuvers, and you'll have the chance to fly the plane yourself. "
     "A low-pressure, hands-on way to find out whether pursuing a certificate is "
     "right for you.",
     True),
    ("Private Pilot License (PPL)", "Most popular", "student-controls.webp",
     "A comprehensive program covering both ground school and flight training. In "
     "ground school you'll learn aviation theory, regulations, weather and "
     "navigation. In the air, you'll learn to fly under the guidance of a CFI. The "
     "course finishes with a checkride, where you demonstrate your proficiency to a "
     "Designated Pilot Examiner. A PPL lets you fly privately and carry passengers "
     "for non-commercial purposes.",
     False),
    ("Instrument Rating (IFR)", "Next step", "dual-instruction.webp",
     "The next level of training, teaching you to fly solely by reference to "
     "instruments. Essential for flying in clouds or low visibility, and a strong "
     "way to sharpen the skills you built during your private pilot training. "
     "Includes ground school on instrument navigation, flight planning and "
     "regulations, plus in-flight practice in simulated and actual instrument "
     "conditions &mdash; navigational aids, instrument approaches and cockpit "
     "resource management.",
     False),
    ("Commercial Pilot License (CPL)", "Career track", "sedona.webp",
     "Designed for pilots who want to fly professionally. This advanced program "
     "builds on your private pilot skills with higher standards of precision, "
     "safety and decision-making, emphasizing aviation regulation, advanced "
     "aerodynamics and cross-country navigation. A CPL allows you to be compensated "
     "for your flying and opens the door to a career in aviation.",
     False),
    ("Certified Flight Instructor (CFI)", "Teach others", "dual-instruction.webp",
     "A program that prepares experienced pilots to teach others to fly. The focus "
     "is on communicating flight concepts clearly, instructing students effectively, "
     "and safely managing a training environment. It's also the most common way to "
     "build the hours you need for an airline career.",
     False),
]


COURSE_ALT = {
    "student-smile.webp": "A smiling student in the cockpit of a Cessna 172 before a discovery flight",
    "student-controls.webp": "A student pilot flying a Cessna 172 over the Arizona desert",
    "dual-instruction.webp": "A flight instructor and student flying together in a Cessna 172",
    "sedona.webp": "View from a Cessna wing over the red rock formations near Sedona, Arizona",
}


# Typical all-in cost per course, calculated from our published rates plus the
# usual third-party costs. Ranges, not quotes — see /cost-of-private-pilot-
# license-arizona for the full PPL breakdown and the assumptions behind these.
COURSE_COST = {
    "Discovery Flight": ("$199", "One flight, about an hour. Nothing else to pay."),
    "Private Pilot License (PPL)": (
        "$14,000&ndash;16,000",
        'Typical all-in. <a href="/cost-of-private-pilot-license-arizona">'
        "Full breakdown &rarr;</a>"),
    "Instrument Rating (IFR)": (
        "$10,000&ndash;14,000",
        "Typical all-in, including written and checkride."),
    "Commercial Pilot License (CPL)": (
        "$5,500&ndash;8,500 training",
        "Plus time building to 250 hours &mdash; usually the larger cost."),
    "Certified Flight Instructor (CFI)": (
        "$6,000&ndash;9,000",
        "Typical all-in, including both written tests and the checkride."),
}


def course_cards():
    out = []
    for name, badge, img, desc, is_discovery in COURSE_DATA:
        alt = COURSE_ALT[img]
        cls = "price price--sun" if is_discovery else "price"
        btn = (f'<a class="btn btn--primary" href="{BOOK}">Book Now</a>'
               if is_discovery else
               '<a class="btn btn--ghost" href="/contact">Ask About This Course</a>')
        cost = COURSE_COST.get(name)
        cost_html = ""
        if cost and not is_discovery:
            cost_html = (f'<p class="course-cost"><strong>{cost[0]}</strong>'
                         f'<span>{cost[1]}</span></p>')
        out.append(f"""
      <div class="card card--media">
        <img src="/assets/img/{img}" width="750" height="562" alt="{alt}" loading="lazy">
        <div class="card__inner">
          <span class="{cls}">{badge}</span>
          <h3>{name}</h3>
          {cost_html}
          <div class="card__body"><p>{desc}</p></div>
          {btn}
        </div>
      </div>""")
    return "".join(out)


COURSES = {
    "slug": "courses",
    "title": "Flight Training Courses",
    "description": (
        "Discovery flights from $199, private pilot, instrument rating, commercial "
        "and CFI training at Falcon Field Airport in Mesa, Arizona."
    ),
    "og_image": "student-smile.webp",
    "schema": [{
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Flight training courses at SG Flight School",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "item": {
                    "@type": "Course",
                    "name": name,
                    "description": desc.replace("&mdash;", "—"),
                    "provider": {"@id": SITE["url"] + "/#organization"},
                },
            }
            for i, (name, _b, _i, desc, _d) in enumerate(COURSE_DATA)
        ],
    }],
    "body": pagehead(
        "Flight training courses",
        "From your very first flight to a career in the cockpit — every certificate "
        "and rating we offer, taught at your pace.",
        badge=True,
        image="dual-instruction.webp",
    ) + f"""
<section class="section">
  <div class="wrap">
    <div class="narrow" style="margin:0 auto 44px">
      <p class="lead">Your flight journey is unique, and we're excited to guide you
         every step of the way. Whether you're dreaming of a career in the airlines
         or just want to explore the skies as a hobby, start wherever makes sense
         &mdash; most students begin with a discovery flight.</p>
    </div>
    <div class="grid grid--3">{course_cards()}</div>
    <div class="wrap narrow" style="padding:0;margin-top:44px">
      <div class="callout">
        <h3 style="margin-top:0">One thing to know about the commercial certificate</h3>
        <p>The FAA requires 10 hours of training in a complex or technically
           advanced airplane. Our two Cessna 172s are neither &mdash; no
           retractable gear, no constant-speed prop, and no two-axis autopilot.</p>
        <p style="margin-bottom:0">You can do everything else toward your
           commercial certificate with us, and we'll help you arrange those 10
           hours in a suitable aircraft. We'd rather tell you now than at hour
           200. <a href="/contact">Ask us</a> and we'll walk through the whole
           sequence.</p>
      </div>
    </div>
  </div>
</section>
""" + sportys_dealer("""
        <p>Every course here has a ground-school component, and you'll need books,
           a headset and a few other things along the way. We're an authorized
           Sporty's dealer, so you can get all of it through us.</p>
        <p>Same products, same prices &mdash; but with your instructor telling you
           what's worth buying now and what can wait.
           <a href="/getting-started">More on ground school options.</a></p>
""") + f"""
{cta("Not sure which course is right for you?",
     "Tell us your goals and we'll map out the fastest, most affordable path to "
     "get you there.")}
""",
}

# ---------------------------------------------------------- GETTING STARTED
GETTING_STARTED = {
    "slug": "getting-started",
    "title": "How to Get Started as a Pilot",
    "description": (
        "The eight steps to earning your Private Pilot License — FAA medical, "
        "ground school, flight training, written test and checkride — explained by "
        "SG Flight School in Mesa, AZ."
    ),
    "og_image": "student-controls.webp",
    "schema": [{
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": "How to earn a Private Pilot License",
        "description": "The mandatory steps to earning an FAA Private Pilot License.",
        "step": [
            {"@type": "HowToStep", "position": 1, "name": "Obtain an FAA medical certificate"},
            {"@type": "HowToStep", "position": 2, "name": "Choose a flight school"},
            {"@type": "HowToStep", "position": 3, "name": "Start ground school"},
            {"@type": "HowToStep", "position": 4, "name": "Begin flight training"},
            {"@type": "HowToStep", "position": 5, "name": "Pass the FAA knowledge test"},
            {"@type": "HowToStep", "position": 6, "name": "Complete solo flight requirements"},
            {"@type": "HowToStep", "position": 7, "name": "Pass the FAA checkride"},
            {"@type": "HowToStep", "position": 8, "name": "Receive your Private Pilot License"},
        ],
    }],
    "body": pagehead(
        "Getting started",
        "Earning a Private Pilot License involves several mandatory steps. Here's the "
        "whole path — and how we make each one as easy as possible.",
        image="student-controls.webp",
    ) + f"""
<section class="section">
  <div class="wrap narrow">
    <ol class="steps">
      <li>
        <h3>Obtain an FAA medical certificate</h3>
        <p>This can take months for the FAA to review and approve, so make it your
           first step. Don't be nervous &mdash; the examination simply confirms
           you're healthy enough to fly.
           <a href="/faa-medical-exam">See what the exam covers.</a></p>
        <ul>
          <li>Schedule an exam with an FAA-authorized Aviation Medical Examiner (AME).
              <a href="https://www.faa.gov/pilots/amelocator" rel="noopener">Find an AME near you.</a></li>
          <li>Create an account at
              <a href="https://medxpress.faa.gov/" rel="noopener">FAA MedXPress</a>.
              Your AME will need this documentation and your MID.</li>
          <li>You'll need at least a Third-Class Medical Certificate. A Recreational
              Pilot Certificate is an alternative, but comes with flying restrictions
              &mdash; ask your instructor which is right for you.</li>
          <li>You can begin ground and flight training while you wait for results.</li>
        </ul>
      </li>
      <li>
        <h3>Choose a flight school</h3>
        <p>Look for experienced instructors, well-maintained aircraft and a good
           safety record. <a href="/contact">Contact SG Flight School</a> and we'll
           answer your questions and get you scheduled.</p>
      </li>
      <li>
        <h3>Start ground school</h3>
        <p>Ground school covers the theory: aerodynamics, weather, navigation and
           FAA regulations. You have options:</p>
        <ul>
          <li><strong>With your SG instructor.</strong> The most thorough option, and
              the most expensive &mdash; but you'll have the strongest grasp of the material.</li>
          <li><strong>Online, at your own pace.</strong>
              <a href="https://www.sportys.com/" rel="noopener">Sporty's</a> is a great
              option with well-built guides, practice tests and study aids for the
              FAA knowledge test.
              <a href="https://www.gleimaviation.com/" rel="noopener">Gleim</a> is
              another solid choice.</li>
        </ul>
      </li>
      <li>
        <h3>Begin flight training</h3>
        <p>Start lessons with your SG Flight School CFI.</p>
        <ul>
          <li><strong>Flight hours:</strong> a minimum of 40 hours, including 20 with
              an instructor and 10 solo. Most students take more &mdash; that's normal.</li>
          <li><strong>Skills:</strong> takeoffs, landings, navigation, emergency
              procedures and cross-country flying.</li>
          <li><strong>Logbook:</strong> keep a detailed record of all hours and training.</li>
        </ul>
      </li>
      <li>
        <h3>Pass the FAA knowledge test</h3>
        <p>Sixty multiple-choice questions covering everything from ground school.
           Your instructor will help you schedule it and prepare with practice exams.</p>
      </li>
      <li>
        <h3>Complete solo flight requirements</h3>
        <p>After enough training, your instructor will endorse you to fly solo
           &mdash; one of the most memorable days in any pilot's life.</p>
      </li>
      <li>
        <h3>Pass the FAA checkride</h3>
        <p>Once you've logged the required hours, your instructor endorses you for
           the checkride: an oral exam plus a practical flight test with an FAA
           Designated Pilot Examiner. Review all knowledge areas and practice your
           maneuvers to make sure you're proficient.</p>
      </li>
      <li>
        <h3>Obtain your Private Pilot License</h3>
        <p>Your examiner issues a temporary certificate on the spot, and the FAA
           mails your permanent license within a few weeks. You're a pilot.</p>
      </li>
    </ol>
  </div>
</section>
""" + sportys_dealer("""
        <p>SG Flight School is an authorized Sporty's dealer, so you can get your
           ground school course, headset, charts, kneeboard and the rest of your
           training gear through us rather than ordering it yourself.</p>
        <p>It's the same Sporty's products at the same prices &mdash; the
           difference is that your instructor can tell you what you actually
           need before you buy it, and what you can happily skip until later.
           New students routinely spend hundreds on gear they never use.</p>
        <p><a href="/contact">Ask us</a> what to get before you order anything.</p>
""") + f"""
<section class="section section--alt">
  <div class="wrap narrow">
    <h2>Where this leads</h2>
    <figure class="shot">
      <img src="/assets/img/backcountry.jpg" width="1100" height="825"
           alt="N1287U parked at a remote Arizona airstrip at golden hour, with a tent
                pitched beside the aircraft and a lake and mountains behind"
           loading="lazy">
      <figcaption>A licence is a door, not a destination. Camping trips to strips you
        can only reach by air are exactly the sort of thing it opens.</figcaption>
    </figure>
  </div>
</section>

{cta("Step one is easier than you think",
     "Book a discovery flight and find out whether flying is for you — before you "
     "commit to anything.")}
""",
}

# ----------------------------------------------------------------- AIRCRAFT
AIRCRAFT = {
    "slug": "aircraft",
    "title": "Our Aircraft & Rental Rates",
    "description": (
        "Two Cessna 172M SkyHawk IIs available for training and rental at Falcon "
        "Field, Mesa AZ. Wet rates from $160/hour plus $60/hour instruction."
    ),
    "og_image": "kraken-ramp.jpg",
    "body": pagehead(
        "Our aircraft",
        "Two well-equipped Cessna 172M SkyHawk IIs, available for training and rental.",
        image="ferry-enroute.jpg",
    ) + f"""
<section class="section">
  <div class="wrap">
    <div class="aircraft">
      <img src="/assets/img/kraken-ramp.jpg" width="1100" height="825" alt="Cessna 172M SkyHawk II, N61574, known as Kraken">
      <div>
        <span class="aircraft__tail">N61574 &middot; "Kraken"</span>
        <h2>Cessna 172M SkyHawk II</h2>
        <p>Equipped with dual Garmin G5 instruments and a Garmin GNS 650 avionics
           suite, N61574 is well suited to both IFR and VFR flight training. The dual
           G5s provide clear, reliable digital flight data &mdash; precise attitude,
           altitude and heading information &mdash; which makes them excellent for
           learning. Paired with the GNS 650, they support cross-country navigation,
           traffic separation, weather updates and more.</p>
        <p>Kraken is a great airplane for every level of training.</p>
        <ul class="rates">
          <li><strong>$165</strong><span>per hour, wet</span></li>
          <li><strong>$60</strong><span>per hour, instruction</span></li>
        </ul>
      </div>
    </div>
    <div class="aircraft">
      <img src="/assets/img/nessie-sunset.jpg" width="1100" height="825" alt="Cessna 172M SkyHawk II, N1287U, known as Nessie">
      <div>
        <span class="aircraft__tail">N1287U &middot; "Nessie"</span>
        <h2>Cessna 172M SkyHawk II</h2>
        <p>A dependable, straightforward trainer for both IFR and VFR work, and the
           most affordable way to build time in our fleet.</p>
        <ul class="rates">
          <li><strong>$160</strong><span>per hour, wet</span></li>
          <li><strong>$60</strong><span>per hour, instruction</span></li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="narrow" style="margin:0 auto 40px">
      <span class="eyebrow">Rates &amp; rental</span>
      <h2>What you actually pay</h2>
    </div>
    <div class="grid grid--3">
      <div class="card">
        <h3>"Wet" includes fuel</h3>
        <p>The hourly aircraft rate covers fuel &mdash; you're not settling up at
           the pump afterward. Instruction is billed separately at $60/hour, so an
           hour of dual in Kraken is $165 + $60 = <strong>$225</strong>.</p>
      </div>
      <div class="card">
        <h3>You're billed for time flown</h3>
        <p>Aircraft time is metered by the Hobbs meter, which runs while the engine
           does. Preflight inspection and post-flight debrief with your instructor
           aren't aircraft time.</p>
      </div>
      <div class="card">
        <h3>Renting as a certificated pilot</h3>
        <p>Both aircraft are available to rated pilots after a checkout with one of
           our instructors. That's standard everywhere &mdash; it's about being
           comfortable in this specific airplane.
           <a href="/contact">Ask us</a> about current requirements.</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap narrow">
    <span class="eyebrow">Why a 172</span>
    <h2>Why we train in Cessna 172s</h2>
    <p>The 172 is the most-produced aircraft in history, and it earned that. It's a
       high-wing design, which means an unobstructed view of the ground below you
       &mdash; genuinely useful when you're learning to judge a landing or find a
       checkpoint. It's stable, forgiving of the imprecision every student starts
       with, and it recovers predictably when you get something wrong.</p>
    <p>It's also everywhere. Skills you build in a 172 transfer directly to rental
       fleets across the country, so the certificate you earn here stays useful
       wherever you travel.</p>
    <p style="color:#6b7a88;font-size:.95rem;margin-top:28px">
      Rates are current as of 2026 and subject to change.
      <a href="/contact">Contact us</a> to confirm pricing before you schedule.</p>
  </div>
</section>

{cta("Want to fly one of these?",
     "Book a discovery flight, or get in touch about aircraft rental and checkout "
     "requirements.")}
""",
}

# -------------------------------------------------------------- INSTRUCTORS
INSTRUCTORS = {
    "slug": "instructors",
    "title": "Your Flight Instructor",
    "description": (
        "At SG Flight School you fly with the same instructor every lesson — not a "
        "rotating cast. Meet Jensen Beard, CFI, at Falcon Field in Mesa, Arizona."
    ),
    "og_image": "jensen.jpg",
    "schema": [{
        "@context": "https://schema.org",
        "@type": "Person",
        "name": "Jensen Beard",
        "jobTitle": "Certified Flight Instructor",
        "image": SITE["url"] + "/assets/img/jensen.jpg",
        "email": "jbeard@sgflightschool.com",
        "worksFor": {"@id": SITE["url"] + "/#organization"},
    }],
    "body": pagehead(
        "Your instructor",
        "The same one, every lesson — not whoever happens to be on the roster.",
        image="dual-instruction.webp",
    ) + f"""
<section class="section">
  <div class="wrap narrow">
    <div class="bio">
      <div class="bio__meta">
        <img class="bio__photo" src="/assets/img/jensen.jpg" width="1200" height="900"
             alt="Jensen Beard, Certified Flight Instructor at SG Flight School, flying a Cessna above the clouds">
        <h3>Jensen Beard</h3>
        <p class="bio__role">Certified Flight Instructor</p>
        <p style="margin:0"><a href="mailto:jbeard@sgflightschool.com">jbeard@sgflightschool.com</a></p>
      </div>
      <div>
        <p>Hello! I'm Jensen Beard, and I'm delighted to be your flight instructor.
           Aviation has been my lifelong passion, and with nine years of flying
           experience under my belt, I'm excited to share it with you. My flying has
           taken me across a number of states and a wide range of environments,
           which gives me plenty of real-world experience to pass along.</p>
        <p>From a young age I was captivated by the idea of flying, and that
           fascination has only grown. Alongside my aviation experience, I've honed
           my teaching skills as a substitute teacher and through my time teaching in
           the Army. Those experiences shaped a positive, adaptable teaching method
           that works with any learning style, so every student gets instruction
           tailored to them.</p>
        <p>My mission is to help you become not just a pilot, but a confident and
           safe pilot. I want each lesson to be engaging and supportive, guiding you
           past your goals while building the skills, knowledge and confidence you
           need in the cockpit. Beyond training pilots, I'm passionate about helping
           people join and thrive in the aviation community. I look forward to
           turning your dreams of flying into reality.</p>
      </div>
    </div>
  </div>
</section>


<section class="section section--alt">
  <div class="wrap narrow">
    <span class="eyebrow">Why one instructor matters</span>
    <h2>You'll fly with the same person every lesson</h2>
    <p>Large academies rotate students between instructors, and most of those
       instructors are building hours toward an airline job. That's a perfectly
       honest career path &mdash; but it means your training is handed off, often
       more than once, and each new instructor spends time re-learning where you
       are before you make progress again.</p>
    <p>That doesn't happen here. Jensen flies with you from your first lesson to
       your checkride. He knows which maneuver you struggled with three weeks ago
       and what finally made it click. Nothing gets re-explained because nobody
       new has to catch up.</p>
    <div class="grid grid--2" style="margin-top:26px">
      <div class="card">
        <h3>Consistency is cheaper</h3>
        <p>Every instructor handoff costs you flight hours while somebody new
           assesses where you are. At $220 an hour for dual instruction, that
           adds up faster than most students expect.</p>
      </div>
      <div class="card">
        <h3>We're honest about the trade</h3>
        <p>One instructor and two aircraft means we can't take unlimited students
           or promise a fixed finish date. If you need a rigid timeline, a larger
           academy may genuinely suit you better &mdash; and we'll say so.</p>
      </div>
    </div>
    <p style="margin-top:26px">If that sounds like the way you'd rather learn,
       <a href="{BOOK}">book a discovery flight</a> and see how it feels.</p>
  </div>
</section>

{cta("Fly with us",
     "Book a discovery flight and meet your instructor in person.")}
""",
}

# --------------------------------------------------------------- FAA MEDICAL
MEDICAL = {
    "slug": "faa-medical-exam",
    "title": "The FAA Medical Exam, Explained",
    "description": (
        "What to expect from your FAA medical examination — vision, hearing, blood "
        "pressure, cardiovascular, neurological and mental health screening — "
        "explained by SG Flight School."
    ),
    "og_image": "dual-instruction.webp",
    "body": pagehead(
        "The FAA medical exam",
        "A critical step toward your pilot certificate — and less intimidating than "
        "most people expect.",
        image="az-aerial.webp",
    ) + f"""
<section class="section">
  <div class="wrap narrow">
    <div class="disclaimer">
      <p><strong>This is a general outline only.</strong> Specific FAA requirements
         change. Visit <a href="https://www.faa.gov/" rel="noopener">FAA.gov</a> or
         ask your Aviation Medical Examiner for authoritative guidance on your
         situation.</p>
    </div>

    <p>The FAA medical examination is required to obtain or renew a pilot's medical
       certificate, which you need to operate aircraft legally in the United States.
       The exam is conducted by an FAA-designated Aviation Medical Examiner (AME) and
       varies slightly depending on the class of certificate you're applying for
       (First, Second or Third Class). Here's what gets assessed.</p>

    <h3>1. Medical history</h3>
    <p>The AME reviews your medical history: past and present conditions, surgeries,
       medications and visits to healthcare providers. Certain conditions &mdash;
       heart disease, diabetes, mental health conditions or neurological disorders
       &mdash; may require additional documentation or a special issuance.</p>

    <h3>2. Vision</h3>
    <ul>
      <li><strong>Acuity:</strong> 20/20 in each eye, with or without correction, for
          First and Second Class. Third Class requires 20/40 or better.</li>
      <li><strong>Color vision:</strong> you must be able to distinguish aviation
          signal lights and airport lighting systems.</li>
      <li><strong>Peripheral vision</strong> and <strong>near vision</strong> are also tested.</li>
    </ul>

    <h3>3. Hearing</h3>
    <p>You must be able to understand normal spoken conversation. This can be tested
       with a standard audiogram, or simply by repeating spoken words back to the examiner.</p>

    <h3>4. Blood pressure</h3>
    <p>The FAA typically requires 155/95 mmHg or lower. Higher readings may require
       further evaluation.</p>

    <h3>5. Cardiovascular health</h3>
    <p>Depending on your age and certificate class, you may need an electrocardiogram
       (ECG). First Class certificates require an ECG at age 35, and annually after 40.</p>

    <h3>6. Neurological health</h3>
    <p>The examiner checks for signs of neurological disorders such as balance issues,
       tremors or other indicators of nervous system problems.</p>

    <h3>7. Mental health</h3>
    <p>A significant area of focus. The AME reviews your history for psychological
       conditions including depression, anxiety and substance abuse. Some conditions
       are disqualifying, though many can be managed under an FAA-approved treatment plan.</p>

    <h3>8. General physical examination</h3>
    <p>An overall assessment covering the abdomen, skin, lungs and musculoskeletal
       system. Anything unusual may prompt further investigation.</p>

    <h3>9. Urinalysis</h3>
    <p>A screening for indicators such as diabetes or kidney issues.</p>

    <h3>Ready to schedule?</h3>
    <ul>
      <li><a href="https://www.faa.gov/pilots/amelocator" rel="noopener">Find an FAA-authorized AME near you</a></li>
      <li><a href="https://medxpress.faa.gov/" rel="noopener">Create your FAA MedXPress account</a> before your appointment</li>
      <li>Most student pilots need at minimum a <strong>Third-Class Medical Certificate</strong></li>
    </ul>
  </div>
</section>

{cta("Questions about the medical?",
     "We've walked a lot of students through this. Ask us anything — we're happy to "
     "point you in the right direction.")}
""",
}

# ------------------------------------------------------------ FERRY SERVICE
FERRY = {
    "slug": "ferry-service",
    "title": "Aircraft Ferry Service",
    "description": (
        "Nationwide aircraft ferry service from SG Flight School. Experienced pilots "
        "relocate, deliver and transport your aircraft safely across the United States."
    ),
    "og_image": "coastline.webp",
    "schema": [{
        "@context": "https://schema.org",
        "@type": "Service",
        "serviceType": "Aircraft ferry service",
        "provider": {"@id": SITE["url"] + "/#organization"},
        "areaServed": {"@type": "Country", "name": "United States"},
        "description": (
            "Nationwide aircraft ferrying for owners relocating, buying or selling "
            "an aircraft."
        ),
    }],
    "body": pagehead(
        "Aircraft ferry service",
        "Transporting your aircraft with precision and care — anywhere in the "
        "United States.",
        image="coastline.webp",
    ) + f"""
<section class="section">
  <div class="wrap narrow">
    <p class="lead">Whether you're relocating, purchasing or selling an aircraft, our
       pilots combine safety, efficiency and expertise to get your airplane where it
       needs to be.</p>
  </div>
  <div class="wrap" style="margin-top:38px">
    <figure class="shot">
      <img src="/assets/img/coastline.webp" width="1000" height="1333"
           alt="View from a Cessna over the Long Beach, California coastline during a
                cross-country ferry flight" loading="lazy">
      <figcaption>Long Beach, California &mdash; a long way from Falcon Field.
        We ferry aircraft coast to coast.</figcaption>
    </figure>
  </div>
  <div class="wrap" style="margin-top:44px">
    <div class="grid grid--3">
      <div class="card">
        <h3>Expertise you can trust</h3>
        <p>Our experienced pilots handle a wide range of aircraft and navigate
           complex routes, so your plane arrives safely and on time.</p>
      </div>
      <div class="card">
        <h3>Personalized service</h3>
        <p>We tailor each ferry to your needs, provide updates along the way, and
           handle the logistics so you can focus on everything else.</p>
      </div>
      <div class="card">
        <h3>Nationwide coverage</h3>
        <p>Coast to coast, we ferry aircraft throughout the United States &mdash;
           efficiently and without hassle.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap narrow">
    <span class="eyebrow">How it works</span>
    <h2>What to expect</h2>
    <ol class="steps">
      <li>
        <h3>Tell us about the aircraft and the route</h3>
        <p>Make and model, current location, destination, and your timeline. If
           there are known squawks or the aircraft has been sitting, say so &mdash;
           that shapes the plan more than anything else.</p>
      </li>
      <li>
        <h3>We scope the trip and quote it</h3>
        <p>Distance, aircraft performance, fuel stops, weather season and crew
           logistics all factor in. We'll also confirm the aircraft's airworthiness
           documentation and what your insurance requires of a ferry pilot, since
           policies differ on who may act as PIC.</p>
      </li>
      <li>
        <h3>We schedule around the weather</h3>
        <p>Ferry flights get planned with margin. Pushing a light aircraft into
           marginal conditions to hit a date is how ferry flights go wrong, so we
           build in slack and keep you updated if we're holding for weather.</p>
      </li>
      <li>
        <h3>Delivery and handoff</h3>
        <p>We deliver to your destination airport and hand over the aircraft along
           with the logs and anything we noticed en route &mdash; a long
           cross-country tends to surface things a short local flight won't.</p>
      </li>
    </ol>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <figure class="shot shot--wide">
      <img src="/assets/img/ferry-enroute.jpg" width="1400" height="1050"
           alt="En route in a Cessna with another aircraft in sight, crossing the
                Phoenix valley on a cross-country flight" loading="lazy">
      <figcaption>En route, traffic in sight. Ferry flights are planned with
        margin &mdash; for weather, for fuel, and for the unexpected.</figcaption>
    </figure>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap narrow">
    <h2>Common reasons owners call us</h2>
    <ul>
      <li><strong>You just bought an aircraft</strong> out of state and need it
          brought home.</li>
      <li><strong>You're selling</strong> and the buyer wants it delivered.</li>
      <li><strong>You're relocating</strong> and would rather not spend a week of
          vacation flying it yourself.</li>
      <li><strong>The aircraft needs to reach a specific shop</strong> for
          maintenance, avionics work or paint.</li>
      <li><strong>You're not current</strong>, or not comfortable with the route,
          the terrain or the weather &mdash; which is a good call, not a failing.</li>
    </ul>
  </div>
</section>

{cta("Need an aircraft moved?",
     "Tell us the aircraft, the route and your timeline, and we'll get back to you "
     "with a plan and a quote.",
     ("Request a Ferry Quote", "/contact"))}
""",
}

# -------------------------------------------------------------------- ABOUT
ABOUT = {
    "slug": "about",
    "title": "About Us",
    "description": (
        "SG stands for Silly Goose. We believe flight training should be rigorous, "
        "safe and genuinely fun. Meet the flight school at Falcon Field in Mesa, Arizona."
    ),
    "og_image": "az-aerial.webp",
    "body": pagehead(
        "About SG Flight School",
        "Serious training. Genuinely fun. Here's what we stand for.",
        image="sedona.webp",
    ) + f"""
<section class="section">
  <div class="wrap narrow">
    <figure class="shot shot--tall">
      <img src="/assets/img/team-booth.jpg" width="675" height="900" alt="The SG Flight School team at a community event with branded merchandise and the Silly Goose logo" loading="lazy">
      <figcaption>Out in the community. The goose gets everywhere.</figcaption>
    </figure>
    <p class="lead" style="margin-top:34px">At SG Flight School, "SG" stands for <strong>Silly Goose</strong>
       &mdash; a reflection of our belief that learning to fly should be both
       educational and enjoyable.</p>
    <p>We take a light-hearted approach to flight training, creating an environment
       where students feel comfortable and motivated even when things get hard. That
       playful-but-professional ethos means each lesson is informative <em>and</em>
       fun. We combine the joy of flying with a commitment to excellence, so your
       journey to becoming a skilled pilot is as delightful as it is rewarding.</p>
  </div>
  <div class="wrap" style="margin-top:48px">
    <div class="grid grid--2">
      <div class="card">
        <h3>Personalized instruction</h3>
        <p>We tailor training to your needs and learning style so you get the most
           out of every lesson. Our instructors adapt their methods to keep you
           motivated and excited about learning.</p>
      </div>
      <div class="card">
        <h3>Safety first</h3>
        <p>We prioritize safety above everything &mdash; and we also believe a
           positive, low-stress environment produces better pilots. Rigorous safety
           protocols let you focus on flying and on mastering new skills.</p>
      </div>
      <div class="card">
        <h3>Diverse learning environments</h3>
        <p>We train in a range of conditions and environments to prepare you for
           real-world flying. It sharpens your skills and keeps training dynamic.</p>
      </div>
      <div class="card">
        <h3>Fun through challenges</h3>
        <p>Not every moment of flight training is easy. Our instructors use
           encouragement, creative problem-solving and a sense of humor to help you
           work through the hard parts without losing the joy of flying.</p>
      </div>
      <div class="card">
        <h3>Goal-oriented</h3>
        <p>Achieving your aviation goals matters to us, and so does enjoying the
           process. We celebrate your milestones because progress deserves to be marked.</p>
      </div>
      <div class="card">
        <h3>Student-first, always</h3>
        <p>We make the most of your time and money, give clear guidance and
           strategies for success, and minimize the frustrations that too often come
           with flight training.</p>
      </div>
    </div>
  </div>
</section>

{cta("Come see if we're a fit",
     "The best way to know whether a flight school is right for you is to fly with "
     "them. Start with a discovery flight.")}
""",
}

# ------------------------------------------------------------------ CONTACT
CONTACT = {
    "slug": "contact",
    "title": "Contact Us",
    "description": (
        "Contact SG Flight School at Falcon Field Airport in Mesa, Arizona. Call, "
        "email, or book a discovery flight online."
    ),
    "og_image": "az-aerial.webp",
    "body": pagehead(
        "We'd love to hear from you",
        "Questions about exploring the skies or starting your flying adventure? "
        "Reach out — we're here to help.",
        image="az-aerial.webp",
    ) + f"""
<section class="section">
  <div class="wrap">
    <div class="contact-grid">
      <div>
        <h2>Get in touch</h2>
        <ul class="contact-list">
          <li>
            <span class="label">Phone</span>
            <span class="value">{phone_html()}</span>
          </li>
          <li>
            <span class="label">Email</span>
            <span class="value"><a href="mailto:{EMAIL}">{EMAIL}</a></span>
          </li>
          <li>
            <span class="label">Where to find us</span>
            <span class="value">{address_html()}</span>
            <p style="margin:.5em 0 0;font-size:.95rem">We fly out of
               <a href="{SITE['airport_url']}" rel="noopener">Falcon Field Airport (KFFZ)</a>
               in Mesa, serving Phoenix, Scottsdale, Gilbert, Chandler and Tempe.</p>
          </li>
          <li>
            <span class="label">Current students</span>
            <span class="value"><a href="{SCHED}" rel="noopener">Log in to FlightCircle</a></span>
            <p style="margin:.5em 0 0;font-size:.95rem">Already training with us? Book
               aircraft and instructor time in FlightCircle, our scheduling system.
               New to SG? <a href="{BOOK}">Start here instead.</a></p>
          </li>
        </ul>
      </div>
      <div>
        <h2>Ready to fly?</h2>
        <p>The quickest way to get started is to book a discovery flight. It's $199,
           takes about an hour, and you'll be flying the airplane yourself.</p>
        <div class="btn-row" style="margin-bottom:28px">
          <a class="btn btn--primary" href="{BOOK}">Book a Discovery Flight</a>
        </div>
        <img src="/assets/img/student-controls.webp" width="750" height="562"
             alt="An SG Flight School student flying a Cessna 172 over the Arizona desert"
             style="border-radius:12px" loading="lazy">
      </div>
    </div>
  </div>
</section>
""",
}

# ---------------------------------------------------------------------- FAQ
# Answers are built only from facts we can support: SG's published rates, the
# aircraft, the location, and FAA regulation. Anything business-specific that
# hasn't been confirmed by the owner is deliberately absent — see README.
FAQ_DATA = [
    ("How much does it cost to get a private pilot license?",
     "Honestly, it depends on you &mdash; but here's the real math instead of a "
     "vague answer. The FAA minimum is 40 flight hours, though the national "
     "average is closer to 60&ndash;70 because most people need repetition to get "
     "comfortable. At our rates, budget roughly:"
     "<ul>"
     "<li><strong>Aircraft:</strong> 60 hours &times; $160&ndash;165/hour wet "
     "&asymp; $9,600&ndash;9,900</li>"
     "<li><strong>Instruction:</strong> about 45 hours &times; $60/hour "
     "&asymp; $2,700</li>"
     "<li><strong>Ground school:</strong> $300&ndash;500 for a self-paced online "
     "course, more if you do it one-on-one with your instructor</li>"
     "<li><strong>Written test:</strong> around $175, paid at the testing center</li>"
     "<li><strong>Checkride:</strong> paid directly to the examiner, commonly "
     "$800&ndash;1,200 in the Phoenix area</li>"
     "<li><strong>Headset, charts, supplies:</strong> $300&ndash;1,000 depending "
     "on how nice a headset you want</li>"
     "</ul>"
     "<p>That puts a realistic total somewhere around "
     "<strong>$14,000&ndash;16,000</strong>. You don't pay it up front &mdash; you "
     "pay per lesson as you go, which is how most students spread the cost over "
     "months. Anyone quoting you the FAA-minimum figure is quoting a number almost "
     "nobody actually hits.</p><p><a href=\"/cost-of-private-pilot-license-arizona\">Full cost breakdown, including what makes it cheaper or more expensive.</a></p>"),

    ("How long does it take?",
     "Most students finish in <strong>6 to 12 months</strong>. The single biggest "
     "factor is how often you fly. Two lessons a week and you'll move steadily; "
     "once every few weeks and you'll spend the first part of each lesson "
     "re-learning what you forgot, which costs both time and money. If you can "
     "fly consistently, do &mdash; it's genuinely cheaper."),

    ("Do I need a medical certificate before I start?",
     "Not to start, but don't wait. FAA medical review can take months if anything "
     "in your history needs a closer look, so schedule the exam early and begin "
     "ground and flight training while it's processing. You'll need at minimum a "
     "Third-Class Medical Certificate before you fly solo. "
     "<a href=\"/faa-medical-exam\">Here's what the exam covers.</a>"),

    ("How old do I have to be?",
     "The FAA sets the floor: you must be <strong>16 to fly solo</strong> and "
     "<strong>17 to earn a private pilot certificate</strong>. There's no minimum "
     "age to start taking lessons, and no upper limit at all &mdash; as long as you "
     "can pass a medical, you can learn to fly."),

    ("What is a discovery flight, exactly?",
     "It's a real flight, not a tour. You sit in the left seat with a certified "
     "flight instructor, they walk you through the controls, and you fly the "
     "airplane yourself. It's $199, takes about an hour including the preflight "
     "briefing, and requires no experience or medical certificate. It's the "
     "cheapest way to find out whether flying is for you before committing to "
     "anything."),

    ("Can I rent your aircraft if I already have a certificate?",
     "Yes. Both aircraft are available for rental at $160&ndash;165 per hour wet. "
     "You'll need a checkout with one of our instructors first &mdash; standard "
     "practice at every flight school, and it's about making sure you're "
     "comfortable in that specific airplane. "
     "<a href=\"/contact\">Get in touch</a> about current checkout requirements."),

    ("What does \"wet\" mean in your rates?",
     "&quot;Wet&quot; means fuel is included in the hourly rate, so you're not "
     "paying separately at the pump. Instruction is billed on top at $60/hour. So "
     "an hour of dual instruction in Kraken runs $165 + $60 = $225."),

    ("Where exactly are you located?",
     "Falcon Field Airport (KFFZ) in Mesa, Arizona &mdash; Hangar 120 at "
     "4800 E Falcon Dr. We're convenient to Phoenix, Scottsdale, Gilbert, Chandler "
     "and Tempe, and Falcon Field's towered airspace and busy pattern make it a "
     "genuinely good place to learn."),

    ("Do I need to buy an airplane or expensive gear to start?",
     "No. Come to your first lesson with nothing. Eventually you'll want your own "
     "headset &mdash; borrowed ones get uncomfortable &mdash; and a logbook, but "
     "there's no reason to spend money on equipment before you know you're going to "
     "stick with it."),

    ("What if I get airsick or find out I'm scared of heights?",
     "Both are more common than people admit, and neither is disqualifying. Fear of "
     "heights in particular rarely transfers to flying &mdash; it's tied to a sense "
     "of falling that a stable aircraft doesn't produce. Airsickness usually fades "
     "as you get used to the motion and to being the one in control. Tell your "
     "instructor; they've seen it before and can adjust how they fly the lesson."),
]


def faq_items():
    out = []
    for i, (q, a) in enumerate(FAQ_DATA):
        body = a if a.strip().startswith("<") and "<p>" in a else f"<p>{a}</p>"
        if not a.strip().startswith("<p") and "<ul>" not in a:
            body = f"<p>{a}</p>"
        out.append(f"""
      <details class="faq"{' open' if i == 0 else ''}>
        <summary>{q}</summary>
        <div class="faq__body">{body}</div>
      </details>""")
    return "".join(out)


def faq_plain(a):
    """Strip tags for the JSON-LD answer text."""
    import re as _re
    import html as _html
    t = _re.sub(r"<[^>]+>", " ", a)
    t = _html.unescape(t)
    return _re.sub(r"\s+", " ", t).strip()


FAQ = {
    "slug": "faq",
    "title": "Flight Training FAQ",
    "description": (
        "What flight training actually costs in Mesa, AZ, how long it takes, "
        "medical requirements, age limits and aircraft rental — straight answers "
        "from SG Flight School at Falcon Field."
    ),
    "og_image": "student-smile.webp",
    "schema": [{
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": faq_plain(a)},
            }
            for q, a in FAQ_DATA
        ],
    }],
    "body": pagehead(
        "Questions people actually ask",
        "Straight answers about cost, timelines and requirements — including the "
        "numbers most flight schools would rather you didn't ask about up front.",
        image="dual-instruction.webp",
    ) + f"""
<section class="section">
  <div class="wrap narrow">
    {faq_items()}
    <p style="margin-top:36px;color:#6b7a88;font-size:.95rem">
      Cost figures are realistic estimates based on our published rates and typical
      student experience, not quotes. Third-party costs &mdash; examiner fees,
      testing centers, ground school &mdash; are set by those providers and change.
      <a href="/contact">Ask us</a> and we'll walk through your specific situation.</p>
  </div>
</section>

{cta("Still have a question?",
     "Ask us anything — there are no bad questions, and we would much rather "
     "answer them before you spend money than after.")}
""",
}

# ----------------------------------------------------------------- LOCATIONS
# One page per East Valley city we draw students from. These are deliberately
# NOT templated: Google treats near-identical location pages as doorway pages
# and discounts or penalises them. Each page answers a question specific to that
# city — usually "why drive here instead of the field down the road" — and every
# airport comparison below is factual.


def location_page(slug, city, title, desc, lede, body, image="sedona.webp"):
    return {
        "slug": slug,
        "title": title,
        "description": desc,
        "og_image": "az-aerial.webp",
        "body": pagehead(f"Flight training for {city}", lede, image=image) + body + cta(
            "Come fly with us",
            f"Book a $199 discovery flight from Falcon Field — about a "
            f"{city}-to-cockpit trip worth making.",
        ),
    }


GILBERT = location_page(
    "flight-school-gilbert-az", "Gilbert",
    "Flight School Near Gilbert, AZ",
    "Learn to fly near Gilbert, AZ. Discovery flights from $199, private pilot "
    "and instrument training at Falcon Field (KFFZ) — a short drive up the 202.",
    "Gilbert has no airport of its own — Falcon Field is the closest full-service "
    "flight training you'll find, straight up the Loop 202.",
    """
<section class="section">
  <div class="wrap narrow">
    <h2>Getting here from Gilbert</h2>
    <p>Gilbert is one of the fastest-growing towns in Arizona and has plenty of
       everything &mdash; except an airport. For flight training that means
       heading out of town, and Falcon Field is the practical choice for most of
       Gilbert. Take the Loop 202 Santan to the Red Mountain, exit toward
       Greenfield or Higley, and you're at the field. From most Gilbert
       neighborhoods that's a straightforward drive with no surface-street
       crawl.</p>
    <p>That matters more than it sounds. Flight training works best when you fly
       two or three times a week, and the schools people actually stick with are
       the ones they don't dread driving to. A predictable freeway run beats a
       marginally closer field you have to fight traffic to reach.</p>

    <h2>Why Gilbert students choose Falcon Field</h2>
    <p>Falcon Field is a towered airport with a genuinely busy pattern. That's an
       advantage when you're learning: you'll talk to a control tower from your
       very first lessons, sequence with other traffic, and get comfortable with
       radio work that intimidates pilots trained at quieter fields. Students who
       learn here tend to find towered airports unremarkable, because they've
       been doing it since the beginning.</p>
    <p>You're also minutes from open practice areas to the northeast, so you
       aren't burning expensive Hobbs time transiting to somewhere you can
       actually work on maneuvers.</p>

    <h2>What training looks like</h2>
    <p>Most Gilbert students start with a <a href="/courses">$199 discovery
       flight</a> &mdash; a real flight where you fly the airplane, not a tour.
       From there it's typically a <a href="/courses">private pilot
       certificate</a> over six to twelve months, depending how often you fly.
       We're upfront about what it costs: our
       <a href="/faq">cost and timeline FAQ</a> lays out the real numbers rather
       than quoting an FAA minimum almost nobody hits.</p>
    <p>Training happens in two <a href="/aircraft">Cessna 172 SkyHawks</a>, one
       with dual Garmin G5s and a Garmin GNS 650 for instrument work.</p>
  </div>
</section>
<section class="section section--alt">
  <div class="wrap narrow">
    <figure class="shot">
      <img src="/assets/img/sedona-trip.jpg" width="1100" height="825"
           alt="Two SG Flight School students beside N1287U on the ramp at Sedona,
                red rock cliffs behind them"
           loading="lazy">
      <figcaption>Sedona is about 45 minutes away by air. Students fly there on
        cross-countries — it is a long drive and a short, spectacular flight.</figcaption>
    </figure>
  </div>
</section>
""")

SCOTTSDALE = location_page(
    "flight-school-scottsdale-az", "Scottsdale",
    "Flight School Near Scottsdale, AZ",
    "Flight training for Scottsdale at Falcon Field (KFFZ) in Mesa. An honest "
    "comparison with Scottsdale Airport, plus $199 discovery flights.",
    "Scottsdale has its own airport, so here's the honest case for driving to "
    "Falcon Field instead.",
    """
<section class="section">
  <div class="wrap narrow">
    <h2>You already have an airport &mdash; why come here?</h2>
    <p>Scottsdale Airport (KSDL) is close, well run, and busy with corporate
       traffic. If it's five minutes from your door, training there is a
       perfectly reasonable choice and we won't pretend otherwise.</p>
    <p>What Falcon Field offers is a different mix. KSDL's traffic skews heavily
       toward jets and turboprops, which means training aircraft spend more time
       waiting and more time being sequenced around much faster arrivals. Falcon
       Field's traffic is overwhelmingly general aviation and training, so the
       pattern moves at a pace that suits a Cessna 172. Less holding, less
       waiting, more of your Hobbs time spent flying.</p>
    <p>The other honest difference is cost. Costs at a field dominated by
       corporate operations tend to be higher across the board. We publish our
       rates &mdash; <a href="/aircraft">$160&ndash;165/hour wet</a> plus $60/hour
       instruction &mdash; and our full
       <a href="/faq">cost breakdown</a>. Compare directly and decide.</p>

    <h2>The drive</h2>
    <p>From South Scottsdale it's a short run down the Loop 101 to the Red
       Mountain 202 east. From North Scottsdale it's longer, and if you're up
       near the 101/Pima corridor, KSDL genuinely may make more sense. We'd
       rather tell you that than have you commit to a drive you'll resent by
       lesson fifteen.</p>

    <h2>What you get here</h2>
    <p>A small school where you fly with the same instructor rather than whoever
       is on the roster, a training plan built around your schedule, and two
       well-equipped <a href="/aircraft">Cessna 172s</a>. We train
       <a href="/courses">private, instrument, commercial and CFI</a>
       candidates, and we're straightforward about
       <a href="/faq">what it costs and how long it takes</a>.</p>
    <p>Start with a <a href="/courses">$199 discovery flight</a> and see whether
       the drive is worth it before committing to anything.</p>
  </div>
</section>
<section class="section section--alt">
  <div class="wrap narrow">
    <figure class="shot">
      <img src="/assets/img/sedona-trip.jpg" width="1100" height="825"
           alt="Two SG Flight School students beside N1287U on the ramp at Sedona,
                red rock cliffs behind them"
           loading="lazy">
      <figcaption>Sedona is about 45 minutes away by air. Students fly there on
        cross-countries — it is a long drive and a short, spectacular flight.</figcaption>
    </figure>
  </div>
</section>
""")

CHANDLER = location_page(
    "flight-school-chandler-az", "Chandler",
    "Flight School Near Chandler, AZ",
    "Flight training for Chandler at Falcon Field (KFFZ) in Mesa. Towered-field "
    "training, published rates, and how we compare to Chandler Municipal.",
    "Chandler Municipal is closer — but it's untowered, and that shapes the "
    "pilot you become.",
    """
<section class="section">
  <div class="wrap narrow">
    <h2>Towered versus untowered training</h2>
    <p>Chandler Municipal (KCHD) is a good airport and it's closer to you. The
       meaningful difference is that it's untowered, and Falcon Field is
       towered.</p>
    <p>Pilots trained entirely at untowered fields are often uneasy the first
       time they have to work a control tower &mdash; the radio work is
       unfamiliar, and it tends to show up exactly when they want to fly
       somewhere interesting. Training at a towered field from day one inverts
       that. You'll be talking to Falcon Tower on your earliest lessons, and
       towered airports will feel routine by the time you're flying
       cross-country.</p>
    <p>None of which makes untowered flying unimportant &mdash; you'll learn
       that too, at the quieter fields nearby. The point is getting both, with
       the harder one becoming second nature first.</p>

    <h2>Getting here from Chandler</h2>
    <p>Loop 101 Price north to the Red Mountain 202 east, then out toward
       Greenfield or Higley. It's a real drive, and worth being realistic about:
       if you're flying twice a week, that's a commitment. Plenty of our
       students make it, but factor it in honestly before you start.</p>

    <h2>What training costs</h2>
    <p>We publish real numbers instead of making you ask. Aircraft are
       <a href="/aircraft">$160&ndash;165/hour wet</a>, instruction is $60/hour,
       and our <a href="/faq">FAQ</a> walks through a realistic
       all-in total for a private pilot certificate &mdash; including the
       third-party costs most schools leave out, like the examiner fee and the
       written test.</p>
    <p>A <a href="/courses">$199 discovery flight</a> is the sensible first step.
       You'll fly the airplane yourself, and you'll know quickly whether the
       drive from Chandler is one you want to make regularly.</p>
  </div>
</section>
<section class="section section--alt">
  <div class="wrap narrow">
    <figure class="shot">
      <img src="/assets/img/falcon-sunset.jpg" width="1600" height="1200" alt="N1287U on the Falcon Field ramp at sunset, with the runway 4R-22L sign lit behind it" loading="lazy">
      <figcaption>Evening at Falcon Field. Winter is the best flying weather Arizona has, and the light at the end of the day is worth showing up for.</figcaption>
    </figure>
  </div>
</section>
""",
    image="az-aerial.webp")

TEMPE = location_page(
    "flight-school-tempe-az", "Tempe",
    "Flight School Near Tempe, AZ",
    "Flight training for Tempe at Falcon Field (KFFZ) in Mesa. Flexible "
    "scheduling around classes and work, with $199 discovery flights.",
    "A straight run east on the 202, with scheduling that bends around classes "
    "and shift work.",
    """
<section class="section">
  <div class="wrap narrow">
    <h2>Tempe to Falcon Field</h2>
    <p>Tempe has no general aviation airport &mdash; Sky Harbor is Class B
       airspace and not a training environment. The Red Mountain 202 runs east
       from Tempe more or less directly to Falcon Field, which makes this one of
       the more straightforward drives in the Valley.</p>

    <h2>If you're a student, or working around a schedule</h2>
    <p>A lot of Tempe interest comes from ASU students and people working
       schedules that don't resemble nine to five. Two things matter for you.</p>
    <p>First, <strong>scheduling flexibility.</strong> We build training around
       your availability rather than fixed blocks. Early mornings are usually the
       best flying of the day in Arizona anyway &mdash; smooth air, cooler
       temperatures, better aircraft performance &mdash; and they tend to fit
       around classes well.</p>
    <p>Second, <strong>honest cost planning.</strong> If you're funding this
       yourself, you need real numbers, not a brochure figure. Our
       <a href="/faq">cost FAQ</a> lays out what a private pilot certificate
       actually runs, why the FAA's 40-hour minimum is not what most people
       finish in, and where the money goes. You pay lesson by lesson, so it
       spreads across months rather than landing all at once.</p>

    <h2>If you're aiming at a career</h2>
    <p>If the goal is flying professionally, the path runs private, then
       instrument, then commercial, then usually
       <a href="/courses">CFI</a> to build hours while getting paid. We train all
       of it. Worth being clear-eyed: this is a long, expensive road, and it's
       worth talking through the whole sequence before you spend anything.
       <a href="/contact">Ask us</a> and we'll be straight with you.</p>
    <p>Start with a <a href="/courses">$199 discovery flight</a>.</p>
  </div>
</section>
<section class="section section--alt">
  <div class="wrap narrow">
    <figure class="shot">
      <img src="/assets/img/sedona-trip.jpg" width="1100" height="825"
           alt="Two SG Flight School students beside N1287U on the ramp at Sedona,
                red rock cliffs behind them"
           loading="lazy">
      <figcaption>Sedona is about 45 minutes away by air. Students fly there on
        cross-countries — it is a long drive and a short, spectacular flight.</figcaption>
    </figure>
  </div>
</section>
""")

PHOENIX = location_page(
    "flight-school-phoenix-az", "Phoenix",
    "Flight School Near Phoenix, AZ",
    "Flight training for Phoenix at Falcon Field (KFFZ) in Mesa. A small, "
    "student-first alternative to the Valley's large academies.",
    "A small school in the East Valley, and an honest comparison with the "
    "Valley's bigger options.",
    """
<section class="section">
  <div class="wrap narrow">
    <h2>Where Phoenix pilots learn</h2>
    <p>The Valley has no shortage of options. Deer Valley (KDVT) is one of the
       busiest general aviation airports in the country, Glendale and Goodyear
       serve the West Valley, and there are large academies scattered across the
       metro. If you live in west Phoenix, one of those is probably closer.</p>
    <p>Falcon Field sits on the east side, and makes most sense if you're in
       central or east Phoenix, or already heading that direction. The Red
       Mountain 202 is the route.</p>

    <h2>Small school, or big academy?</h2>
    <p>This is the real decision, and it matters more than geography.</p>
    <p>Large academies run structured programs with many aircraft and many
       instructors. That suits people who want a defined timeline and don't mind
       being one of a large cohort. The tradeoff is that you often fly with
       whoever is available, and instructor turnover is high &mdash; many are
       building hours toward an airline job and will leave mid-training.</p>
    <p>We're the other thing. You fly with the same instructor, on a plan built
       around your schedule, in one of two <a href="/aircraft">aircraft</a> you
       will get to know well. That means more consistency and less repeated
       ground covered &mdash; but also less capacity, so we can't absorb an
       unlimited number of students or promise a fixed finish date.</p>
    <p>Neither model is better in the abstract. But if you've been put off by
       feeling like a number, or you've started training somewhere and stalled
       out, this is worth a look.</p>

    <h2>What we're upfront about</h2>
    <p>Our rates are published. Our <a href="/faq">cost FAQ</a> gives a realistic
       all-in figure for a private pilot certificate instead of the FAA minimum.
       We'll tell you when a different school is a better fit for you &mdash;
       including when the drive doesn't make sense.</p>
    <p>A <a href="/courses">$199 discovery flight</a> is the low-commitment way to
       find out.</p>
  </div>
</section>
<section class="section section--alt">
  <div class="wrap narrow">
    <figure class="shot shot--tall">
      <img src="/assets/img/first-solo.jpg" width="675" height="900" alt="A student celebrating on the cowling of N1287U with the Falcon Field control tower behind" loading="lazy">
      <figcaption>First solo. Whatever brought you to a flight school in the first place, this is the moment it becomes real.</figcaption>
    </figure>
  </div>
</section>
""",
    image="ferry-enroute.jpg")


# ------------------------------------------------------------------ COST
# Standalone page for the highest-intent search in the category:
# "how much does it cost to get a private pilot license". The numbers are the
# same honest ones as the FAQ, but expanded and given a URL that can rank.
# Figures derive from SG's published rates — see FAQ_DATA for the short version.
COST_QA = [
    ("How much does a private pilot license cost in Arizona?",
     "Realistically $14,000 to $16,000 at SG Flight School's rates, assuming "
     "about 60 hours of flight time. The FAA minimum of 40 hours would come to "
     "roughly $10,000, but very few people finish in 40 hours."),
    ("Do I have to pay it all up front?",
     "No. You pay lesson by lesson as you go, which spreads the cost over the "
     "six to twelve months most students take. There is no package to buy and "
     "no deposit to put down."),
    ("Why do most people need more than the FAA's 40 hours?",
     "The 40-hour minimum assumes near-perfect retention and no weather delays. "
     "The national average is closer to 60-70 hours. Flying frequently is the "
     "single biggest thing that keeps your total near the lower end."),
    ("What is the cheapest way to get a private pilot license?",
     "Fly often, use a self-paced online ground school, choose the lower-cost "
     "aircraft, and arrive prepared for each lesson. Frequency matters more "
     "than any other single factor — long gaps mean re-learning, and "
     "re-learning is what makes training expensive."),
]

COST = {
    "slug": "cost-of-private-pilot-license-arizona",
    "title": "How Much Does a Private Pilot License Cost in Arizona? (2026)",
    "description": (
        "Real 2026 numbers for a private pilot license in Arizona — aircraft, "
        "instruction, ground school, written test, checkride and supplies broken "
        "out, from a flight school that publishes its rates."
    ),
    "og_image": "student-controls.webp",
    "schema": [{
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in COST_QA
        ],
    }],
    "body": pagehead(
        "What a private pilot license actually costs",
        "Real numbers, updated for 2026 — not an FAA-minimum figure that almost "
        "nobody hits.",
        image="student-controls.webp",
    ) + f"""
<section class="section">
  <div class="wrap narrow">
    <div class="callout">
      <h2 style="margin-top:0">The short answer</h2>
      <p style="margin-bottom:0"><strong>Budget $14,000&ndash;16,000.</strong>
         That assumes about 60 hours of flight time at our published rates, and
         it includes the third-party costs most schools leave out of their
         estimates &mdash; the written test, the examiner's fee, and your
         medical.</p>
    </div>

    <h2>Where the money goes</h2>
    <table class="rate-table">
      <thead>
        <tr><th>Item</th><th>Typical cost</th><th>Notes</th></tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Aircraft</strong><br><span class="rate-table__sub">~60 hours</span></td>
          <td>$9,600&ndash;9,900</td>
          <td>$160&ndash;165/hour wet. "Wet" means fuel is included.</td>
        </tr>
        <tr>
          <td><strong>Flight instruction</strong><br><span class="rate-table__sub">~45 hours</span></td>
          <td>$2,700</td>
          <td>$60/hour. Only the dual hours &mdash; solo time has no instructor charge.</td>
        </tr>
        <tr>
          <td><strong>Ground school</strong></td>
          <td>$300&ndash;500</td>
          <td>Self-paced online. More if you do it one-on-one with your instructor.</td>
        </tr>
        <tr>
          <td><strong>FAA medical exam</strong></td>
          <td>$100&ndash;200</td>
          <td>Paid to the Aviation Medical Examiner. <a href="/faa-medical-exam">What the exam covers.</a></td>
        </tr>
        <tr>
          <td><strong>FAA written test</strong></td>
          <td>~$175</td>
          <td>Paid at the testing center.</td>
        </tr>
        <tr>
          <td><strong>Checkride</strong></td>
          <td>$800&ndash;1,200</td>
          <td>Paid directly to the Designated Pilot Examiner. Phoenix-area rate.</td>
        </tr>
        <tr>
          <td><strong>Headset &amp; supplies</strong></td>
          <td>$300&ndash;1,000</td>
          <td>Mostly the headset. A used one is a perfectly good place to start.</td>
        </tr>
      </tbody>
      <tfoot>
        <tr><td><strong>Realistic total</strong></td>
            <td><strong>$14,000&ndash;16,000</strong></td>
            <td>Spread over 6&ndash;12 months, paid lesson by lesson.</td></tr>
      </tfoot>
    </table>
    <p class="rate-table__note">Our rates are published on the
       <a href="/aircraft">fleet page</a>. Third-party costs &mdash; examiner,
       testing center, medical, ground school &mdash; are set by those providers
       and change; the ranges above are what students are currently paying in the
       Phoenix area.</p>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap narrow">
    <h2>Why the "40 hours" number is misleading</h2>
    <p>The FAA sets a 40-hour minimum for a private pilot certificate. You will
       see schools quote a total based on it. At our rates that would be around
       <strong>$10,000</strong> &mdash; and it is not a number most people should
       plan around.</p>
    <p>Forty hours assumes you retain everything between lessons, never lose a
       day to weather or maintenance, and are ready for your checkride the moment
       you hit the minimum. The national average is closer to
       <strong>60&ndash;70 hours</strong>. We would rather tell you that up front
       than surprise you at hour 45.</p>

    <h2>What actually changes the total</h2>
    <div class="grid grid--2" style="margin-top:26px">
      <div class="card">
        <h3>Flying frequently makes it cheaper</h3>
        <p>This is the biggest lever by a wide margin. Two lessons a week and
           you build on the last one. Once every three weeks and you spend the
           first half of each lesson recovering ground you already paid for.</p>
      </div>
      <div class="card">
        <h3>Starting and stopping makes it expensive</h3>
        <p>Long breaks are what turn a $14,000 certificate into a $20,000 one.
           If money is tight, it is better to pause deliberately and resume
           properly than to stretch lessons thin.</p>
      </div>
      <div class="card">
        <h3>Preparation is free and saves money</h3>
        <p>Chair-fly the maneuvers, review the lesson beforehand, know the
           checklist. Time spent on the ground costs nothing; the same learning
           in the air costs $220 an hour.</p>
      </div>
      <div class="card">
        <h3>Get your medical early</h3>
        <p>FAA medical review can take months if anything in your history needs a
           second look. Start it before you need it, and it never becomes the
           thing holding up your solo.</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap narrow">
    <figure class="shot" style="margin:6px 0 40px">
      <img src="/assets/img/kraken-ramp.jpg" width="1100" height="825"
           alt="N61574 on the ramp at Falcon Field with a pilot standing beside it"
           loading="lazy">
      <figcaption>N61574 &mdash; $165 an hour wet, and the aircraft most of these
        numbers are based on.</figcaption>
    </figure>

    <h2>What the other certificates cost</h2>
    <table class="rate-table">
      <thead><tr><th>Certificate</th><th>Typical total</th><th>What that assumes</th></tr></thead>
      <tbody>
        <tr><td><strong>Discovery flight</strong></td><td>$199</td>
            <td>One flight, about an hour. Nothing else to pay.</td></tr>
        <tr><td><strong>Private (PPL)</strong></td><td>$14,000&ndash;16,000</td>
            <td>~60 hours total. Broken down in the table above.</td></tr>
        <tr><td><strong>Instrument (IFR)</strong></td><td>$10,000&ndash;14,000</td>
            <td>40+ hours instrument time, mostly dual, plus written and checkride.</td></tr>
        <tr><td><strong>Commercial (CPL)</strong></td><td>$5,500&ndash;8,500<br>
            <span class="rate-table__sub">training only</span></td>
            <td>Plus time building to 250 total hours &mdash; usually the larger
                cost. See the note below.</td></tr>
        <tr><td><strong>Flight instructor (CFI)</strong></td><td>$6,000&ndash;9,000</td>
            <td>20&ndash;30 hours dual, two written tests, and a checkride that
                runs higher than most.</td></tr>
      </tbody>
    </table>

    <h3>Why commercial is quoted differently</h3>
    <p>A commercial certificate requires <strong>250 total flight hours</strong>.
       The instruction itself is a small part of that. If you finish your
       instrument rating around 120 hours, you still need roughly 130 more
       &mdash; about <strong>$21,000</strong> of flying at our rates, though most
       people build hours more cheaply by sharing costs with other pilots.</p>
    <p>There is also a requirement for 10 hours in a complex or technically
       advanced airplane. Our 172s don't qualify, so those hours happen
       elsewhere &mdash; we'll help you arrange them.
       <a href="/courses">More on the courses.</a></p>

    <h2>How you pay</h2>
    <p>Lesson by lesson. You are billed for the aircraft time you fly (metered by
       the Hobbs meter, which runs with the engine) plus your instructor's time.
       There is no package to buy, no deposit, and nothing to finance through us.</p>
    <p>In practice most students spend somewhere between $800 and $1,500 a month
       while training steadily. If that pace does not fit, flying less often
       still works &mdash; it just costs more in total, and it is worth going in
       with your eyes open about that trade.</p>

    <h2>Start with $199</h2>
    <p>Before committing to any of this, take a
       <a href="/book">discovery flight</a>. It is $199, takes about an hour, and
       you will fly the airplane yourself with an instructor beside you. No
       experience and no medical certificate required. It is the cheapest way to
       find out whether the rest of this is for you.</p>
    <p>Questions about your specific situation? <a href="/contact">Ask us</a>
       &mdash; we would much rather talk it through before you spend anything.
       There is more on timelines and requirements in our
       <a href="/faq">FAQ</a>.</p>
  </div>
</section>

{cta("Find out if flying is for you",
     "A $199 discovery flight answers the question better than any amount of "
     "reading.")}
""",
}


# ------------------------------------------------------------------ GALLERY
# Dimensions are read from the files at build time so they can never drift from
# what's actually on disk — that mismatch causes layout shift.
GALLERY = [
    ("falcon-sunset.jpg", "N1287U on the Falcon Field ramp at sunset, runway 4R-22L sign behind",
     "Evening on the ramp at Falcon Field."),
    ("first-solo.jpg", "A student celebrating on the cowling of N1287U, control tower behind",
     "First solo. Nothing else in training feels like it."),
    ("first-solo-2.jpg", "A student sitting on the cowling of N1287U at dusk, control tower behind",
     "Same evening, once it had sunk in."),
    ("kraken-ramp.jpg", "N61574 on the ramp at Falcon Field with a pilot standing beside it",
     "N61574 &mdash; “Kraken”. Dual Garmin G5s and a GNS 650."),
    ("nessie-sunset.jpg", "N1287U at sunset with the cabin door open",
     "N1287U &mdash; “Nessie”. The most affordable way to build hours in our fleet."),
    ("backcountry.jpg", "N1287U parked at a remote Arizona airstrip at golden hour with a tent beside it",
     "A licence is a door. Strips you can only reach by air are what's behind it."),
    ("sedona-trip.jpg", "Two students beside N1287U on the ramp at Sedona, red rock cliffs behind",
     "Sedona &mdash; a long drive, a short and spectacular flight."),
    ("sedona.webp", "View from a Cessna wing over the red rocks near Sedona, Arizona",
     "Sedona from the air."),
    ("az-aerial.webp", "Aerial view over the Superstition Mountains and Salt River near Mesa",
     "The Superstitions and the Salt River, a few minutes from the field."),
    ("ferry-enroute.jpg", "En route in a Cessna with another aircraft in sight over the Phoenix valley",
     "En route, traffic in sight."),
    ("coastline.webp", "View from a Cessna over the Long Beach, California coastline",
     "Long Beach, California. We ferry aircraft coast to coast."),
    ("night-flight.jpg", "City lights seen from the air at night during a night training flight",
     "Night flying. Required for your certificate, and worth it on its own."),
    ("dual-instruction.webp", "An instructor and student in the cockpit of a Cessna 172 on approach",
     "On approach, dual instruction."),
    ("student-controls.webp", "A student flying a Cessna 172 over the Arizona desert",
     "Hands on the yoke. That happens on your first flight, not your tenth."),
    ("student-smile.webp", "A smiling student in the cockpit before takeoff",
     "Before takeoff on a discovery flight."),
    ("team-booth.jpg", "The SG Flight School team at a community event with branded merchandise",
     "Out in the community. The goose gets everywhere."),
    ("jensen.jpg", "Jensen Beard, Certified Flight Instructor, flying a Cessna above the clouds",
     "Jensen Beard, CFI."),
]


def gallery_grid():
    import os as _os
    import re as _re
    import subprocess as _sp
    base = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "site", "assets", "img")
    out = []
    for src, alt, cap in GALLERY:
        path = _os.path.join(base, src)
        if not _os.path.exists(path):
            continue
        try:
            info = _sp.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", path],
                           capture_output=True, text=True).stdout
            w = int(_re.search(r"pixelWidth: (\d+)", info).group(1))
            h = int(_re.search(r"pixelHeight: (\d+)", info).group(1))
        except Exception:
            w = h = 0
        portrait = " gal__item--tall" if h > w else ""
        dims = f' width="{w}" height="{h}"' if w else ""
        out.append(f"""
      <figure class="gal__item{portrait}">
        <button type="button" class="gal__btn" data-full="/assets/img/{src}"
                data-cap="{cap}" aria-label="View larger: {cap}">
          <img src="/assets/img/{src}"{dims} alt="{alt}" loading="lazy">
        </button>
        <figcaption>{cap}</figcaption>
      </figure>""")
    return "".join(out)


GALLERY_PAGE = {
    "slug": "gallery",
    "title": "Photo Gallery",
    "description": (
        "Photographs from SG Flight School at Falcon Field in Mesa, Arizona — our "
        "Cessna 172s, students on their first solo, and where flying around Arizona "
        "actually takes you."
    ),
    "og_image": "first-solo.jpg",
    "scripts": ["/assets/js/gallery.js"],
    "body": pagehead(
        "Photos",
        "Our aircraft, our students, and the places an Arizona licence takes you.",
        image="falcon-sunset.jpg",
    ) + f"""
<section class="section">
  <div class="wrap">
    <div class="gal">{gallery_grid()}
    </div>
    <p class="center" style="margin-top:44px;color:#6b7a88">
      Every photo here was taken by us or our students at Falcon Field and around
      Arizona. Want to be in the next one?
      <a href="{BOOK}">Book a discovery flight.</a></p>
  </div>
</section>

<div class="lightbox" id="lightbox" hidden>
  <button type="button" class="lightbox__close" id="lightbox-close"
          aria-label="Close">&times;</button>
  <figure class="lightbox__inner">
    <img id="lightbox-img" src="" alt="">
    <figcaption id="lightbox-cap"></figcaption>
  </figure>
</div>
"""
}

LOCATIONS = [GILBERT, SCOTTSDALE, CHANDLER, TEMPE, PHOENIX]

# ---------------------------------------------------------------------- BOOK
# First-time visitors land here instead of FlightCircle's registration form.
# The phone number is repeated prominently because for a $199 discovery flight
# most people would rather call than fill anything in.
BOOK_PAGE = {
    "slug": "book",
    "title": "Book a Discovery Flight",
    "description": (
        "Book a $199 discovery flight at Falcon Field in Mesa, AZ. No experience "
        "or medical certificate needed — you'll fly the airplane yourself. Call "
        "or send us a few details and we'll get back to you."
    ),
    "og_image": "student-smile.webp",
    "scripts": ["/assets/js/book.js"],
    "body": pagehead(
        "Book a discovery flight",
        "$199, about an hour, and you'll be flying the airplane yourself. "
        "No experience or medical certificate required.",
        image="student-smile.webp",
    ) + f"""
<section class="section">
  <div class="wrap narrow">
    <div class="callout">
      <h2 style="margin-top:0">Prefer to just call?</h2>
      <p>Honestly, that's the fastest way. Call {phone_html()} and we'll sort out a
         time in a couple of minutes &mdash; and you can ask whatever you like
         first.</p>
      <p style="margin-bottom:0">Or email
         <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
    </div>

    <h2>Or send us a few details</h2>
    <p>Tell us roughly when you're free and we'll come back to you with times. No
       account to create, and nothing is charged here &mdash; you pay on the day.</p>

    <form class="form" id="book-form" method="POST" action="/api/book" novalidate>
      <div class="form__row">
        <label for="f-name">Your name <span aria-hidden="true">*</span></label>
        <input id="f-name" name="name" type="text" autocomplete="name" required
               maxlength="120">
      </div>
      <div class="form__grid">
        <div class="form__row">
          <label for="f-phone">Phone <span aria-hidden="true">*</span></label>
          <input id="f-phone" name="phone" type="tel" autocomplete="tel" required
                 maxlength="40" inputmode="tel">
        </div>
        <div class="form__row">
          <label for="f-email">Email</label>
          <input id="f-email" name="email" type="email" autocomplete="email"
                 maxlength="160">
        </div>
      </div>
      <div class="form__row">
        <label for="f-interest">What are you interested in?</label>
        <select id="f-interest" name="interest">
          <option value="Discovery flight ($199)">Discovery flight ($199)</option>
          <option value="Private pilot (PPL)">Private pilot certificate</option>
          <option value="Instrument rating (IFR)">Instrument rating</option>
          <option value="Commercial (CPL)">Commercial certificate</option>
          <option value="CFI">Flight instructor (CFI)</option>
          <option value="Aircraft rental">Aircraft rental (already certificated)</option>
          <option value="Ferry service">Aircraft ferry service</option>
          <option value="Something else">Something else</option>
        </select>
      </div>
      <div class="form__row">
        <label for="f-when">When are you generally free?</label>
        <input id="f-when" name="when" type="text" maxlength="200"
               placeholder="e.g. weekday mornings, or weekends after 10am">
      </div>
      <div class="form__row">
        <label for="f-notes">Anything else we should know?</label>
        <textarea id="f-notes" name="notes" rows="4" maxlength="2000"
                  placeholder="Questions, previous flight experience, anything at all — optional."></textarea>
      </div>
      <!-- Honeypot: real people never fill this in. Hidden from sight and from
           screen readers, and never autocompleted. -->
      <div class="form__trap" aria-hidden="true">
        <label for="f-website">Website</label>
        <input id="f-website" name="website" type="text" tabindex="-1"
               autocomplete="off">
      </div>
      <button class="btn btn--primary" type="submit" id="book-submit">
        Send &mdash; we'll be in touch</button>
      <p class="form__note">We'll only use this to contact you about flying. No
         mailing list, and we won't pass it on.</p>
      <div class="form__status" id="book-status" role="status" aria-live="polite"></div>
    </form>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap narrow">
    <figure class="shot shot--tall">
      <img src="/assets/img/first-solo.jpg" width="675" height="900" alt="A student celebrating on the cowling of N1287U with the Falcon Field control tower behind" loading="lazy">
      <figcaption>The bit everyone remembers. First solo at Falcon Field.</figcaption>
    </figure>
    <h2 style="margin-top:38px">What happens next</h2>
    <ol class="steps">
      <li>
        <h3>We get back to you</h3>
        <p>Usually the same day. We'll suggest a couple of times that work around
           your schedule.</p>
      </li>
      <li>
        <h3>We set up your booking</h3>
        <p>We handle the scheduling side. Once you're training with us regularly
           you'll get a <a href="{SCHED}" rel="noopener">FlightCircle</a> account so
           you can book aircraft and instructor time yourself &mdash; but there's
           nothing to sign up for now.</p>
      </li>
      <li>
        <h3>You show up and fly</h3>
        <p>Bring nothing. Wear sunglasses if you have them. We'll brief you on the
           ground, then you'll take the controls with an instructor beside you.</p>
      </li>
    </ol>
    <p style="margin-top:30px">Wondering about cost or how long training takes?
       Our <a href="/faq">FAQ answers both</a> with real numbers.</p>
  </div>
</section>"""
}

# ------------------------------------------------------------- FALCON FIELD
# Every factual claim here is verifiable: runway lengths and field elevation
# from airport records, and the 1941 British Flying Training School history
# from the airport's own account and the Commemorative Air Force.
FALCON_FIELD = {
    "slug": "falcon-field",
    "title": "Learning to Fly at Falcon Field (KFFZ)",
    "description": (
        "Falcon Field Airport in Mesa, AZ — two runways, a control tower, and a "
        "flight training history going back to 1941. Why KFFZ is a good place to "
        "learn to fly."
    ),
    "og_image": "az-aerial.webp",
    "body": pagehead(
        "Falcon Field Airport (KFFZ)",
        "Two runways, a control tower, and a field that has been training pilots "
        "since 1941. Here's why that matters to you.",
        image="falcon-sunset.jpg",
    ) + """
<section class="section">
  <div class="wrap narrow">
    <h2>The field</h2>
    <p>Falcon Field sits about six miles northeast of downtown Mesa, at a field
       elevation of <strong>1,394 feet</strong>. It has two parallel runways:
       <strong>4R/22L</strong>, the 5,100-foot main runway, and
       <strong>4L/22R</strong>, a 3,800-foot parallel added in the 1980s. It is a
       <strong>towered airport</strong> with an active control tower, and one of
       the busiest general aviation fields in Arizona.</p>
    <p>We're in <strong>Hangar 120</strong>, at 4800 E Falcon Dr.
       <a href="/contact">Directions and contact details</a>.</p>

    <h2>A field built to train pilots &mdash; in 1941</h2>
    <p>Falcon Field didn't grow into a training airport. It was built as one.</p>
    <p>It opened on <strong>14 September 1941</strong> as the
       <strong>No. 4 British Flying Training School</strong>, on empty desert at
       the northern edge of Mesa. Britain was at war, and training pilots at home
       had become impractical &mdash; Luftwaffe raids and English weather made it
       both dangerous and slow. So the RAF sent its cadets to Arizona, where the
       skies were clear, the visibility enormous, and nobody was shooting at
       them.</p>
    <p>The first training flight went up in a Boeing PT-17 Stearman. Between 1941
       and 1945, <strong>more than 2,300 British cadets</strong> earned their
       wings here, along with American pilots. Some never went home &mdash;
       there's a memorial in Mesa to the cadets who died during training.</p>
    <p>Which is a long way of saying: when you fly your first lesson out of
       Falcon Field, you're using an airport that was purpose-built, eighty-odd
       years ago, for exactly what you're doing.</p>

    <h2>Why it's a good place to learn</h2>
    <div class="grid grid--2" style="margin-top:26px">
      <div class="card">
        <h3>You'll work a control tower from day one</h3>
        <p>Pilots trained at quiet, untowered fields often find their first
           towered airport intimidating &mdash; and it usually arrives at the
           worst moment, on a cross-country somewhere unfamiliar. Learn here and
           tower communication is simply how flying has always worked for you.</p>
      </div>
      <div class="card">
        <h3>Two parallel runways</h3>
        <p>Parallel operations mean less time holding for traffic and more of
           your paid Hobbs time actually flying. It also means you'll practise
           parallel-runway awareness, which is a genuinely useful habit.</p>
      </div>
      <div class="card">
        <h3>Practice areas close by</h3>
        <p>Open desert to the north and east means you're at the practice area
           within minutes. At schools that have to transit a long way to work on
           maneuvers, you're paying for the commute at the same hourly rate.</p>
      </div>
      <div class="card">
        <h3>Arizona flying weather</h3>
        <p>Clear skies most of the year mean lessons rarely cancel for weather
           &mdash; the single biggest cause of stalled training elsewhere.
           Summer brings heat and monsoon season, and learning density altitude
           where it genuinely bites makes you a better pilot.</p>
      </div>
    </div>

    <h2>Airspace worth knowing</h2>
    <p>Falcon Field sits east of Phoenix Sky Harbor's Class B airspace. Learning
       here means learning to operate near busy Class B without living inside it
       &mdash; you'll get comfortable with airspace boundaries, transitions and
       flight following as a matter of routine.</p>
    <p>To the east are the Superstition Mountains, which give you terrain,
       genuine cross-country navigation practice, and some of the best scenery
       you'll fly over anywhere.</p>

    <h2>While you're on the field</h2>
    <p>The Commemorative Air Force's Arizona Wing operates the
       <a href="https://www.azcaf.org/" rel="noopener">Airbase Arizona</a>
       museum at Falcon Field, including a memorial to the RAF cadets who trained
       here. Worth an hour if you're bringing someone along to your lesson.</p>
  </div>
</section>

""" + cta(
        "Fly from Falcon Field",
        "Book a $199 discovery flight and take the controls yourself, from an "
        "airport that has been teaching people to fly since 1941.",
    ),
}

PAGES = [HOME, COURSES, GETTING_STARTED, AIRCRAFT, INSTRUCTORS, MEDICAL, FAQ,
         FERRY, ABOUT, CONTACT, FALCON_FIELD, BOOK_PAGE, COST, GALLERY_PAGE] + LOCATIONS
