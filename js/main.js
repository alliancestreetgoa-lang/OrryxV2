/* Orryx Commodities — Version 2: motion and behaviour */
(function () {
  'use strict';

  // Set the company email here to switch the enquiry form on (opens the visitor's mail app).
  var CONTACT_EMAIL = '';

  var doc = document.documentElement;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hasGsap = !!(window.gsap && window.ScrollTrigger);

  /* ---------- colour templates ---------- */
  var themeColors = { night: '#000000', day: '#ffffff', ember: '#FE9102' };
  function setTheme(t) {
    doc.setAttribute('data-theme', t);
    try { localStorage.setItem('orryx-theme', t); } catch (e) {}
    var m = $('meta[name="theme-color"]'); if (m) m.setAttribute('content', themeColors[t]);
  }
  $$('[data-set-theme]').forEach(function (b) {
    b.addEventListener('click', function () {
      var t = b.getAttribute('data-set-theme');
      if (document.startViewTransition && !reduce) document.startViewTransition(function () { setTheme(t); });
      else setTheme(t);
    });
  });

  /* ---------- licence validity ---------- */
  (function () {
    var start = new Date('2025-10-17T00:00:00+04:00'), end = new Date('2027-10-16T23:59:59+04:00'), now = new Date();
    var left = Math.max(0, Math.ceil((end - now) / 864e5));
    var frac = Math.min(1, Math.max(0, (end - now) / (end - start)));
    window.__lic = { left: left, frac: frac };
    var a = $('#daysLeft'), b = $('#daysLeftTop');
    if (a) a.textContent = left; if (b) b.textContent = left;
    var y = $('#yr'); if (y) y.textContent = now.getFullYear();
  })();

  /* ---------- menu ---------- */
  var burger = $('#burger'), links = $('#navLinks');
  if (burger) {
    burger.addEventListener('click', function () {
      var open = links.classList.toggle('is-open');
      burger.setAttribute('aria-expanded', open);
    });
    $$('a', links).forEach(function (a) { a.addEventListener('click', function () { links.classList.remove('is-open'); burger.setAttribute('aria-expanded', 'false'); }); });
  }

  /* ---------- feelings ---------- */
  var moods = {
    stretched: ['“The business has grown, but every decision still lands on my desk.”', 'We look at how the business is organised and run, and help it work without you in every room.', '7020.00', 'Management consultancy', 'management-consultancy/'],
    unsure: ['“There are three good directions and one budget. I cannot see which comes first.”', 'We set out the real options, recommend a direction and put the steps in the order they should happen.', '7020.11', 'Strategy advisory', 'strategy-advisory/'],
    exposed: ['“Sales look fine, yet cash is tight, and I cannot see why.”', 'We read what the business earns, needs and can afford, and explain it in plain language.', '6619.14', 'Financial consultancy', 'financial-consultancy/'],
    ready: ['“It is time to buy a business. Or it is time to sell mine.”', 'We arrange the purchase and sale of small and medium sized businesses and professional practices. Not real estate brokerage.', '7490.02', 'Business brokerage', 'business-brokerage/']
  };
  var panel = $('#feelPanel');
  function showMood(key, tab) {
    var m = moods[key]; if (!m || !panel) return;
    $$('.feel-tab').forEach(function (t) { var on = t === tab; t.classList.toggle('is-on', on); t.setAttribute('aria-selected', on); });
    var apply = function () {
      panel.setAttribute('data-mood', key);
      $('#feelQuote').textContent = m[0]; $('#feelAnswer').textContent = m[1];
      $('#feelCode').textContent = m[2]; $('#feelName').textContent = m[3];
      var fl = $('#feelLink'); if (fl) fl.setAttribute('href', m[4]);
    };
    if (hasGsap && !reduce) {
      var els = $$('.feel-text > *', panel);
      gsap.to(els, { opacity: 0, y: 14, duration: .2, stagger: .03, onComplete: function () {
        apply(); gsap.fromTo(els, { opacity: 0, y: 22 }, { opacity: 1, y: 0, duration: .55, stagger: .07, ease: 'power3.out' });
      } });
      gsap.fromTo('.orb-wrap', { scale: .8, rotate: -12 }, { scale: 1, rotate: 0, duration: .8, ease: 'elastic.out(1,.6)' });
    } else apply();
  }
  $$('.feel-tab').forEach(function (t) { t.addEventListener('click', function () { showMood(t.getAttribute('data-mood'), t); }); });

  /* ---------- questions: one open at a time ---------- */
  $$('.qa').forEach(function (d) {
    d.addEventListener('toggle', function () { if (d.open) $$('.qa').forEach(function (o) { if (o !== d) o.open = false; }); });
  });

  /* ---------- enquiry form ---------- */
  var form = $('#enqForm');
  (function () {   // service pages link here with ?about=management | strategy | finance | brokerage
    var m = /[?&]about=([a-z]+)/.exec(location.search), map = { management: 'Management consultancy', strategy: 'Strategy advisory', finance: 'Financial consultancy', brokerage: 'Business brokerage' };
    if (!m || !map[m[1]] || !form) return;
    $$('input[name="topic"]', form).forEach(function (r) { r.checked = r.value === map[m[1]]; });
  })();
  if (form) form.addEventListener('submit', function (e) {
    e.preventDefault();
    var note = $('#formNote'), f = new FormData(form);
    if (!f.get('name') || !f.get('email') || !f.get('message')) { note.textContent = 'Please add your name, email and a short message.'; return; }
    if (!CONTACT_EMAIL) { note.textContent = 'Thank you. Our enquiry line is being connected. Please try again shortly.'; return; }
    var body = 'Name: ' + f.get('name') + '\nCompany: ' + (f.get('company') || '-') + '\nEmail: ' + f.get('email') + '\nAbout: ' + f.get('topic') + '\n\n' + f.get('message');
    window.location.href = 'mailto:' + CONTACT_EMAIL + '?subject=' + encodeURIComponent('Enquiry: ' + f.get('topic')) + '&body=' + encodeURIComponent(body);
    note.textContent = 'Your mail app should open with the enquiry ready to send.';
  });

  /* ---------- glass spotlight follows the pointer ---------- */
  document.addEventListener('pointermove', function (e) {
    var g = e.target.closest && e.target.closest('.glass'); if (!g) return;
    var r = g.getBoundingClientRect();
    g.style.setProperty('--mx', (e.clientX - r.left) + 'px'); g.style.setProperty('--my', (e.clientY - r.top) + 'px');
  }, { passive: true });

  /* ---------- split titles into words ---------- */
  $$('.title.split').forEach(function (t) {
    t.innerHTML = t.textContent.trim().split(/\s+/).map(function (w) { return '<span class="w"><span>' + w + '</span></span>'; }).join(' ');
  });

  /* ---------- method line (same idea as Version 1): a gentle S-curve down the middle of the five steps ---------- */
  var flow = $('.flow'), flowSvg = $('.flow-line'), flowFg = $('#flowPath'), flowBg = flowSvg ? $('.flow-bg', flowSvg) : null, flowLen = 0, flowP = { p: 1 };
  function layoutFlow() {
    if (!flow || !flowFg) return;
    var h = flow.offsetHeight, c = 60, a = innerWidth < 900 ? 16 : 48;   // a = how far the line swings to each side
    var d = 'M' + c + ' 0 C ' + (c + a) + ' ' + (.12 * h) + ', ' + (c - a) + ' ' + (.22 * h) + ', ' + c + ' ' + (.34 * h) +
            ' S ' + (c + a) + ' ' + (.56 * h) + ', ' + c + ' ' + (.68 * h) + ' S ' + (c - a) + ' ' + (.88 * h) + ', ' + c + ' ' + h;
    flowSvg.setAttribute('viewBox', '0 0 120 ' + h);
    flowBg.setAttribute('d', d); flowFg.setAttribute('d', d);
    flowLen = flowFg.getTotalLength();
    flowFg.style.strokeDasharray = flowLen;
    flowFg.style.strokeDashoffset = flowLen * (1 - flowP.p);
  }

  var loader = $('#loader');
  function showAll() {
    doc.classList.remove('js'); if (loader) loader.style.display = 'none';
    layoutFlow(); $$('[data-step]').forEach(function (st) { st.classList.add('is-in'); });
    window.addEventListener('resize', layoutFlow);
    var rf = $('#ringFg'); if (rf) rf.style.strokeDashoffset = 1 - window.__lic.frac;
  }
  if (!hasGsap || reduce) { showAll(); return; }

  /* =====================================================================
     Motion
     ===================================================================== */
  gsap.registerPlugin(ScrollTrigger);

  var lenis = null;
  if (window.Lenis) {
    lenis = new Lenis({ duration: 1.1, smoothWheel: true });
    window.__lenis = lenis;
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add(function (t) { lenis.raf(t * 1000); });
    gsap.ticker.lagSmoothing(0);
    $$('a[href^="#"]').forEach(function (a) {
      a.addEventListener('click', function (e) {
        var id = a.getAttribute('href'); if (id.length < 2) return;
        var el = $(id); if (!el) return; e.preventDefault(); lenis.scrollTo(el, { offset: id === '#top' ? 0 : -70 });
      });
    });
  }

  /* opening: the logo draws itself, then the page opens. Shown once per visit; coming back from a
     service page, or arriving on a link to a section, goes straight to the page. */
  var quick = doc.classList.contains('quick'), navEl = $('#nav'), T = 0;
  var intro = gsap.timeline({ defaults: { ease: 'power3.out' } });
  window.__intro = intro;
  if (quick) {
    if (loader) loader.style.display = 'none';
  } else {
    navEl.classList.add('is-hidden');
    var num = $('#loaderNum'), cnt = { v: 0 };
    T = 2.35;
    $$('.ld-tip').forEach(function (c) { intro.to(c, { attr: { r: 60 }, duration: .16, ease: 'none' }, +c.getAttribute('data-at')); });
    intro.to('.ld-draw', { strokeDashoffset: 0, autoRound: false, duration: 1.45, stagger: .3, ease: 'power2.inOut' }, 0)
      .call(function () { var g = $('#ldMark'); if (g) g.removeAttribute('mask'); }, null, 1.9)
      .to('.ld-letter', { opacity: 1, duration: .45, stagger: .035, ease: 'power2.out' }, .95)
      .to(cnt, { v: 100, duration: 1.7, ease: 'power1.inOut', onUpdate: function () { num.textContent = Math.round(cnt.v); } }, 0)
      .to('.loader-mark', { scale: 1.06, duration: .5, ease: 'power2.in' }, 2.15)
      .to(loader, { yPercent: -100, duration: .9, ease: 'power4.inOut', onComplete: function () { loader.style.display = 'none'; try { sessionStorage.setItem('orryx-seen', '1'); } catch (e) {} } }, T)
      .call(function () { navEl.classList.remove('is-hidden'); }, null, T + .35);
  }
  intro.from('.hero-bg img', { scale: quick ? 1.1 : 1.25, duration: quick ? 1.6 : 2.4, ease: 'power2.out' }, T)
    .to('.hero-title .line>span', { y: 0, duration: 1.1, stagger: .12, ease: 'power4.out' }, T + (quick ? .1 : .4))
    .to('.hero .reveal', { opacity: 1, y: 0, duration: .9, stagger: .1 }, T + (quick ? .4 : .8));

  /* testing aid: add ?hold=1.2 to the address to freeze the opening at that second */
  var hold = /[?&]hold=([\d.]+)/.exec(location.search); if (hold) intro.pause(+hold[1]);

  /* hero: picture drifts and text lifts away as you scroll */
  gsap.to('.hero-bg img', { yPercent: 14, ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true } });
  gsap.to('.hero-copy', { yPercent: -18, opacity: .2, ease: 'none', scrollTrigger: { trigger: '.hero', start: '55% top', end: 'bottom top', scrub: true } });
  var heroImg = $('.hero-bg img');
  if (heroImg && window.matchMedia('(hover:hover)').matches) {
    var qx = gsap.quickTo(heroImg, 'x', { duration: 1.2, ease: 'power3' }), qy = gsap.quickTo(heroImg, 'y', { duration: 1.2, ease: 'power3' });
    $('.hero').addEventListener('pointermove', function (e) { qx((e.clientX / innerWidth - .5) * -22); qy((e.clientY / innerHeight - .5) * -14); });
  }

  /* reveals */
  $$('.reveal').forEach(function (el) {
    if (el.closest('.hero')) return;
    gsap.to(el, { opacity: 1, y: 0, duration: 1, ease: 'power3.out', scrollTrigger: { trigger: el, start: 'top 88%' } });
  });
  $$('.title.split').forEach(function (t) {
    gsap.to($$('.w>span', t), { y: 0, duration: 1, stagger: .045, ease: 'power4.out', scrollTrigger: { trigger: t, start: 'top 88%' } });
  });

  /* pictures drift inside their windows */
  $$('.shot img').forEach(function (img) {
    gsap.fromTo(img, { yPercent: -5 }, { yPercent: 5, ease: 'none', scrollTrigger: { trigger: img.parentNode, start: 'top bottom', end: 'bottom top', scrub: true } });
  });

  /* background shapes react to scrolling */
  gsap.to('.tiles', { yPercent: -7, ease: 'none', scrollTrigger: { trigger: document.body, start: 'top top', end: 'bottom bottom', scrub: 1.2 } });   // the tile wall drifts slowly behind the page

  /* marquee follows scroll speed */
  (function () {
    var track = $('.marquee-track'); if (!track) return;
    var x = 0, vel = 0, half = track.scrollWidth / 2;
    window.addEventListener('resize', function () { half = track.scrollWidth / 2; });
    ScrollTrigger.create({ onUpdate: function (s) { vel = s.getVelocity() / 260; } });
    gsap.ticker.add(function () {
      x -= 1.1 + Math.abs(vel); vel *= .92;
      if (-x >= half) x += half;
      track.style.transform = 'translate3d(' + x + 'px,0,0) skewX(' + Math.max(-8, Math.min(8, vel * -1.2)) + 'deg)';
    });
  })();

  /* feelings: cards slide in */
  gsap.from('.feel-tab', { x: -50, opacity: 0, duration: .8, stagger: .1, ease: 'power3.out', scrollTrigger: { trigger: '.feel-grid', start: 'top 82%' } });
  gsap.from('.feel-panel', { y: 60, opacity: 0, scale: .96, duration: 1, ease: 'power3.out', scrollTrigger: { trigger: '.feel-grid', start: 'top 82%' } });

  /* activities: each glass card settles back as the next one arrives */
  var acts = $$('.act');
  acts.forEach(function (card, i) {
    gsap.from(card, { y: 90, opacity: 0, duration: 1, ease: 'power3.out', scrollTrigger: { trigger: card, start: 'top 92%' } });
    if (i < acts.length - 1) {
      // start value is stated on purpose: without it the card fades through black on the way to its dimmed state
      gsap.fromTo(card, { scale: 1, filter: 'brightness(1)' }, { scale: 1 - (acts.length - 1 - i) * .035, filter: 'brightness(.8)', ease: 'none',
        scrollTrigger: { trigger: acts[i + 1], start: 'top 85%', end: 'top 15%', scrub: true } });
    }
  });

  /* method: the same scrolling motion as Version 1. The line draws down the middle as you scroll,
     each number lights up when reached, and the cards arrive from the left and right in turn. */
  (function () {
    if (!flow || !flowFg) return;
    flowP.p = 0; layoutFlow();
    gsap.to(flowP, { p: 1, ease: 'none', scrollTrigger: { trigger: flow, start: 'top 60%', end: 'bottom 70%', scrub: .6 },
      onUpdate: function () { flowFg.style.strokeDashoffset = flowLen * (1 - flowP.p); } });
    ScrollTrigger.addEventListener('refreshInit', layoutFlow);
    $$('[data-step]').forEach(function (st, i) {
      gsap.from($('.step-c', st), { x: innerWidth < 900 ? 30 : (i % 2 ? 80 : -80), autoAlpha: 0, rotateY: i % 2 ? -18 : 18, transformPerspective: 900, duration: 1.2, ease: 'expo.out', scrollTrigger: { trigger: st, start: 'top 78%' } });
      ScrollTrigger.create({ trigger: st, start: 'top 62%', onEnter: function () { st.classList.add('is-in'); }, onLeaveBack: function () { st.classList.remove('is-in'); } });
    });
  })();

  /* brokerage */
  gsap.from('.party:not(.right)', { x: -80, opacity: 0, duration: 1, ease: 'power3.out', scrollTrigger: { trigger: '.deal', start: 'top 80%' } });
  gsap.from('.party.right', { x: 80, opacity: 0, duration: 1, ease: 'power3.out', scrollTrigger: { trigger: '.deal', start: 'top 80%' } });
  gsap.from('.bridge-core', { scale: 0, rotate: -180, duration: 1.2, ease: 'back.out(1.6)', scrollTrigger: { trigger: '.deal', start: 'top 78%' } });

  /* licence card: ring fills, days count up, card tilts with the pointer */
  (function () {
    var card = $('#licCard'); if (!card) return;
    var L = window.__lic, o = { v: 0 }, d = $('#daysLeft');
    ScrollTrigger.create({ trigger: card, start: 'top 80%', once: true, onEnter: function () {
      var ring = $('#ringFg');
      gsap.to(o, { v: 1, duration: 2, ease: 'power3.out', onUpdate: function () { d.textContent = Math.round(o.v * L.left); ring.style.strokeDashoffset = 1 - L.frac * o.v; } });
      gsap.fromTo(card, { '--sx': '120%' }, { '--sx': '-60%', duration: 1.8, ease: 'power2.inOut' });
    } });
    gsap.from(card, { rotateY: -24, rotateX: 10, y: 60, opacity: 0, duration: 1.3, ease: 'power3.out', scrollTrigger: { trigger: card, start: 'top 88%' } });
    if (window.matchMedia('(hover:hover)').matches) {
      var wrap = card.parentNode;
      wrap.addEventListener('pointermove', function (e) {
        var r = card.getBoundingClientRect(), px = (e.clientX - r.left) / r.width - .5, py = (e.clientY - r.top) / r.height - .5;
        gsap.to(card, { rotateY: px * 14, rotateX: -py * 12, '--sx': (120 - (px + .5) * 180) + '%', duration: .5, ease: 'power2.out', overwrite: 'auto' });
      });
      wrap.addEventListener('pointerleave', function () { gsap.to(card, { rotateY: 0, rotateX: 0, duration: .9, ease: 'elastic.out(1,.6)' }); });
    }
  })();

  /* top stat counts up */
  $$('[data-count]').forEach(function (el) {
    var o = { v: 0 }, to = +el.getAttribute('data-count');
    intro.to(o, { v: to, duration: 1.2, onUpdate: function () { el.textContent = Math.round(o.v); } }, T + .95);
  });
  (function () { var el = $('#daysLeftTop'), o = { v: 0 }; if (el) intro.to(o, { v: window.__lic.left, duration: 1.6, ease: 'power2.out', onUpdate: function () { el.textContent = Math.round(o.v); } }, T + .95); })();

  /* magnetic buttons */
  if (window.matchMedia('(hover:hover)').matches) $$('.magnetic').forEach(function (b) {
    b.addEventListener('pointermove', function (e) { var r = b.getBoundingClientRect(); gsap.to(b, { x: (e.clientX - r.left - r.width / 2) * .25, y: (e.clientY - r.top - r.height / 2) * .35, duration: .4, ease: 'power2.out' }); });
    b.addEventListener('pointerleave', function () { gsap.to(b, { x: 0, y: 0, duration: .8, ease: 'elastic.out(1,.5)' }); });
  });

  /* footer word rises */
  gsap.from('.foot-logo', { yPercent: 35, opacity: 0, scale: .9, ease: 'none', scrollTrigger: { trigger: '.foot', start: 'top bottom', end: 'bottom bottom', scrub: true } });

  /* menu bar hides on the way down, returns on the way up; highlights the current section */
  var nav = $('#nav');
  ScrollTrigger.create({ start: 300, end: 'max', onUpdate: function (s) { if (!links.classList.contains('is-open')) nav.classList.toggle('is-hidden', s.direction === 1); } });
  $$('.nav-links a').forEach(function (a) {
    var sec = $(a.getAttribute('href')); if (!sec) return;
    ScrollTrigger.create({ trigger: sec, start: 'top 50%', end: 'bottom 50%', onToggle: function (s) { a.classList.toggle('is-active', s.isActive); } });
  });

  window.addEventListener('load', function () {
    ScrollTrigger.refresh();
    var target = location.hash.length > 1 ? $(location.hash) : null;
    if (target && lenis) lenis.scrollTo(target, { offset: -70, immediate: true });
  });
})();
