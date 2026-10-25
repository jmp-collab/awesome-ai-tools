/* KI-Werkstatt – Seitenlogik. Kein Framework, keine Abhängigkeiten. */
(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return [].slice.call((r || document).querySelectorAll(s)); };
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };

  /* Theme-Umschalter */
  var root = document.documentElement;
  var saved = store.get("kw-theme");
  if (saved) root.setAttribute("data-theme", saved);
  var tbtn = $("#theme");
  if (tbtn) tbtn.addEventListener("click", function () {
    var dark = root.getAttribute("data-theme") === "dark" ||
      (!root.getAttribute("data-theme") && window.matchMedia("(prefers-color-scheme: dark)").matches);
    var next = dark ? "light" : "dark";
    root.setAttribute("data-theme", next); store.set("kw-theme", next);
  });

  /* Suche + Filter über die Tool-Liste */
  var q = $("#q"), count = $("#count"), items = $$("ul.tools li");
  var feu = $$("input.f-eu"), foss = $$("input.f-oss");
  var main = $("main.content");
  function uniq(list) { var u = {}; list.forEach(function (li) { u[li.querySelector("a.name").href] = 1; }); return Object.keys(u).length; }
  function run() {
    var s = (q ? q.value : "").trim().toLowerCase();
    var eu = feu.some(function (c) { return c.checked; }), oss = foss.some(function (c) { return c.checked; }), filtering = !!(s || eu || oss);
    items.forEach(function (li) {
      var ok = (!s || li.dataset.search.indexOf(s) > -1) && (!eu || li.dataset.eu === "1") && (!oss || li.dataset.oss === "1");
      li.classList.toggle("hidden", !ok);
    });
    $$("section.cat").forEach(function (sec) {
      var any = !!sec.querySelector("ul.tools li:not(.hidden)");
      sec.classList.toggle("hidden", filtering && !any);
      $$("ul.tools", sec).forEach(function (ul) {
        var has = !!ul.querySelector("li:not(.hidden)");
        ul.classList.toggle("hidden", filtering && !has);
        var h3 = ul.previousElementSibling;
        while (h3 && h3.tagName !== "H3" && h3.tagName !== "H2") h3 = h3.previousElementSibling;
        if (h3 && h3.tagName === "H3") h3.classList.toggle("hidden", filtering && !has);
      });
      $$("aside, p, .table, ul.plain, ol.plain, .cat-art", sec).forEach(function (el) { el.classList.toggle("hidden", filtering); });
    });
    if (count) count.textContent = filtering ? uniq(items.filter(function (li) { return !li.classList.contains("hidden"); })) + " von " + uniq(items) + " Tools" : uniq(items) + " Tools";
    if (filtering) {
      // Zum ersten sichtbaren Treffer scrollen, egal in welcher Liste er steht
      var first = items.filter(function (li) { return !li.classList.contains("hidden"); })[0];
      if (first) {
        var r = first.getBoundingClientRect();
        if (r.top < 120 || r.bottom > window.innerHeight) window.scrollTo({ top: r.top + window.scrollY - 140, behavior: reduce ? "auto" : "smooth" });
      }
    }
  }
  [q].concat(feu, foss).forEach(function (el) { if (el) el.addEventListener("input", function (e) { if (e.target.type === "checkbox") { (e.target.classList.contains("f-eu") ? feu : foss).forEach(function (c) { c.checked = e.target.checked; }); } run(); }); });
  var sf = $("#searchform"); if (sf) sf.addEventListener("submit", function (e) { e.preventDefault(); run(); });
  run();

  /* Scroll: Fortschritt, Topbutton, Sticky-Leiste, Parallax */
  var prog = $("#progress"), totop = $("#totop"), bar = $("#stickybar");
  var floats = $$(".float");
  var barDone = store.get("kw-bar") === "1";
  var ticking = false;
  function onScroll() {
    if (ticking) return; ticking = true;
    requestAnimationFrame(function () {
      var h = document.documentElement, max = h.scrollHeight - h.clientHeight, y = window.scrollY, p = max > 0 ? y / max : 0;
      if (prog) prog.style.width = (p * 100).toFixed(2) + "%";
      if (totop) totop.classList.toggle("show", y > 900);
      if (bar && !barDone) { var show = p > 0.3; bar.classList.toggle("show", show); document.body.classList.toggle("has-bar", show); }
      if (!reduce) floats.forEach(function (f) {
        var d = parseFloat(f.dataset.depth || "0.2");
        f.style.transform = "translate3d(0," + (y * d * -0.4).toFixed(1) + "px,0) rotate(" + (y * d * 0.02).toFixed(2) + "deg)";
      });
      ticking = false;
    });
  }
  window.addEventListener("scroll", onScroll, { passive: true }); onScroll();
  if (totop) totop.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" }); });
  var barClose = $("#stickybar .close");
  if (barClose) barClose.addEventListener("click", function () { bar.classList.remove("show"); document.body.classList.remove("has-bar"); barDone = true; store.set("kw-bar", "1"); });
  var barForm = $("#stickybar form"); if (barForm) barForm.addEventListener("submit", function () { store.set("kw-bar", "1"); });

  /* Reveal beim Scrollen */
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -8% 0px" });
    $$(".reveal").forEach(function (el) { io.observe(el); });
  } else { $$(".reveal").forEach(function (el) { el.classList.add("in"); }); }

  /* Zähler in den Stat-Kacheln */
  function countUp(el) {
    var end = parseInt(el.dataset.count, 10), start = 0, t0 = null, dur = 1200;
    if (reduce || !end) { el.textContent = end; return; }
    function step(ts) { if (!t0) t0 = ts; var k = Math.min(1, (ts - t0) / dur); k = 1 - Math.pow(1 - k, 3); el.textContent = Math.round(start + (end - start) * k); if (k < 1) requestAnimationFrame(step); }
    requestAnimationFrame(step);
  }
  if ("IntersectionObserver" in window) {
    var io2 = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { countUp(e.target); io2.unobserve(e.target); } }); });
    $$("[data-count]").forEach(function (el) { io2.observe(el); });
  } else { $$("[data-count]").forEach(countUp); }

  /* Scroll-Spy für die Seitenleiste */
  var railLinks = $$(".rail a[href^='#']"), secs = railLinks.map(function (a) { return $(a.getAttribute("href")); }).filter(Boolean);
  if (secs.length && "IntersectionObserver" in window) {
    var cur = null;
    var io3 = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) cur = e.target.id; });
      railLinks.forEach(function (a) { a.classList.toggle("on", a.getAttribute("href") === "#" + cur); });
    }, { rootMargin: "-20% 0px -70% 0px" });
    secs.forEach(function (s) { io3.observe(s); });
  }

  /* Stack-Finder */
  var F = window.KW_FINDER, TOOLS = window.KW_TOOLS || {};
  var finder = $("#finder");
  if (F && finder) {
    var ans = {}, stepIdx = 0;
    var qEl = $(".finder-q", finder), optsEl = $(".opts", finder), dots = $(".dots", finder), back = $(".back", finder), res = $(".finder-result", finder), stepLbl = $(".steplbl", finder);
    function icon(id) { return '<svg class="ico"><use href="#i-' + id + '"/></svg>'; }
    function fav(url) { try { var h = new URL(url).hostname; return '<img loading="lazy" alt="" src="https://icons.duckduckgo.com/ip3/' + h + '.ico">'; } catch (e) { return ""; } }
    function render() {
      var step = F.questions[stepIdx];
      res.classList.add("hidden"); qEl.classList.remove("hidden"); optsEl.classList.remove("hidden");
      qEl.textContent = step.q;
      optsEl.innerHTML = step.options.map(function (o) {
        return '<button type="button" class="opt' + (ans[step.id] === o[0] ? " on" : "") + '" data-v="' + o[0] + '">' + icon(o[2]) + '<span>' + o[1] + '</span></button>';
      }).join("");
      dots.innerHTML = F.questions.map(function (_, i) { return "<i" + (i <= stepIdx ? ' class="on"' : "") + "></i>"; }).join("");
      stepLbl.textContent = "Frage " + (stepIdx + 1) + " von " + F.questions.length;
      back.classList.toggle("hidden", stepIdx === 0);
      $$(".opt", optsEl).forEach(function (b) {
        b.addEventListener("click", function () {
          ans[step.id] = b.dataset.v;
          if (stepIdx < F.questions.length - 1) { stepIdx++; render(); } else { showResult(); }
        });
      });
    }
    function showResult() {
      var list = (F.base[ans.ziel] || []).slice();
      if (ans.daten === "eu") list = list.map(function (n) { return F.eu_swap[n] || n; });
      if (ans.team === "firma") F.firma_add.forEach(function (n) { if (list.indexOf(n) < 0) list.push(n); });
      list = list.filter(function (n, i) { return list.indexOf(n) === i; });
      var cards = list.map(function (n) {
        var t = TOOLS[n]; if (!t) return "";
        return '<a href="' + t.u + '" target="_blank" rel="noopener">' + fav(t.u) + '<span><b>' + n + (t.eu ? ' <span class="badge eu">EU</span>' : "") + '</b><small>' + t.d + '</small></span></a>';
      }).join("");
      var notes = [F.notes[ans.team], ans.daten === "eu" ? F.notes.eu : ""].filter(Boolean).map(function (n) { return '<p class="note">' + n + "</p>"; }).join("");
      var stackText = list.join(", ");
      res.innerHTML = '<p class="eyebrow">Dein Setup</p><h3 class="finder-q">' + list.length + ' Tools, die zu deinem Fall passen</h3>' +
        '<div class="result-tools">' + cards + "</div>" + notes +
        '<form class="form" action="https://formsubmit.co/' + F.to + '" method="POST" style="margin-top:18px;box-shadow:none;border:1px solid var(--line)">' +
        '<input type="hidden" name="_subject" value="Stack-Check (Finder) – KI-Werkstatt"><input type="hidden" name="_template" value="table"><input type="hidden" name="_captcha" value="false">' +
        '<input type="hidden" name="_next" value="' + F.next + '">' +
        '<input type="text" name="_honey" class="honey" tabindex="-1" autocomplete="off">' +
        '<input type="hidden" name="quelle" value="Stack-Finder"><input type="hidden" name="antworten" value="' + [ans.ziel, ans.daten, ans.team].join(" / ") + '"><input type="hidden" name="vorschlag" value="' + stackText.replace(/"/g, "&quot;") + '">' +
        '<p style="margin:0 0 4px;font:700 18px var(--font-d)">Soll Jean da noch mal drüberschauen?</p><p style="margin:0;color:#5B616B;font-size:14px">Du bekommst das Setup mit Anmerkungen zu deinem Fall per Mail. Kostenlos, ohne Pitch.</p>' +
        '<div class="row"><div><label>Name</label><input name="name" required></div><div><label>E-Mail</label><input type="email" name="email" required></div></div>' +
        '<label>Was baust du gerade? (optional)</label><textarea name="projekt" rows="3"></textarea>' +
        '<label class="consent"><input type="checkbox" name="einwilligung" value="ja" required><span>Ich bin einverstanden, dass meine Angaben per E-Mail an Jean Maurice Port übermittelt werden, um meine Anfrage zu beantworten. Details in der <a href="datenschutz.html">Datenschutzerklärung</a>.</span></label>' +
        '<button class="btn" type="submit">' + icon("mail") + 'Setup per Mail bekommen</button>' +
        '<p class="hint">Oder direkt: <a href="mailto:' + F.to + '?subject=Stack-Check">' + F.to + '</a></p></form>' +
        '<p style="margin-top:14px"><button type="button" class="btn btn-sm restart">' + icon("arrow") + 'Noch mal von vorn</button></p>';
      qEl.classList.add("hidden"); optsEl.classList.add("hidden"); res.classList.remove("hidden");
      dots.innerHTML = F.questions.map(function () { return '<i class="on"></i>'; }).join(""); stepLbl.textContent = "Fertig"; back.classList.add("hidden");
      $(".restart", res).addEventListener("click", function () { ans = {}; stepIdx = 0; render(); });
    }
    back.addEventListener("click", function () { if (stepIdx > 0) { stepIdx--; render(); } });
    render();
  }
})();
