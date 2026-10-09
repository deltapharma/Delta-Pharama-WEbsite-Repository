/* Delta Pharma — site interactions */
(function () {
  'use strict';

  // Email address that receives contact-form messages. Change this.
  var CONTACT_EMAIL = 'info@example.com';

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
  // No server is needed: on submit the visitor's email app opens with the
  // message pre-filled. To use a form service (Formspree, Netlify Forms, etc.)
  // instead, set the form's action/method and remove this handler.
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
        var bad = !pair[1] || (pair[0] === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(pair[1]));
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
      var body = 'Name: ' + name + '\nEmail: ' + email +
        (form.elements.phone.value.trim() ? '\nPhone: ' + form.elements.phone.value.trim() : '') +
        '\n\n' + message;

      window.location.href = 'mailto:' + CONTACT_EMAIL +
        '?subject=' + encodeURIComponent(subject) +
        '&body=' + encodeURIComponent(body);

      status.textContent = 'Thank you — your email app should open with your message ready to send.';
      status.className = 'form-status caption is-success';
    });
  }
})();
