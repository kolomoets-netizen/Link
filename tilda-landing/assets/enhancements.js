(function () {
  if (window.__istocklinkEnhancements) return;
  window.__istocklinkEnhancements = true;

  function boot() {
    var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var LenisCtor = window.Lenis || globalThis.Lenis;

    if (!reduced && LenisCtor) {
      new LenisCtor({
        autoRaf: true,
        duration: 1.2,
        smoothWheel: true,
        touchMultiplier: 1.2,
        anchors: true,
      });
    }

    var selectors = [
      '.tg-hero-inner > div:first-child',
      '.tg-hero-visual',
      '.tg-positioning-inner',
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
      '.tg-compare-matrix',
      '.tg-price-header',
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

    var modal = document.getElementById('tg-demo-modal');
    var tierEl = document.getElementById('tg-demo-modal-tier');

    function openDemoModal(tier) {
      if (!modal) return;
      if (tierEl) {
        if (tier) {
          tierEl.textContent = 'Тариф: ' + tier;
          tierEl.hidden = false;
        } else {
          tierEl.hidden = true;
        }
      }
      modal.classList.add('is-open');
      modal.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
      var input = modal.querySelector('.tg-demo-modal-input');
      if (input) setTimeout(function () { input.focus(); }, 50);
    }

    function closeDemoModal() {
      if (!modal) return;
      modal.classList.remove('is-open');
      modal.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
    }

    document.querySelectorAll('[data-demo-open]').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        openDemoModal(btn.getAttribute('data-tier') || '');
      });
    });

    document.querySelectorAll('[data-demo-close]').forEach(function (el) {
      el.addEventListener('click', closeDemoModal);
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeDemoModal();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
