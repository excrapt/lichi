// Lichi site: header hairline on scroll, reveal-on-scroll, and a guard against being shown inside someone else's frame.
(function () {
  // Clickjacking guard: GitHub Pages cannot send frame-ancestors / X-Frame-Options, so leave any foreign frame.
  try {
    if (window.top !== window.self) { window.top.location = window.self.location.href; }
  } catch (e) {
    document.documentElement.style.display = 'none';
  }

  var head = document.querySelector('.site-head');
  if (head) {
    var onScroll = function () { head.classList.toggle('scrolled', window.scrollY > 8); };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  var items = document.querySelectorAll('[data-reveal]');
  if (!('IntersectionObserver' in window)) {
    items.forEach(function (el) { el.classList.add('in'); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    });
  }, { threshold: 0, rootMargin: '0px 0px 12% 0px' });
  items.forEach(function (el) { io.observe(el); });
})();
