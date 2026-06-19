(function () {
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (!reduced && window.Lenis) {
    var lenis = new Lenis({
      duration: 1.1,
      smoothWheel: true,
      touchMultiplier: 1.2,
    });
    function raf(time) {
      lenis.raf(time);
      requestAnimationFrame(raf);
    }
    requestAnimationFrame(raf);
  }

  var selectors = [
    '.tg-hero-inner > div:first-child',
    '.tg-hero-visual',
    '.tg-logos-inner',
    '.tg-how-header',
    '.tg-diagram',
    '.tg-step-card',
    '.tg-platform-header',
    '.tg-pillar',
    '.tg-funnel-board',
    '.tg-feat-header',
    '.tg-feat-card',
    '.tg-compare-header',
    '.tg-compare-table',
    '.tg-compare-note',
    '.tg-price-header',
    '.tg-price-offer-plaque',
    '.tg-price-card',
    '.tg-faq-header',
    '.tg-faq-item',
    '.tg-cta-box',
  ];

  if (!reduced) {
    selectors.forEach(function (sel) {
      document.querySelectorAll(sel).forEach(function (el, i) {
        el.setAttribute('data-aos', 'fade-up');
        el.setAttribute('data-aos-duration', '650');
        el.setAttribute('data-aos-easing', 'ease-out-cubic');
        if (i % 4) el.setAttribute('data-aos-delay', String((i % 4) * 80));
      });
    });
  }

  if (window.AOS) {
    AOS.init({
      once: true,
      offset: 48,
      duration: 650,
      easing: 'ease-out-cubic',
      disable: reduced,
    });
  }
})();
