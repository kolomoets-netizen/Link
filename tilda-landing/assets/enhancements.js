(function () {
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (!reduced && window.Lenis) {
    var lenis = new Lenis({ duration: 0.9, smoothWheel: true });
    function raf(time) {
      lenis.raf(time);
      requestAnimationFrame(raf);
    }
    requestAnimationFrame(raf);
  }

  /* Только крупные секции — без «шоу» на каждой карточке */
  var selectors = [
    '.tg-how-header',
    '.tg-platform-header',
    '.tg-feat-header',
    '.tg-price-header',
    '.tg-faq-header',
    '.tg-cta-box',
  ];

  if (!reduced) {
    selectors.forEach(function (sel) {
      document.querySelectorAll(sel).forEach(function (el) {
        el.setAttribute('data-aos', 'fade-up');
        el.setAttribute('data-aos-duration', '500');
        el.setAttribute('data-aos-offset', '32');
      });
    });
  }

  if (window.AOS) {
    AOS.init({
      once: true,
      offset: 40,
      duration: 500,
      easing: 'ease-out-quart',
      disable: reduced,
    });
  }
})();
