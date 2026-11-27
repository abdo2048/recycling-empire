/* Recycling Empire — site behaviour: search overlay, sources filter, TOC scroll-spy.
   No dependencies; every page works without this file. */
(function () {
  "use strict";
  var rootMeta = document.querySelector('meta[name="doc-root"]');
  var ROOT = rootMeta ? rootMeta.getAttribute("content") : "./";

  /* ---------- search overlay ---------- */
  var overlay = document.getElementById("soverlay");
  var btn = document.getElementById("searchbtn");
  var input = document.getElementById("sinput");
  var results = document.getElementById("sresults");
  var INDEX = null;
  var sel = -1;
  var current = [];

  function loadIndex() {
    if (INDEX) return Promise.resolve(INDEX);
    return fetch(ROOT + "assets/search-index.json")
      .then(function (r) { return r.json(); })
      .then(function (j) { INDEX = j; return j; })
      .catch(function () { INDEX = []; return INDEX; });
  }

  function score(entry, q) {
    var t = entry.t.toLowerCase(), s = entry.s || "", x = (entry.x || "").toLowerCase();
    var sc = 0;
    if (t === q) sc += 60;
    if (t.indexOf(q) === 0) sc += 40;
    if (t.indexOf(q) !== -1) sc += 24;
    if (s.indexOf(q) !== -1) sc += 8;
    if (x.indexOf(q) !== -1) sc += 6;
    return sc;
  }

  function search(q) {
    if (!q) { results.innerHTML = ""; return; }
    var terms = q.toLowerCase().split(/\s+/).filter(Boolean);
    var hits = [];
    for (var i = 0; i < INDEX.length; i++) {
      var total = 0;
      for (var j = 0; j < terms.length; j++) total += score(INDEX[i], terms[j]);
      if (total > 0) hits.push({ e: INDEX[i], sc: total });
    }
    hits.sort(function (a, b) { return b.sc - a.sc; });
    current = hits.slice(0, 12);
    sel = -1;
    results.innerHTML = current.map(function (h, k) {
      var url = ROOT + h.e.u.replace(/^\.\//, "");
      return '<a href="' + url + '" data-i="' + k + '">' +
        '<div class="st">' + escapeHtml(h.e.t) + '</div>' +
        (h.e.s ? '<div class="ss">' + escapeHtml(h.e.s) + '</div>' : '') +
        '<div class="sx">' + escapeHtml((h.e.x || "").slice(0, 180)) + '…</div></a>';
    }).join("") || '<p class="shint">No results.</p>';
  }

  function escapeHtml(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function openOverlay() {
    overlay.hidden = false;
    loadIndex().then(function () { input.focus(); });
  }
  function closeOverlay() { overlay.hidden = true; }

  if (btn) btn.addEventListener("click", openOverlay);
  if (overlay) overlay.addEventListener("click", function (e) { if (e.target === overlay) closeOverlay(); });
  document.addEventListener("keydown", function (e) {
    if ((e.ctrlKey || e.metaKey) && (e.key === "k" || e.key === "K")) { e.preventDefault(); openOverlay(); }
    if (e.key === "/" && !overlay.hidden === false && document.activeElement.tagName !== "INPUT") { openOverlay(); }
    if (e.key === "Escape") closeOverlay();
    if ((e.key === "ArrowDown" || e.key === "ArrowUp") && current.length) {
      e.preventDefault();
      sel = e.key === "ArrowDown" ? Math.min(sel + 1, current.length - 1) : Math.max(sel - 1, 0);
      var links = results.querySelectorAll("a");
      for (var i = 0; i < links.length; i++) links[i].classList.toggle("sel", i === sel);
    }
    if (e.key === "Enter" && !overlay.hidden && current.length) {
      var go = sel >= 0 ? current[sel] : current[0];
      if (go) { e.preventDefault(); window.location.href = ROOT + go.e.u.replace(/^\.\//, ""); }
    }
  });
  if (input) input.addEventListener("input", function () { loadIndex().then(function () { search(input.value.trim()); }); });

  /* ---------- sources filter ---------- */
  var filter = document.getElementById("srcfilter");
  var table = document.getElementById("srctable");
  if (filter && table) {
    filter.addEventListener("input", function () {
      var q = filter.value.toLowerCase();
      var rows = table.querySelectorAll("tbody tr");
      for (var i = 0; i < rows.length; i++) {
        rows[i].style.display = rows[i].textContent.toLowerCase().indexOf(q) !== -1 ? "" : "none";
      }
    });
  }

  /* ---------- TOC scroll-spy ---------- */
  var toc = document.querySelector(".toc");
  if (toc) {
    var links = toc.querySelectorAll("a[href^='#']");
    var heads = [];
    for (var i = 0; i < links.length; i++) {
      var id = links[i].getAttribute("href").slice(1);
      var el = document.getElementById(id);
      if (el) heads.push({ a: links[i], el: el });
    }
    if (heads.length && "IntersectionObserver" in window) {
      var active = null;
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) {
            if (active) active.a.classList.remove("active");
            for (var i = 0; i < heads.length; i++) {
              if (heads[i].el === en.target) { active = heads[i]; heads[i].a.classList.add("active"); break; }
            }
          }
        });
      }, { rootMargin: "0px 0px -70% 0px" });
      heads.forEach(function (h) { io.observe(h.el); });
    }
  }
})();
