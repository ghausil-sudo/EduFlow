document.addEventListener('DOMContentLoaded', function() {
  AOS.init({
    duration: 700,
    easing: 'ease-out-cubic',
    once: true,
    offset: 80,
  });

  const navbar = document.getElementById('siteNavbar');
  if (navbar) {
    const handleScroll = () => {
      if (window.scrollY > 40) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }
    };
    handleScroll();
    window.addEventListener('scroll', handleScroll, { passive: true });
  }

  document.querySelectorAll('form').forEach((form) => {
    form.addEventListener('submit', function(e) {
      const btn = form.querySelector('button[type="submit"]');
      if (!btn) return;
      const originalText = btn.innerHTML;
      btn.classList.add('loading');
      btn.innerHTML = '<span class="btn-text">Memproses...</span>';

      const onDone = () => {
        btn.classList.remove('loading');
        btn.innerHTML = originalText;
        form.removeEventListener('submit', onDone);
      };

      setTimeout(() => {
        if (document.body.contains(btn)) onDone();
      }, 3000);
    });
  });

  const alerts = document.querySelectorAll('[data-auto-dismiss]');
  alerts.forEach((alert) => {
    const ms = parseInt(alert.getAttribute('data-auto-dismiss') || '4000', 10);
    setTimeout(() => {
      alert.classList.add('fade-out');
      setTimeout(() => alert.remove(), 500);
    }, ms);
  });

  const counters = document.querySelectorAll('[data-count]');
  counters.forEach((el) => {
    const target = +el.getAttribute('data-count');
    const duration = 1500;
    const startTime = performance.now();
    function update(currentTime) {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const ease = 1 - Math.pow(1 - progress, 3);
      el.textContent = Math.floor(target * ease).toLocaleString('id-ID');
      if (progress < 1) requestAnimationFrame(update);
    }
    requestAnimationFrame(update);
  });

  const progressBars = document.querySelectorAll('.progress-bar-animated');
  progressBars.forEach((bar) => {
    const width = bar.getAttribute('data-width');
    setTimeout(() => { bar.style.width = width; }, 400);
  });

  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener('click', function(e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  /* === Ilustrasi Buku 3D Interaktif - Hero Section === */
  const bookWrapper = document.getElementById('book3d');
  if (bookWrapper) {
    const book = bookWrapper.querySelector('.book-3d');
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const isMobile = window.innerWidth < 768;

    if (!reducedMotion && !isMobile) {
      const heroSection = document.querySelector('.hero-section');
      if (heroSection) {
        heroSection.addEventListener('mousemove', (e) => {
          const rect = heroSection.getBoundingClientRect();
          const x = e.clientX - rect.left;
          const y = e.clientY - rect.top;
          const centerX = rect.width / 2;
          const centerY = rect.height / 2;
          const rotateX = ((y - centerY) / centerY) * -10;
          const rotateY = ((x - centerX) / centerX) * 10;
          book.style.animation = 'none';
          book.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
        });

        heroSection.addEventListener('mouseleave', () => {
          book.style.animation = 'bookFloat 3.5s ease-in-out infinite';
          book.style.transform = '';
        });
      }
    }

    bookWrapper.addEventListener('click', () => {
      if (reducedMotion) return;
      bookWrapper.classList.toggle('flipped');
    });
  }
});
