/* Delta Pharma — site interactions */
(function () {
  'use strict';

  // Contact-form messages are sent to this WhatsApp number
  // (international format, digits only: 92 + number without the leading 0).
  // To receive them by email instead, add an address to CONTACT_EMAIL.
  var CONTACT_WHATSAPP = '923439104456';
  var CONTACT_EMAIL = '';

  var header = document.querySelector('.site-header');
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');

  // ----- Mobile menu -----
  function closeMenu() {
    nav.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Open menu');
  }

  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) closeMenu();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeMenu();
    });
  }

  // ----- Header shadow on scroll -----
  function onScroll() {
    header.classList.toggle('is-scrolled', window.scrollY > 8);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // ----- Active nav link + reveal animations -----
  if ('IntersectionObserver' in window) {
    var links = document.querySelectorAll('.nav-link');
    var sectionObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        links.forEach(function (l) {
          l.classList.toggle('is-active', l.getAttribute('href') === '#' + entry.target.id);
        });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    document.querySelectorAll('main section[id]').forEach(function (s) { sectionObserver.observe(s); });

    var revealTargets = document.querySelectorAll(
      '.section-head, .split > *, .process li, .card, .why-item'
    );
    var revealObserver = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    revealTargets.forEach(function (el) {
      el.classList.add('reveal');
      revealObserver.observe(el);
    });
  }

  // ----- Footer year -----
  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();

  // ----- Contact form -----
  // No server is needed: on submit the message opens pre-filled in WhatsApp
  // (or the visitor's email app, if CONTACT_EMAIL is set).
  var form = document.getElementById('contact-form');
  var status = document.getElementById('form-status');

  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var name = form.elements.name.value.trim();
      var email = form.elements.email.value.trim();
      var message = form.elements.message.value.trim();
      var invalid = [];

      [['name', name], ['email', email], ['message', message]].forEach(function (pair) {
        var field = form.elements[pair[0]];
        var bad = pair[0] === 'email'
          ? (pair[1] !== '' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(pair[1]))
          : !pair[1];
        field.setAttribute('aria-invalid', bad ? 'true' : 'false');
        if (bad) invalid.push(field);
      });

      if (invalid.length) {
        status.textContent = 'Please complete the highlighted fields.';
        status.className = 'form-status caption is-error';
        invalid[0].focus();
        return;
      }

      var subject = 'Website enquiry: ' + form.elements.topic.value;
      var phone = form.elements.phone.value.trim();
      var body = 'Name: ' + name +
        (email ? '\nEmail: ' + email : '') +
        (phone ? '\nPhone: ' + phone : '') +
        '\n\n' + message;

      if (CONTACT_EMAIL) {
        window.location.href = 'mailto:' + CONTACT_EMAIL +
          '?subject=' + encodeURIComponent(subject) +
          '&body=' + encodeURIComponent(body);
        status.textContent = 'Thank you — your email app should open with your message ready to send.';
      } else {
        window.open('https://wa.me/' + CONTACT_WHATSAPP + '?text=' +
          encodeURIComponent(subject + '\n' + body), '_blank', 'noopener');
        status.textContent = 'Thank you — WhatsApp should open with your message ready to send.';
      }
      status.className = 'form-status caption is-success';
    });
  }
})();
