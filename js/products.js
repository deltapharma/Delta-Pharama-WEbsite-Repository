/* Delta Pharma — product catalogue: category filter, search and detail popup */
(function () {
  'use strict';

  var dataEl = document.getElementById('product-data');
  if (!dataEl) return;
  var products = JSON.parse(dataEl.textContent);

  var cards = Array.prototype.slice.call(document.querySelectorAll('.category-card'));
  var groups = Array.prototype.slice.call(document.querySelectorAll('.product-group'));
  var search = document.getElementById('product-search');
  var empty = document.getElementById('product-empty');
  var active = 'all';

  // Text each product card is searched against
  document.querySelectorAll('.product').forEach(function (btn) {
    var p = products[+btn.dataset.product];
    btn.dataset.search = (p.name + ' ' + p.cls + ' ' + p.form + ' ' +
      p.composition.map(function (c) { return c[0]; }).join(' ')).toLowerCase();
  });

  function applyFilter() {
    var q = search ? search.value.trim().toLowerCase() : '';
    var shown = 0;
    groups.forEach(function (g) {
      var inCat = active === 'all' || g.dataset.category === active;
      var visible = 0;
      g.querySelectorAll('.product').forEach(function (btn) {
        var ok = inCat && (!q || btn.dataset.search.indexOf(q) !== -1);
        btn.parentElement.hidden = !ok;
        if (ok) visible++;
      });
      g.hidden = visible === 0;
      shown += visible;
    });
    if (empty) empty.hidden = shown !== 0;
  }

  cards.forEach(function (card) {
    card.addEventListener('click', function () {
      active = card.dataset.filter;
      cards.forEach(function (c) {
        var on = c === card;
        c.classList.toggle('is-active', on);
        c.setAttribute('aria-pressed', String(on));
      });
      applyFilter();
    });
  });
  if (search) search.addEventListener('input', applyFilter);

  // ----- Detail popup -----
  var dialog = document.getElementById('product-dialog');
  var main = document.getElementById('pd-main');
  var thumbs = document.getElementById('pd-thumbs');

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (ch) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[ch];
    });
  }
  function src(name) { return 'assets/images/products/' + name + '.jpg'; }

  function showImage(p, k) {
    main.innerHTML = p.images.length
      ? '<img src="' + src(p.images[k]) + '" alt="' + esc(p.name) + ', photo ' + (k + 1) + '">'
      : '<span class="product-noimg"><b>' + esc(p.name) + '</b><small>Photo coming soon</small></span>';
    Array.prototype.forEach.call(thumbs.children, function (b, j) {
      b.setAttribute('aria-current', String(j === k));
    });
  }

  function openDialog(i) {
    var p = products[i];
    document.getElementById('pd-category').textContent = p.category;
    document.getElementById('pd-name').textContent = p.name;
    document.getElementById('pd-class').textContent = p.cls;
    document.getElementById('pd-label').textContent =
      p.category === 'Tablets' ? 'Each tablet contains' :
      p.category === 'Capsules' ? 'Each capsule contains' : 'Composition';
    document.getElementById('pd-composition').innerHTML = p.composition.map(function (c) {
      return '<li><span>' + esc(c[0]) + '</span><span>' + esc(c[1]) + '</span></li>';
    }).join('');
    var specs = [
      ['Dosage form', p.form],
      ['Pack size', p.pack || 'On request'],
      ['Specification', p.spec + (p.spec.indexOf('International') === 0 ? '' : ' specification')],
      ['Registration no.', p.reg],
      ['M.R.P.', p.mrp ? 'Rs ' + p.mrp : 'On request'],
      ['Category', p.category]
    ];
    document.getElementById('pd-specs').innerHTML = specs.map(function (s) {
      return '<div><dt>' + s[0] + '</dt><dd>' + esc(s[1]) + '</dd></div>';
    }).join('');
    thumbs.innerHTML = p.images.length > 1 ? p.images.map(function (im, k) {
      return '<button type="button" data-k="' + k + '" aria-label="Show photo ' + (k + 1) + '"><img src="' + src(im) + '" alt=""></button>';
    }).join('') : '';
    thumbs.onclick = function (e) {
      var b = e.target.closest('button');
      if (b) showImage(p, +b.dataset.k);
    };
    showImage(p, 0);

    // Pre-select "Product enquiry" and mention the product in the contact form
    var enquire = document.getElementById('pd-enquire');
    enquire.onclick = function () {
      dialog.close();
      var msg = document.getElementById('message');
      var topic = document.getElementById('topic');
      if (topic) topic.value = 'Product enquiry';
      if (msg && !msg.value.trim()) msg.value = 'I would like to know more about ' + p.name + '.';
    };

    if (typeof dialog.showModal === 'function') dialog.showModal();
    else dialog.setAttribute('open', '');
  }

  document.getElementById('product-catalogue').addEventListener('click', function (e) {
    var btn = e.target.closest('.product');
    if (btn) openDialog(+btn.dataset.product);
  });

  function wireClose(dlg, closeBtn) {
    if (!dlg) return;
    closeBtn.addEventListener('click', function () { dlg.close(); });
    dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
  }
  wireClose(dialog, document.getElementById('pd-close'));

  // ----- Licence popup -----
  var licence = document.getElementById('licence-dialog');
  var licenceOpen = document.getElementById('licence-open');
  if (licence && licenceOpen) {
    licenceOpen.addEventListener('click', function () {
      if (typeof licence.showModal === 'function') licence.showModal();
      else licence.setAttribute('open', '');
    });
    wireClose(licence, document.getElementById('licence-close'));
  }
})();
