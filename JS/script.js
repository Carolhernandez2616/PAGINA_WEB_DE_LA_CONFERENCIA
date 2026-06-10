/* ═══════════════════════════════════════════════════
   Colombia 5.0 — Agentes de IA | SENA
   JavaScript — script.js
   ═══════════════════════════════════════════════════ */

'use strict';

/* ──────────────────────────────────────────
   1. LANGUAGE SYSTEM
   Default: Español. Switch on button click.
   All translatable elements carry data-es / data-en.
   innerHTML-aware for tags like <em> and <strong>.
────────────────────────────────────────── */

let currentLang = 'es';

function setLang(lang) {
  if (lang === currentLang) return;
  currentLang = lang;

  // Toggle active class on buttons
  document.getElementById('btn-es').classList.toggle('active', lang === 'es');
  document.getElementById('btn-en').classList.toggle('active', lang === 'en');

  // Update html lang attribute
  document.documentElement.lang = lang;

  // Update all translatable elements
  const key = 'data-' + lang;
  document.querySelectorAll('[data-es][data-en]').forEach(function (el) {
    const val = el.getAttribute(key);
    if (!val) return;
    // Use innerHTML to support nested tags like <em>, <strong>
    el.innerHTML = val;
  });

  // Announce to screen readers
  const announcement = lang === 'es'
    ? 'Idioma cambiado a Español'
    : 'Language changed to English';
  announceToScreenReader(announcement);
}

function announceToScreenReader(msg) {
  const el = document.getElementById('sr-announce');
  if (!el) return;
  el.textContent = '';
  setTimeout(function () { el.textContent = msg; }, 50);
}

// Create live region for screen readers
(function () {
  const sr = document.createElement('div');
  sr.id = 'sr-announce';
  sr.setAttribute('aria-live', 'polite');
  sr.setAttribute('aria-atomic', 'true');
  Object.assign(sr.style, {
    position: 'absolute', width: '1px', height: '1px',
    overflow: 'hidden', clip: 'rect(0,0,0,0)',
    whiteSpace: 'nowrap'
  });
  document.body.appendChild(sr);
})();

/* ──────────────────────────────────────────
   2. SCROLL REVEAL
   Observe .reveal elements and add .visible
   when they enter the viewport.
────────────────────────────────────────── */

(function initScrollReveal() {
  const revealEls = document.querySelectorAll('.reveal');
  if (!revealEls.length) return;

  if (!('IntersectionObserver' in window)) {
    // Fallback: show all immediately
    revealEls.forEach(function (el) { el.classList.add('visible'); });
    return;
  }

  const observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          // Stagger children if multiple are in a grid
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
  );

  revealEls.forEach(function (el) { observer.observe(el); });
})();

/* ──────────────────────────────────────────
   3. NAVBAR — scroll shadow + hamburger menu
────────────────────────────────────────── */

(function initNavbar() {
  const navbar = document.getElementById('navbar');
  const hamburger = document.getElementById('hamburger');
  const navLinks = document.querySelector('.nav-links');

  // Scroll shadow
  window.addEventListener('scroll', function () {
    if (window.scrollY > 40) {
      navbar.style.boxShadow = '0 4px 30px rgba(0,0,0,0.5)';
    } else {
      navbar.style.boxShadow = 'none';
    }
  }, { passive: true });

  // Hamburger toggle
  if (hamburger && navLinks) {
    hamburger.addEventListener('click', function () {
      const isOpen = navLinks.classList.toggle('open');
      hamburger.setAttribute('aria-expanded', isOpen);
      animateHamburger(isOpen);
    });

    // Close on nav link click (mobile)
    navLinks.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        navLinks.classList.remove('open');
        hamburger.setAttribute('aria-expanded', 'false');
        animateHamburger(false);
      });
    });

    // Close on outside click
    document.addEventListener('click', function (e) {
      if (!navbar.contains(e.target)) {
        navLinks.classList.remove('open');
        hamburger.setAttribute('aria-expanded', 'false');
        animateHamburger(false);
      }
    });
  }

  function animateHamburger(open) {
    const spans = hamburger.querySelectorAll('span');
    if (open) {
      spans[0].style.transform = 'translateY(7px) rotate(45deg)';
      spans[1].style.opacity   = '0';
      spans[2].style.transform = 'translateY(-7px) rotate(-45deg)';
    } else {
      spans[0].style.transform = '';
      spans[1].style.opacity   = '';
      spans[2].style.transform = '';
    }
  }
})();

/* ──────────────────────────────────────────
   4. SMOOTH ACTIVE NAV LINKS
   Highlights nav link for section in viewport.
────────────────────────────────────────── */

(function initActiveNav() {
  const sections = document.querySelectorAll('section[id], div[id]');
  const navItems = document.querySelectorAll('.nav-links a');
  if (!sections.length || !navItems.length) return;

  const observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        const id = entry.target.getAttribute('id');
        navItems.forEach(function (a) {
          const href = a.getAttribute('href');
          if (href === '#' + id) {
            a.style.color = 'var(--blue-lt)';
          } else {
            a.style.color = '';
          }
        });
      });
    },
    { threshold: 0.4 }
  );

  sections.forEach(function (s) { observer.observe(s); });
})();

/* ──────────────────────────────────────────
   5. PLAY BUTTON INTERACTION
   Visual feedback for video placeholder clicks.
────────────────────────────────────────── */

(function initPlayButtons() {
  document.querySelectorAll('.play-circle').forEach(function (btn) {
    btn.addEventListener('click', function () {
      const box = btn.closest('.media-box');
      const caption = box ? box.querySelector('.media-caption') : null;

      // Pulse animation
      btn.style.transform = 'scale(0.9)';
      setTimeout(function () { btn.style.transform = ''; }, 150);

      // Tooltip message (bilingual)
      const msg = currentLang === 'es'
        ? '📹 Reemplaza este marcador con tu video del evento'
        : '📹 Replace this placeholder with your event video';
      showToast(msg);
    });
  });
})();

/* ──────────────────────────────────────────
   6. TOAST NOTIFICATION
────────────────────────────────────────── */

function showToast(message) {
  let toast = document.getElementById('toast-msg');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'toast-msg';
    Object.assign(toast.style, {
      position:        'fixed',
      bottom:          '2rem',
      left:            '50%',
      transform:       'translateX(-50%) translateY(20px)',
      background:      'rgba(15,22,48,0.97)',
      border:          '1px solid rgba(41,121,255,0.3)',
      color:           '#f0f4ff',
      padding:         '0.8rem 1.8rem',
      borderRadius:    '8px',
      fontSize:        '0.85rem',
      fontFamily:      "'DM Sans', sans-serif",
      zIndex:          '9999',
      opacity:         '0',
      transition:      'opacity 0.3s, transform 0.3s',
      pointerEvents:   'none',
      boxShadow:       '0 4px 30px rgba(0,0,0,0.5)',
      maxWidth:        '90vw',
      textAlign:       'center',
    });
    document.body.appendChild(toast);
  }

  toast.textContent = message;
  toast.style.opacity = '1';
  toast.style.transform = 'translateX(-50%) translateY(0)';

  clearTimeout(toast._timer);
  toast._timer = setTimeout(function () {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(-50%) translateY(20px)';
  }, 3500);
}

/* ──────────────────────────────────────────
   7. STATS COUNTER ANIMATION
   Animates numbers when stats bar comes into view.
────────────────────────────────────────── */

(function initCounters() {
  const statsBar = document.querySelector('.stats-bar');
  if (!statsBar) return;

  const numbers = statsBar.querySelectorAll('.sp-num');
  let animated = false;

  const observer = new IntersectionObserver(function (entries) {
    if (entries[0].isIntersecting && !animated) {
      animated = true;
      numbers.forEach(function (el) {
        const text = el.getAttribute('data-es') || el.textContent;
        // Extract number
        const match = text.match(/[\d.]+/);
        if (!match) return;
        const target = parseFloat(match[0]);
        const prefix = text.match(/^[^0-9]*/)[0] || '';
        const suffix = text.replace(/^[^0-9]*[\d.]+/, '');
        animateCount(el, 0, target, 1400, prefix, suffix);
      });
    }
  }, { threshold: 0.5 });

  observer.observe(statsBar);

  function animateCount(el, from, to, duration, prefix, suffix) {
    const start = performance.now();
    const isDecimal = to % 1 !== 0;
    function step(now) {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
      const value = from + (to - from) * eased;
      el.textContent = prefix + (isDecimal ? value.toFixed(1) : Math.round(value)) + suffix;
      if (progress < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
})();

/* ──────────────────────────────────────────
   8. GLOSSARY SEARCH FILTER
   Adds a live search to the glossary table.
────────────────────────────────────────── */

(function initGlossarySearch() {
  const table = document.querySelector('.gloss-table');
  if (!table) return;

  const wrap = document.querySelector('.gloss-table-wrap');
  const searchEl = document.createElement('input');
  searchEl.type = 'text';
  searchEl.id = 'gloss-search';
  searchEl.setAttribute('placeholder', '🔍  Buscar término / Search term...');
  Object.assign(searchEl.style, {
    display:       'block',
    width:         '100%',
    marginBottom:  '1rem',
    padding:       '0.75rem 1.2rem',
    background:    'rgba(15,22,48,0.8)',
    border:        '1px solid rgba(41,121,255,0.2)',
    borderRadius:  '8px',
    color:         '#f0f4ff',
    fontFamily:    "'DM Sans', sans-serif",
    fontSize:      '0.9rem',
    outline:       'none',
    transition:    'border-color 0.2s',
  });
  searchEl.addEventListener('focus', function () {
    searchEl.style.borderColor = 'rgba(41,121,255,0.6)';
  });
  searchEl.addEventListener('blur', function () {
    searchEl.style.borderColor = 'rgba(41,121,255,0.2)';
  });

  // Insert before table wrapper
  wrap.parentNode.insertBefore(searchEl, wrap);

  const rows = table.querySelectorAll('tbody tr');

  searchEl.addEventListener('input', function () {
    const q = searchEl.value.toLowerCase().trim();
    rows.forEach(function (row) {
      const text = row.textContent.toLowerCase();
      row.style.display = (!q || text.includes(q)) ? '' : 'none';
    });
  });
})();

/* ──────────────────────────────────────────
   9. BACK TO TOP BUTTON
────────────────────────────────────────── */

(function initBackToTop() {
  const btn = document.createElement('button');
  btn.id = 'back-top';
  btn.setAttribute('aria-label', 'Volver arriba');
  btn.innerHTML = '↑';
  Object.assign(btn.style, {
    position:     'fixed',
    bottom:       '1.8rem',
    right:        '1.8rem',
    width:        '44px',
    height:       '44px',
    borderRadius: '50%',
    background:   'linear-gradient(135deg, #2979ff, #ff6d00)',
    color:        '#fff',
    border:       'none',
    fontSize:     '1.1rem',
    cursor:       'pointer',
    zIndex:       '500',
    opacity:      '0',
    transform:    'translateY(16px)',
    transition:   'opacity 0.3s, transform 0.3s',
    pointerEvents:'none',
    display:      'flex',
    alignItems:   'center',
    justifyContent:'center',
    boxShadow:    '0 4px 20px rgba(41,121,255,0.4)',
  });
  document.body.appendChild(btn);

  window.addEventListener('scroll', function () {
    const show = window.scrollY > 400;
    btn.style.opacity      = show ? '1' : '0';
    btn.style.transform    = show ? 'translateY(0)' : 'translateY(16px)';
    btn.style.pointerEvents= show ? 'auto' : 'none';
  }, { passive: true });

  btn.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
})();

/* ──────────────────────────────────────────
   10. INIT on DOM ready
────────────────────────────────────────── */

document.addEventListener('DOMContentLoaded', function () {
  // Ensure page starts in Spanish
  setLang('es');

  // Expose setLang globally (called from HTML buttons)
  window.setLang = setLang;
});
