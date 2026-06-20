/* ── Page Loader ── */
function hideLoader() {
  const loader = document.getElementById('page-loader');
  if (loader) {
    loader.classList.add('hidden');
    setTimeout(() => loader.remove(), 500);
  }
}
if (document.readyState === 'complete') {
  hideLoader();
} else {
  window.addEventListener('load', hideLoader);
}
setTimeout(hideLoader, 2000); // fallback

/* ── Theme Toggle ── */
document.addEventListener('DOMContentLoaded', () => {
  const toggle    = document.getElementById('themeToggle');
  const themeIcon = document.getElementById('themeIcon');
  const html      = document.documentElement;
  const saved     = localStorage.getItem('theme') || 'dark';

  html.setAttribute('data-theme', saved);
  updateIcon(saved);

  if (toggle) {
    toggle.addEventListener('click', () => {
      const current = html.getAttribute('data-theme');
      const next    = current === 'dark' ? 'light' : 'dark';
      html.setAttribute('data-theme', next);
      localStorage.setItem('theme', next);
      updateIcon(next);
    });
  }

  function updateIcon(theme) {
    if (!themeIcon) return;
    themeIcon.className = theme === 'dark' ? 'fas fa-moon' : 'fas fa-sun';
  }

  /* ── Scroll Reveal ── */
  const observer = new IntersectionObserver(
    entries => entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); }),
    { threshold: 0.1 }
  );
  document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

  /* ── Back to Top ── */
  const btn = document.getElementById('backToTop');
  window.addEventListener('scroll', () => {
    if (btn) btn.classList.toggle('visible', window.scrollY > 400);
  });
  if (btn) btn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

  /* ── Gallery Votes ── */
  const voteDataEl = document.getElementById('gallery-votes-data');
  const voteBars = document.querySelectorAll('.slide-vote-bar');

  if (voteDataEl && voteBars.length) {
    const galleryVotes = JSON.parse(voteDataEl.textContent || '{}');

    function getCookie(name) {
      const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
      return match ? decodeURIComponent(match[2]) : null;
    }

    function applyVoteState(bar, voteType) {
      bar.querySelectorAll('.vote-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.vote === voteType);
      });
    }

    voteBars.forEach(bar => {
      const itemId = bar.dataset.itemId;
      applyVoteState(bar, galleryVotes[itemId] || null);
    });

    voteBars.forEach(bar => {
      bar.addEventListener('click', async (event) => {
        const btn = event.target.closest('.vote-btn');
        if (!btn || btn.disabled) return;

        const itemId = bar.dataset.itemId;
        const voteType = btn.dataset.vote;
        const buttons = bar.querySelectorAll('.vote-btn');
        buttons.forEach(b => { b.disabled = true; });

        try {
          const response = await fetch('/api/gallery/vote/', {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({ item_id: Number(itemId), vote_type: voteType }),
          });

          if (!response.ok) throw new Error('Vote request failed');

          const data = await response.json();
          galleryVotes[itemId] = data.vote_type;
          applyVoteState(bar, data.vote_type);
        } catch (err) {
          console.error(err);
        } finally {
          buttons.forEach(b => { b.disabled = false; });
        }
      });
    });
  }

  /* ── Project Filter ── */
  document.querySelectorAll('.filter-btn').forEach(b => {
    b.addEventListener('click', function () {
      document.querySelectorAll('.filter-btn').forEach(x => x.classList.remove('active'));
      this.classList.add('active');
      const filter = this.dataset.filter;
      document.querySelectorAll('.project-item').forEach(item => {
        item.style.display = filter === 'all' || item.dataset.category === filter ? 'block' : 'none';
      });
    });
  });
});

/* ── My Gallery Carousel ── */
  const slidesEl  = document.getElementById('gallerySlides');
  const prevBtn2  = document.getElementById('galleryPrev');
  const nextBtn2  = document.getElementById('galleryNext');
  const dotsEl    = document.getElementById('galleryDots');

  if (slidesEl && prevBtn2 && nextBtn2) {
    const items = slidesEl.querySelectorAll('.slide-item');
    const total = items.length;
    let current = 0;
    let timer;

    // Build dots dynamically
    dotsEl.innerHTML = '';
    items.forEach((_, i) => {
      const d = document.createElement('div');
      d.className = 'dot' + (i === 0 ? ' active' : '');
      d.addEventListener('click', () => { goTo(i); resetTimer(); });
      dotsEl.appendChild(d);
    });

    const allDots = dotsEl.querySelectorAll('.dot');

    function goTo(i) {
      current = (i + total) % total;
      slidesEl.style.transform = `translateX(${-current * 100}%)`;
      allDots.forEach(d => d.classList.remove('active'));
      if (allDots[current]) allDots[current].classList.add('active');
    }

    function resetTimer() {
      clearInterval(timer);
      timer = setInterval(() => goTo(current + 1), 3000);
    }

    prevBtn2.addEventListener('click', () => { goTo(current - 1); resetTimer(); });
    nextBtn2.addEventListener('click', () => { goTo(current + 1); resetTimer(); });

    // Touch / swipe
    let touchStartX = 0;
    slidesEl.addEventListener('touchstart', e => { touchStartX = e.touches[0].clientX; }, { passive: true });
    slidesEl.addEventListener('touchend', e => {
      const diff = touchStartX - e.changedTouches[0].clientX;
      if (Math.abs(diff) > 40) { goTo(diff > 0 ? current + 1 : current - 1); resetTimer(); }
    });

    // Pause on hover
    slidesEl.closest('.slider').addEventListener('mouseenter', () => clearInterval(timer));
    slidesEl.closest('.slider').addEventListener('mouseleave', resetTimer);

    // Init
    goTo(0);
    resetTimer();
  }