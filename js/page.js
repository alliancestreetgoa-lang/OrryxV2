/* Orryx Commodities — Version 2: motion and behaviour for the four service pages.
   (The home page uses main.js. The pages themselves are written by tools/build_pages.py.) */
(function () {
  'use strict';

  var doc = document.documentElement;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hasGsap = !!(window.gsap && window.ScrollTrigger);
  var canHover = window.matchMedia('(hover:hover)').matches;

  /* ---------- colour templates (same three as the home page, remembered on the device) ---------- */
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

  var y = $('#yr'); if (y) y.textContent = new Date().getFullYear();

  /* ---------- menu ---------- */
  var burger = $('#burger'), links = $('#navLinks');
  if (burger) {
    burger.addEventListener('click', function () {
      var open = links.classList.toggle('is-open');
      burger.setAttribute('aria-expanded', open);
    });
    $$('a', links).forEach(function (a) { a.addEventListener('click', function () { links.classList.remove('is-open'); burger.setAttribute('aria-expanded', 'false'); }); });
  }

  /* ---------- questions: one open at a time ---------- */
  $$('.qa').forEach(function (d) {
    d.addEventListener('toggle', function () { if (d.open) $$('.qa').forEach(function (o) { if (o !== d) o.open = false; }); });
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

  /* ---------- "how it works" line: a gentle S-curve down the middle of the steps (same as the home Method) ---------- */
  var flow = $('.flow'), flowSvg = $('.flow-line'), flowFg = $('#flowPath'), flowBg = flowSvg ? $('.flow-bg', flowSvg) : null, flowLen = 0, flowP = { p: 1 };
  function layoutFlow() {
    if (!flow || !flowFg) return;
    var h = flow.offsetHeight, c = 60, a = innerWidth < 900 ? 16 : 48;
    var d = 'M' + c + ' 0 C ' + (c + a) + ' ' + (.12 * h) + ', ' + (c - a) + ' ' + (.22 * h) + ', ' + c + ' ' + (.34 * h) +
            ' S ' + (c + a) + ' ' + (.56 * h) + ', ' + c + ' ' + (.68 * h) + ' S ' + (c - a) + ' ' + (.88 * h) + ', ' + c + ' ' + h;
    flowSvg.setAttribute('viewBox', '0 0 120 ' + h);
    flowBg.setAttribute('d', d); flowFg.setAttribute('d', d);
    flowLen = flowFg.getTotalLength();
    flowFg.style.strokeDasharray = flowLen;
    flowFg.style.strokeDashoffset = flowLen * (1 - flowP.p);
  }

  function showAll() {
    doc.classList.remove('js');
    layoutFlow();
    $$('[data-step], .sign').forEach(function (el) { el.classList.add('is-in'); });
    window.addEventListener('resize', layoutFlow);
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

  /* opening: the picture settles, the name rises line by line, the rest follows */
  var intro = gsap.timeline({ defaults: { ease: 'power3.out' } });
  window.__intro = intro;
  intro.from('.hero-bg img', { scale: 1.18, duration: 2, ease: 'power2.out' }, 0)
    .to('.hero-title .line>span', { y: 0, duration: 1.1, stagger: .12, ease: 'power4.out' }, .15)
    .to('.hero .reveal', { opacity: 1, y: 0, duration: .9, stagger: .09 }, .5);

  /* hero: picture drifts with the scroll and the pointer, words lift away */
  gsap.to('.hero-bg img', { yPercent: 12, ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true } });
  gsap.to('.hero-copy', { yPercent: -14, opacity: .25, ease: 'none', scrollTrigger: { trigger: '.hero', start: '60% top', end: 'bottom top', scrub: true } });
  var heroImg = $('.hero-bg img');
  if (heroImg && canHover) {
    var qx = gsap.quickTo(heroImg, 'x', { duration: 1.2, ease: 'power3' }), qy = gsap.quickTo(heroImg, 'y', { duration: 1.2, ease: 'power3' });
    $('.hero').addEventListener('pointermove', function (e) { qx((e.clientX / innerWidth - .5) * -22); qy((e.clientY / innerHeight - .5) * -14); });
  }

  /* reveals: things that enter together arrive one after another */
  ScrollTrigger.batch($$('.reveal').filter(function (el) { return !el.closest('.hero'); }), {
    start: 'top 88%', once: true,
    onEnter: function (els) { gsap.to(els, { opacity: 1, y: 0, duration: 1, ease: 'power3.out', stagger: .1 }); }
  });
  $$('.title.split').forEach(function (t) {
    gsap.to($$('.w>span', t), { y: 0, duration: 1, stagger: .045, ease: 'power4.out', scrollTrigger: { trigger: t, start: 'top 88%' } });
  });

  /* pictures drift inside their frames */
  $$('.shot img').forEach(function (img) {
    gsap.fromTo(img, { yPercent: -5 }, { yPercent: 5, ease: 'none', scrollTrigger: { trigger: img.parentNode, start: 'top bottom', end: 'bottom top', scrub: true } });
  });
  gsap.to('.stage-mark', { rotate: 40, ease: 'none', scrollTrigger: { trigger: document.body, start: 'top top', end: 'bottom bottom', scrub: 1.2 } });

  /* signs: each tick draws itself as its line arrives */
  $$('.sign').forEach(function (el) {
    ScrollTrigger.create({ trigger: el, start: 'top 86%', once: true, onEnter: function () { el.classList.add('is-in'); } });
  });

  /* how it works: the same scrolling motion as the home Method (and Version 1) */
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

  /* licence card: turns in, a light passes over it, then it tilts with the pointer */
  (function () {
    var card = $('#licCard'); if (!card) return;
    ScrollTrigger.create({ trigger: card, start: 'top 80%', once: true, onEnter: function () {
      gsap.fromTo(card, { '--sx': '120%' }, { '--sx': '-60%', duration: 1.8, ease: 'power2.inOut' });
    } });
    gsap.from(card, { rotateY: -24, rotateX: 10, y: 60, opacity: 0, duration: 1.3, ease: 'power3.out', scrollTrigger: { trigger: card, start: 'top 88%' } });
    if (canHover) {
      var wrap = card.parentNode;
      wrap.addEventListener('pointermove', function (e) {
        var r = card.getBoundingClientRect(), px = (e.clientX - r.left) / r.width - .5, py = (e.clientY - r.top) / r.height - .5;
        gsap.to(card, { rotateY: px * 14, rotateX: -py * 12, '--sx': (120 - (px + .5) * 180) + '%', duration: .5, ease: 'power2.out', overwrite: 'auto' });
      });
      wrap.addEventListener('pointerleave', function () { gsap.to(card, { rotateY: 0, rotateX: 0, duration: .9, ease: 'elastic.out(1,.6)' }); });
    }
  })();

  /* magnetic buttons */
  if (canHover) $$('.magnetic').forEach(function (b) {
    b.addEventListener('pointermove', function (e) { var r = b.getBoundingClientRect(); gsap.to(b, { x: (e.clientX - r.left - r.width / 2) * .25, y: (e.clientY - r.top - r.height / 2) * .35, duration: .4, ease: 'power2.out' }); });
    b.addEventListener('pointerleave', function () { gsap.to(b, { x: 0, y: 0, duration: .8, ease: 'elastic.out(1,.5)' }); });
  });

  /* footer logo rises */
  gsap.from('.foot-logo', { yPercent: 35, opacity: 0, scale: .9, ease: 'none', scrollTrigger: { trigger: '.foot', start: 'top bottom', end: 'bottom bottom', scrub: true } });

  /* menu bar hides on the way down, returns on the way up */
  var nav = $('#nav');
  ScrollTrigger.create({ start: 300, end: 'max', onUpdate: function (s) { if (!links.classList.contains('is-open')) nav.classList.toggle('is-hidden', s.direction === 1); } });

  window.addEventListener('load', function () { ScrollTrigger.refresh(); });
})();
