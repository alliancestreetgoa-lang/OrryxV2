"""Writes the four service pages of Orryx Commodities, Version 2.

Run from the project folder:   python3 tools/build_pages.py

The wording is the same as the Version 1 service pages. To change a page, change the text in
PAGES below and run this again (hand edits to the four index.html files are overwritten).
Raise CSS_V / JS_V when css/style.css or js/page.js change, so browsers load the new files.
"""
import os, re, html

CSS_V, JS_V = 23, 3
ARROW = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
TICK = '<svg class="tick" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M7 12.5l3.2 3.2L17 9"/></svg>'

FIVE_STEPS = [
    ('Listen', "We start with the owner's real question and the facts behind it."),
    ('Diagnose', 'We examine how the business is run and how the numbers behave.'),
    ('Design', 'We set out the options, a recommended strategy and the plan.'),
    ('Deliver', 'We stay alongside management while the plan is carried out.'),
    ('Transact', 'When buying or selling is the right move, our brokerage desk arranges the deal.'),
]

PAGES = [
    dict(
        slug='management-consultancy', key='management', code='7020.00', name='Management consultancy',
        words=('Management', 'consultancy'), img='management', alt='Glass organisation structure with gears',
        title='Management Consultancy in Dubai | Orryx Commodities',
        desc='Management consultancy from Orryx Commodities L.L.C-FZ, Dubai: organisation design, process improvement, governance and change support. Licensed activity 7020.00.',
        lead='Practical advice on how the business is organised and run, so decisions get made faster and the work gets done better.',
        question='How should the business be organised and run?',
        covers=[
            ('Operating model and organisation design', 'How the business is structured: who does what, how teams fit together, and whether that structure still suits the size and direction of the company.'),
            ('Process and performance improvement', 'A close look at how work actually flows, where time and money are lost, and what to change first.'),
            ('Governance, roles and reporting lines', 'Clear decision rights and reporting, so owners and managers know who decides, who is accountable and who needs to be told.'),
            ('Change and transformation support', 'We stay alongside management while changes are carried out, and adjust as results arrive.'),
        ],
        signs=['The business has outgrown the way it is organised.', 'Too many decisions wait on one person.', 'The same problems return every quarter.', 'A change has been agreed but is not happening.'],
        how_title='How an engagement flows.', steps=FIVE_STEPS,
        activity='Management consultancy activities', activity_ar='انشطة استشارات الادارية', notes=[],
        faq_title='Management consultancy, answered plainly.',
        faqs=[
            ('What is management consultancy?', 'Management consultancy is advice to owners and leadership teams on how a business is organised and run. At Orryx it covers operating model and organisation design, process and performance improvement, governance, roles and reporting lines, and change and transformation support.'),
            ('Is Orryx licensed for management consultancy?', "Yes. Management consultancy is activity 7020.00 on the company's business licence number 2538901.01, issued by the Meydan Free Zone, Dubai. The licence was issued on 17 October 2025 and is valid to 16 October 2027."),
            ('How does a management consultancy engagement start?', "It starts with the owner's real question (growth, control, cash or exit) and the facts behind it. We then examine how the business is run, separate symptoms from causes, and set out the options and a plan in plain language."),
        ],
    ),
    dict(
        slug='strategy-advisory', key='strategy', code='7020.11', name='Strategy advisory',
        words=('Strategy', 'advisory'), img='strategy', alt='Glass chess knight beside a glowing route with waypoints',
        title='Strategy Advisory in Dubai | Orryx Commodities',
        desc='Strategy advisory from Orryx Commodities L.L.C-FZ, Dubai: growth and market-entry planning, business plans, positioning and decision support. Licensed activity 7020.11.',
        lead='Where to play, how to win and what to do first. A clear route from where the business stands today to where you want it to be.',
        question='Where does the business go next, and in what order?',
        covers=[
            ('Growth and market-entry planning', 'Where growth can come from (new customers, new services or new markets) and what entering each one would take.'),
            ('Business plans and strategic roadmaps', 'A written plan that sets out the goal, the steps, the order they happen in and who owns each one.'),
            ('Competitive positioning', 'Where the business stands against the alternatives a customer has, and what it should be known for.'),
            ('Board and owner decision support', 'The options, the trade-offs and a recommendation, set out in plain language before a major decision is made.'),
        ],
        signs=['Growth has slowed and the next step is not obvious.', 'A new market or service is on the table.', 'The owners want one agreed plan, not several opinions.', 'A major decision needs a clear, written case.'],
        how_title='How an engagement flows.', steps=FIVE_STEPS,
        activity='Strategy advisory services', activity_ar='خدمات استشارات الاستراتيجية', notes=[],
        faq_title='Strategy advisory, answered plainly.',
        faqs=[
            ('What is strategy advisory?', 'Strategy advisory helps owners and boards decide where the business goes next and in what order. At Orryx it covers growth and market-entry planning, business plans and strategic roadmaps, competitive positioning, and board and owner decision support.'),
            ('Is Orryx licensed for strategy advisory?', "Yes. Strategy advisory services is activity 7020.11 on the company's business licence number 2538901.01, issued by the Meydan Free Zone, Dubai. The licence was issued on 17 October 2025 and is valid to 16 October 2027."),
            ('What do I get at the end of a strategy engagement?', 'The options, a recommended strategy and the plan to reach it, written in plain language. Where the client wants it, Orryx stays alongside management while the plan is carried out.'),
        ],
    ),
    dict(
        slug='financial-consultancy', key='finance', code='6619.14', name='Financial consultancy',
        words=('Financial', 'consultancy'), img='finance', alt='Glass bars rising like a chart beside stacks of glass coins',
        title='Financial Consultancy in Dubai | Orryx Commodities',
        desc='Financial consultancy from Orryx Commodities L.L.C-FZ, Dubai: budgets and forecasts, cash-flow reviews, feasibility studies and investor readiness. Activity 6619.14.',
        lead='Consultancy on the numbers behind the plan, so owners understand what the business earns, needs and can afford.',
        question='What do the numbers say the business earns, needs and can afford?',
        covers=[
            ('Financial planning, budgets and forecasts', 'A budget and forecast the owners can actually run the business by, built on the plan and not on last year plus a percentage.'),
            ('Cash-flow and working-capital reviews', 'Where cash comes in, where it gets stuck and how much the business needs to keep operating comfortably.'),
            ('Feasibility studies for new ventures', 'Whether a new venture, product or location stacks up before money is committed to it.'),
            ('Funding and investor readiness', 'Getting the numbers and the supporting information in order before the business approaches a lender or an investor.'),
        ],
        signs=['Profit looks fine but cash is always tight.', 'There is no budget the team actually works to.', 'A new venture needs testing before money goes in.', 'A lender or investor will soon ask hard questions.'],
        how_title='How an engagement flows.', steps=FIVE_STEPS,
        activity='Financial consultancy', activity_ar='استشارات المالية',
        notes=['Activity authorisation issued 18·11·2026 under Meydan Free Zone regulations.'],
        faq_title='Financial consultancy, answered plainly.',
        faqs=[
            ('What is financial consultancy?', 'Financial consultancy is advice on the numbers behind a business plan. At Orryx it covers financial planning, budgets and forecasts, cash-flow and working-capital reviews, feasibility studies for new ventures, and funding and investor readiness.'),
            ('Is Orryx licensed for financial consultancy?', "Financial consultancy is activity 6619.14, held by Orryx Commodities L.L.C-FZ under an Activity Authorisation issued on 18 November 2026 under Meydan Free Zone regulations, with expiry on 16 October 2027. The company's business licence number is 2538901.01."),
            ('How does financial consultancy connect to the other Orryx services?', 'Each activity feeds the next. The financial review shows what a strategy will cost and whether the business can afford it, and it supports the preparation of a business for sale when the owner decides to exit.'),
        ],
    ),
    dict(
        slug='business-brokerage', key='brokerage', code='7490.02', name='Business brokerage',
        words=('Business', 'brokerage'), img='brokerage', alt='Two glass hands meeting in a handshake',
        title='Business Brokerage in Dubai: Buy or Sell an SME | Orryx',
        desc='Business brokerage from Orryx Commodities L.L.C-FZ, Dubai: arranging the purchase and sale of small and medium sized businesses. Not real estate. Activity 7490.02.',
        lead='Arranging the purchase and sale of small and medium sized businesses, including professional practices.',
        question='Is it time to buy a business, or sell this one?',
        covers=[
            ('Preparing a business for sale', 'Position the business, organise the information and agree what a good outcome looks like.'),
            ('Finding and introducing buyers or sellers', 'Identify suitable counterparties and make confidential introductions.'),
            ('Supporting negotiation and terms', 'A steady hand between the two sides while price and terms are worked out.'),
            ('Coordinating the path to completion', 'Keep the steps moving in order, from agreed terms through to completion.'),
        ],
        signs=['An owner is thinking about exit or retirement.', 'A professional practice needs a successor.', 'An entrepreneur would rather buy than start from zero.', 'An investor is looking for an established business.'],
        how_title='From first conversation to completion.',
        steps=[
            ('Prepare', 'Position the business, organise the information and agree what a good outcome looks like.'),
            ('Match', 'Identify suitable counterparties and make confidential introductions.'),
            ('Arrange', 'Support the negotiation and coordinate the steps through to completion.'),
        ],
        activity='Business brokerage activities', activity_ar='انشطة السمسرة التجارية',
        notes=['Licensed scope: business brokerage of small and medium sized businesses and professional practices. It does not include real estate brokerage.'],
        faq_title='Business brokerage, answered plainly.',
        faqs=[
            ('What does a business broker do?', 'A business broker arranges the purchase and sale of businesses. Orryx prepares a business for sale, finds and introduces buyers or sellers, supports the negotiation of terms and coordinates the steps through to completion.'),
            ("Who is Orryx's business brokerage for?", 'For sellers who own small and medium sized businesses or professional practices, and for buyers: entrepreneurs and investors looking to acquire an established business.'),
            ('Does Orryx broker real estate?', 'No. The licensed activity (7490.02, business licence 2538901.01, Meydan Free Zone, Dubai) covers arranging the purchase and sale of small and medium sized businesses, including professional practices. It does not include real estate brokerage.'),
        ],
    ),
]

e = html.escape
home = open('index.html').read()
badges = re.findall(r'<div class="mg-badge" aria-hidden="true">(<svg.*?</svg>)\s*</div>', home, re.S)
assert len(badges) == 4, 'expected the four moving diagrams in index.html'

LOGO = ('<img class="logo logo-w" src="../assets/logo/orryx-logo-transparent-white-text.svg" alt="%s" width="1157" height="616">'
        '<img class="logo logo-b" src="../assets/logo/orryx-logo-transparent-black-text.svg" alt="" width="1157" height="616">')
THEMES = ('<button class="theme-dot" data-set-theme="night" aria-label="Night theme: black and orange" title="Night"></button>'
          '<button class="theme-dot" data-set-theme="day" aria-label="Day theme: white and orange" title="Day"></button>'
          '<button class="theme-dot" data-set-theme="ember" aria-label="Ember theme: orange and black" title="Ember"></button>')


def page(p, i):
    others = [q for q in PAGES if q is not p]
    covers = '\n'.join('      <article class="cover glass reveal"><span class="cover-n">%02d</span><h3>%s</h3><p>%s</p></article>' % (n + 1, e(t), e(x)) for n, (t, x) in enumerate(p['covers']))
    signs = '\n'.join('      <li class="sign glass reveal">%s<span>%s</span></li>' % (TICK, e(s)) for s in p['signs'])
    steps = '\n'.join('        <li class="step" data-step><div class="step-n">%d</div><div class="step-c glass"><h3>%s</h3><p>%s</p></div></li>' % (n + 1, e(t), e(x)) for n, (t, x) in enumerate(p['steps']))
    notes = '\n'.join('      <p class="fine reveal">%s</p>' % e(n) for n in p['notes'] + ['Issued under the Meydan Free Zone regulations.'])
    faqs = '\n'.join('      <details class="qa glass reveal"%s><summary>%s<i></i></summary><p>%s</p></details>' % (' open' if n == 0 else '', e(q), e(a)) for n, (q, a) in enumerate(p['faqs']))
    cards = '\n'.join(
        '      <a class="other glass reveal" href="../%s/"><div class="shot"><img src="../assets/img/%s.webp" alt="%s" loading="lazy" width="1536" height="1024"></div>'
        '<div class="other-body"><span class="code">%s</span><h3>%s</h3><p>%s</p><span class="more"><span>Open</span>%s</span></div></a>'
        % (q['slug'], q['img'], e(q['alt']), q['code'], e(q['name']), e(q['question']), ARROW) for q in others)
    foot_links = ''.join('<a href="../%s/">%s</a>' % (q['slug'], e(q['name'])) for q in PAGES)
    return f'''<!doctype html>
<html lang="en" data-theme="night">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(p['title'])}</title>
<meta name="description" content="{e(p['desc'])}">
<!-- Version 2 is a design alternative. Keep it out of search until one version is chosen. -->
<meta name="robots" content="noindex">
<meta name="theme-color" content="#000000">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(p['title'])}">
<meta property="og:description" content="{e(p['desc'])}">
<meta property="og:image" content="https://alliancestreetgoa-lang.github.io/OrryxV2/assets/img/og.png">
<link rel="icon" type="image/png" href="../assets/img/favicon.png">
<link rel="apple-touch-icon" href="../assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&family=Manrope:wght@400;500;600;700&family=Noto+Kufi+Arabic:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../css/style.css?v={CSS_V}">
<script>
  (function(){{var d=document.documentElement;d.classList.add('js');
  try{{var t=localStorage.getItem('orryx-theme');if(t)d.setAttribute('data-theme',t);}}catch(e){{}}}})();
</script>
</head>
<body class="page">
<!-- This page is written by tools/build_pages.py. Change the wording there and run it again. -->

<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
  <filter id="goo"><feGaussianBlur in="SourceGraphic" stdDeviation="12" result="b"/><feColorMatrix in="b" values="1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 22 -9"/></filter>
</defs></svg>

<div class="stage" aria-hidden="true">
  <div class="blob b1"></div>
  <div class="blob b2"></div>
  <div class="blob b3"></div>
  <div class="tiles"></div>
  <div class="sweep"></div>
</div>

<header class="nav glass" id="nav">
  <a class="brand" href="../" aria-label="Orryx Commodities, home">{LOGO % ''}</a>
  <nav class="nav-links" id="navLinks" aria-label="Main">
    <a href="../#feel">Start here</a>
    <a href="../#activities" class="is-active" aria-current="true">Activities</a>
    <a href="../#method">Method</a>
    <a href="../#brokerage">Brokerage</a>
    <a href="../#licence">Licence</a>
    <a href="../#questions">Questions</a>
  </nav>
  <div class="nav-right">
    <div class="themes" role="group" aria-label="Colour theme">{THEMES}</div>
    <a class="btn btn-solid nav-cta" href="../?about={p['key']}#enquire"><span>Enquire</span></a>
    <button class="burger" id="burger" aria-label="Open menu" aria-expanded="false"><i></i><i></i></button>
  </div>
</header>

<main id="top">

<section class="hero svc-hero" id="hero">
  <div class="hero-bg" aria-hidden="true"><img src="../assets/img/{p['img']}.webp" alt="" width="1536" height="1024" fetchpriority="high"></div>
  <div class="hero-copy">
    <nav class="crumbs reveal" aria-label="Breadcrumb"><a href="../">Home</a><i>/</i><a href="../#activities">Activities</a><i>/</i><span>{e(p['name'])}</span></nav>
    <p class="kicker reveal"><span class="code">{p['code']}</span>Licensed activity<span class="k-x"> · Meydan Free Zone · Dubai</span></p>
    <h1 class="hero-title" id="heroTitle" aria-label="{e(p['name'])} in Dubai">
      <span class="line"><span>{e(p['words'][0])}</span></span>
      <span class="line"><span>{e(p['words'][1])}</span></span>
      <span class="line"><span><em>in Dubai.</em></span></span>
    </h1>
    <p class="hero-sub reveal">{e(p['lead'])}</p>
    <div class="svc-q glass reveal"><small>The question it answers</small><p>{e(p['question'])}</p></div>
    <div class="hero-btns reveal">
      <a class="btn btn-solid magnetic" href="../?about={p['key']}#enquire"><span>Talk to us about this</span>{ARROW}</a>
      <a class="btn btn-glass magnetic" href="#covers"><span>What it covers</span></a>
    </div>
  </div>
  <div class="mg-badge svc-badge reveal" aria-hidden="true">{badges[i]}</div>
</section>

<section class="section" id="covers">
  <div class="wrap">
    <div class="head">
      <p class="eyebrow reveal"><b>01</b> What it covers</p>
      <h2 class="title split">Four parts of the work.</h2>
    </div>
    <div class="cover-grid">
{covers}
    </div>
  </div>
</section>

<section class="section fits" id="fits">
  <div class="wrap fits-grid">
    <div>
      <p class="eyebrow reveal"><b>02</b> When it fits</p>
      <h2 class="title split">Signs it is time to talk.</h2>
      <div class="shot fits-shot reveal"><img src="../assets/img/{p['img']}.webp" alt="{e(p['alt'])}" loading="lazy" width="1536" height="1024"></div>
    </div>
    <ul class="signs">
{signs}
    </ul>
  </div>
</section>

<section class="section method" id="how">
  <div class="wrap">
    <div class="head center">
      <p class="eyebrow reveal"><b>03</b> How it works</p>
      <h2 class="title split">{e(p['how_title'])}</h2>
    </div>
    <div class="flow">
      <svg class="flow-line" aria-hidden="true"><path class="flow-bg"/><path class="flow-fg" id="flowPath"/></svg>
      <ol class="flow-steps" id="steps">
{steps}
      </ol>
    </div>
  </div>
</section>

<section class="section licence svc-lic" id="licence">
  <div class="wrap licence-grid">
    <div>
      <p class="eyebrow reveal"><b>04</b> Credentials</p>
      <h2 class="title split">The licence behind it.</h2>
      <p class="lead reveal">{e(p['name'])} is one of the four activities Orryx Commodities L.L.C-FZ is licensed for in the Meydan Free Zone, Dubai.</p>
{notes}
      <a class="btn btn-glass reveal" href="../#licence"><span>See the full licence</span>{ARROW}</a>
    </div>
    <div class="card3d-wrap">
      <div class="card3d glass" id="licCard">
        <div class="card3d-shine" aria-hidden="true"></div>
        <div class="lic-top"><span class="lic-logo">{LOGO % ''}</span><span>Licensed activity</span></div>
        <div class="lic-code">{p['code']}</div>
        <dl class="lic-rows">
          <div><dt>Activity</dt><dd>{e(p['activity'])}</dd></div>
          <div><dt lang="ar" dir="rtl">النشاط</dt><dd lang="ar" dir="rtl">{p['activity_ar']}</dd></div>
          <div><dt>Company</dt><dd>Orryx Commodities L.L.C-FZ</dd></div>
          <div><dt>Licence number</dt><dd>2538901.01</dd></div>
          <div><dt>Licence valid to</dt><dd>16 October 2027</dd></div>
          <div><dt>Registered address</dt><dd>Meydan Grandstand, 6th floor, Meydan Road, Nad Al Sheba, Dubai, U.A.E.</dd></div>
        </dl>
      </div>
    </div>
  </div>
</section>

<section class="section faq" id="questions">
  <div class="wrap narrow">
    <div class="head center">
      <p class="eyebrow reveal"><b>05</b> Questions</p>
      <h2 class="title split">{e(p['faq_title'])}</h2>
    </div>
    <div class="qa-list">
{faqs}
    </div>
  </div>
</section>

<section class="section others" id="others">
  <div class="wrap">
    <div class="head">
      <p class="eyebrow reveal"><b>06</b> The other activities</p>
      <h2 class="title split">Each one feeds the next.</h2>
    </div>
    <div class="other-grid">
{cards}
    </div>
  </div>
</section>

<section class="section cta" id="talk">
  <div class="wrap">
    <div class="cta-box glass reveal">
      <h2 class="title">Tell us what is on your mind.</h2>
      <p class="lead">Share a few lines about your company and the question on your desk. We will come back with how Orryx can help.</p>
      <a class="btn btn-solid magnetic" href="../?about={p['key']}#enquire"><span>Send an enquiry</span>{ARROW}</a>
    </div>
  </div>
</section>

</main>

<footer class="foot">
  <div class="wrap foot-grid">
    <div>
      <h4>Registered office</h4>
      <p class="foot-co"><b>Orryx Commodities L.L.C-FZ</b><br>Meydan Grandstand, 6th floor, Meydan Road,<br>Nad Al Sheba, Dubai, U.A.E.</p>
    </div>
    <div><h4>Activities</h4>{foot_links}</div>
    <div><h4>Company</h4><a href="../#method">Method</a><a href="../#licence">Licence</a><a href="../#questions">Questions</a><a href="../#enquire">Enquire</a></div>
    <div><h4>Colour</h4>
      <div class="themes foot-themes" role="group" aria-label="Colour theme">{THEMES}</div>
      <p class="fine">Licence No. 2538901.01<br>Valid to 16 · 10 · 2027</p>
    </div>
  </div>
  <div class="foot-logo">{LOGO % 'Orryx Commodities'}</div>
  <div class="wrap foot-base"><span>© <span id="yr">2026</span> Orryx Commodities L.L.C-FZ</span><span>Meydan Free Zone, Dubai</span></div>
</footer>

<script src="../vendor/gsap.min.js"></script>
<script src="../vendor/ScrollTrigger.min.js"></script>
<script src="../vendor/lenis.min.js"></script>
<script src="../js/page.js?v={JS_V}"></script>
</body>
</html>
'''


for i, p in enumerate(PAGES):
    os.makedirs(p['slug'], exist_ok=True)
    open(os.path.join(p['slug'], 'index.html'), 'w').write(page(p, i))
    print('wrote', p['slug'] + '/index.html')
