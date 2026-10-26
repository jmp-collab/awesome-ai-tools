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
  var panelMode = !!$("#searchpanel"); // Startseite: Suche über tools.json statt Filter auf der Seite
  function uniq(list) { var u = {}; list.forEach(function (li) { u[li.querySelector("a.name").href] = 1; }); return Object.keys(u).length; }
  function run() {
    if (panelMode) { var tot = $(".hero .stat b[data-count]"); if (count && tot) count.textContent = tot.dataset.count + " Tools"; return; }
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
  var sf = $("#searchform"); if (sf) sf.addEventListener("submit", function (e) { e.preventDefault(); if (panelMode) { if (window.kwPanelRun) window.kwPanelRun(); } else run(); });
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
      if (bar && !barDone) {
        var show = p > 0.3;
        bar.classList.toggle("show", show); document.body.classList.toggle("has-bar", show);
        if (show) document.documentElement.style.setProperty("--barh", bar.offsetHeight + "px"); // reale Höhe, auf dem Handy höher
      }
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
  // Im HTML stehen die echten Zahlen (ohne JavaScript, für Crawler); die Animation zählt beim Einblenden ab 0 hoch
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
    function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
    function fav(url) { try { var h = new URL(url).hostname; return '<img loading="lazy" alt="" src="https://icons.duckduckgo.com/ip3/' + esc(h) + '.ico">'; } catch (e) { return ""; } }
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
        return '<a href="' + esc(t.u) + '" target="_blank" rel="noopener">' + fav(t.u) + '<span><b>' + esc(n) + (t.eu ? ' <span class="badge eu">EU</span>' : "") + '</b><small>' + esc(t.d) + '</small></span></a>';
      }).join("");
      var notes = [F.notes[ans.team], ans.daten === "eu" ? F.notes.eu : ""].filter(Boolean).map(function (n) { return '<p class="note">' + esc(n) + "</p>"; }).join("");
      var stackText = list.join(", ");
      res.innerHTML = '<p class="eyebrow">Dein Setup</p><h3 class="finder-q">' + list.length + ' Tools, die zu deinem Fall passen</h3>' +
        '<div class="result-tools">' + cards + "</div>" + notes +
        '<form class="form" action="https://formsubmit.co/' + esc(F.to) + '" method="POST" style="margin-top:18px;box-shadow:none;border:1px solid var(--line)">' +
        '<input type="hidden" name="_subject" value="Stack-Check (Finder) – KI-Werkstatt"><input type="hidden" name="_template" value="table"><input type="hidden" name="_captcha" value="false">' +
        '<input type="hidden" name="_next" value="' + esc(F.next) + '">' +
        '<input type="text" name="_honey" class="honey" tabindex="-1" autocomplete="off">' +
        '<input type="hidden" name="quelle" value="Stack-Finder"><input type="hidden" name="antworten" value="' + esc([ans.ziel, ans.daten, ans.team].join(" / ")) + '"><input type="hidden" name="vorschlag" value="' + esc(stackText) + '">' +
        '<p style="margin:0 0 4px;font:700 18px var(--font-d)">Soll Jean da noch mal drüberschauen?</p><p style="margin:0;color:#5B616B;font-size:14px">Du bekommst das Setup mit Anmerkungen zu deinem Fall per Mail. Kostenlos, ohne Pitch.</p>' +
        '<div class="row"><div><label for="f-name">Name</label><input id="f-name" name="name" required autocomplete="name"></div><div><label for="f-mail">E-Mail</label><input id="f-mail" type="email" name="email" required autocomplete="email"></div></div>' +
        '<label for="f-proj">Was baust du gerade? (optional)</label><textarea id="f-proj" name="projekt" rows="3"></textarea>' +
        '<label class="consent"><input type="checkbox" name="einwilligung" value="ja" required><span>Ich bin einverstanden, dass meine Angaben per E-Mail an Jean Maurice Port übermittelt werden, um meine Anfrage zu beantworten. Details in der <a href="datenschutz.html">Datenschutzerklärung</a>.</span></label>' +
        '<button class="btn" type="submit">' + icon("mail") + 'Setup per Mail bekommen</button>' +
        '<p class="hint">Oder direkt: <a href="mailto:' + esc(F.to) + '?subject=Stack-Check">' + esc(F.to) + '</a></p></form>' +
        '<p style="margin-top:14px"><button type="button" class="btn btn-sm restart">' + icon("arrow") + 'Noch mal von vorn</button></p>';
      qEl.classList.add("hidden"); optsEl.classList.add("hidden"); res.classList.remove("hidden");
      dots.innerHTML = F.questions.map(function () { return '<i class="on"></i>'; }).join(""); stepLbl.textContent = "Fertig"; back.classList.add("hidden");
      $(".restart", res).addEventListener("click", function () { ans = {}; stepIdx = 0; render(); });
    }
    back.addEventListener("click", function () { if (stepIdx > 0) { stepIdx--; render(); } });
    render();
  }
  /* Gemeinsame Hilfen für Merkliste, Rechner und Formular-Anhänge */
  function escH(s) { return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function svg(id) { return '<svg class="ico" aria-hidden="true"><use href="#i-' + id + '"/></svg>'; }
  function attach(fieldId, text, label) {
    var f = document.getElementById(fieldId); if (!f) return false;
    f.value = text || "";
    var box = document.getElementById(fieldId === "l-merk" ? "l-attach-merk" : "l-attach-rechner");
    if (box) { $("span", box).textContent = label || ""; box.classList.toggle("hidden", !text); }
    return true;
  }
  $$(".attach button[data-clear]").forEach(function (b) {
    b.addEventListener("click", function () { attach(b.dataset.clear, "", ""); if (b.dataset.clear === "l-merk") store.set("kw-merk-attach", "0"); });
  });
  function goLead(prefill) {
    var ta = $("#l-proj");
    if (ta && prefill && !ta.value.trim()) ta.value = prefill;
    var target = $("#stack-check"); if (!target) return;
    target.scrollIntoView({ behavior: reduce ? "auto" : "smooth" });
    var nm = $("#l-name"); if (nm) setTimeout(function () { nm.focus({ preventScroll: true }); }, reduce ? 0 : 700);
  }
  var leadForm = $("#l-merk") ? $("#l-merk").form : null;
  if (leadForm) leadForm.addEventListener("submit", function () { store.set("kw-merk-attach", "0"); });

  /* Merkliste: Lesezeichen an jedem Tool, Liste bleibt im Browser */
  var MK = "kw-merk";
  function mLoad() {
    try { var v = JSON.parse(store.get(MK) || "[]"); return Array.isArray(v) ? v.filter(function (x) { return x && typeof x.n === "string" && typeof x.u === "string" && /^https?:/.test(x.u); }).slice(0, 60) : []; }
    catch (e) { return []; }
  }
  var merk = mLoad();
  function mSave() { store.set(MK, JSON.stringify(merk)); }
  function mHas(u) { return merk.some(function (x) { return x.u === u; }); }
  function mText() { return merk.map(function (x) { return x.n + " (" + x.u + ")"; }).join("\n"); }
  function mLabel() { return merk.length + (merk.length === 1 ? " Tool" : " Tools") + " aus deiner Merkliste angehängt"; }
  var pill = $("#merk-pill"), panel = $("#merk"), mList = panel ? $(".merk-list", panel) : null;
  function addMerkBtn(li) {
    var a = li.querySelector("a.name"); if (!a || li.querySelector(".merk-btn")) return;
    var b = document.createElement("button");
    b.type = "button"; b.className = "merk-btn"; b.innerHTML = svg("bookmark");
    b.dataset.u = a.href; b.dataset.n = a.textContent;
    b.addEventListener("click", function () {
      if (mHas(a.href)) merk = merk.filter(function (x) { return x.u !== a.href; }); else merk.push({ n: a.textContent, u: a.href });
      mSave(); mRender();
      if (pill && merk.length) { pill.classList.remove("pop"); void pill.offsetWidth; pill.classList.add("pop"); }
    });
    li.appendChild(b);
  }
  $$("ul.tools li").forEach(addMerkBtn);
  window.kwAddMerk = function (root) { $$("li", root).forEach(addMerkBtn); mRender(); };
  function mRender() {
    $$(".merk-btn").forEach(function (b) {
      var on = mHas(b.dataset.u);
      b.classList.toggle("on", on); b.setAttribute("aria-pressed", on ? "true" : "false");
      b.setAttribute("aria-label", (on ? "Von der Merkliste nehmen: " : "Merken: ") + b.dataset.n); b.title = on ? "Gemerkt" : "Merken";
    });
    if (pill) { pill.classList.toggle("hidden", !merk.length); $("#merk-n").textContent = merk.length; }
    if (mList) {
      mList.innerHTML = merk.map(function (x, i) {
        return '<li><a href="' + escH(x.u) + '" target="_blank" rel="noopener">' + escH(x.n) + '</a><button type="button" data-i="' + i + '" aria-label="Entfernen: ' + escH(x.n) + '">' + svg("x") + "</button></li>";
      }).join("");
      $(".merk-empty", panel).classList.toggle("hidden", merk.length > 0);
      $(".merk-actions", panel).classList.toggle("hidden", !merk.length);
    }
    var f = $("#l-merk"); if (f && f.value) attach("l-merk", merk.length ? mText() : "", mLabel());
  }
  function mOpen(open) {
    if (!panel) return;
    panel.hidden = !open; if (pill) pill.setAttribute("aria-expanded", open ? "true" : "false");
    if (open) { var c = $(".close", panel); if (c) c.focus(); }
  }
  if (pill && panel) {
    pill.addEventListener("click", function () { mOpen(panel.hidden); });
    $(".close", panel).addEventListener("click", function () { mOpen(false); pill.focus(); });
    mList.addEventListener("click", function (e) {
      var b = e.target.closest("button[data-i]"); if (!b) return;
      merk.splice(parseInt(b.dataset.i, 10), 1); mSave(); mRender(); if (!merk.length) { mOpen(false); }
    });
    $("#merk-clear").addEventListener("click", function () { merk = []; mSave(); mRender(); mOpen(false); });
    $("#merk-copy").addEventListener("click", function (e) {
      var btn = e.currentTarget, txt = btn.lastChild;
      function done(t) { txt.textContent = t; setTimeout(function () { txt.textContent = "Kopieren"; }, 1600); }
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(mText()).then(function () { done("Kopiert"); }, function () { done("Nicht möglich"); });
      else done("Nicht möglich");
    });
    $("#merk-send").addEventListener("click", function () {
      store.set("kw-merk-attach", "1");
      if ($("#l-merk")) { attach("l-merk", mText(), mLabel()); mOpen(false); goLead("Meine Merkliste: " + merk.map(function (x) { return x.n; }).join(", ") + ". "); }
      else location.href = "./#stack-check";
    });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !panel.hidden) { mOpen(false); pill.focus(); } });
  }
  // Auf einer anderen Seite zum Senden vorgemerkt: hier ans Formular hängen
  if (store.get("kw-merk-attach") === "1" && merk.length && $("#l-merk")) attach("l-merk", mText(), mLabel());
  mRender();

  /* Zeitspar-Rechner */
  var calc = $("#calc");
  if (calc) {
    var wochen = parseFloat(calc.dataset.wochen) || 46, rate = $("#c-rate"), cRows = $$(".calc-row", calc), summary = "";
    var nf1 = new Intl.NumberFormat("de-DE", { maximumFractionDigits: 1 }), nf0 = new Intl.NumberFormat("de-DE", { maximumFractionDigits: 0 });
    function num(el, max) { var v = parseFloat(String(el.value).replace(",", ".")); return isFinite(v) && v > 0 ? Math.min(v, max) : 0; }
    function calcRun() {
      var total = 0, saved = 0, top = 0, parts = [];
      var vals = cRows.map(function (r) {
        var h = num($(".c-h", r), 60), pc = num($(".c-p", r), 100), sv = h * pc / 100;
        total += h; saved += sv; if (sv > top) top = sv;
        return { r: r, h: h, pc: pc, sv: sv };
      });
      vals.forEach(function (v) {
        $("output", v.r).textContent = v.pc + " %";
        $(".calc-bar i", v.r).style.width = (top ? v.sv / top * 100 : 0).toFixed(1) + "%";
        $(".calc-bar span", v.r).textContent = nf1.format(v.sv) + " h/Woche";
        if (v.h > 0) parts.push(v.r.dataset.label + ": " + nf1.format(v.h) + " h pro Woche, " + v.pc + " % Ersparnis");
      });
      var share = total ? saved / total * 100 : 0, year = saved * wochen, r = num(rate, 1000), eur = year * r;
      $("#c-share").textContent = nf0.format(share) + " %";
      $(".calc-ring .fg", calc).setAttribute("stroke-dasharray", share.toFixed(1) + " 100");
      $("#c-week").textContent = nf1.format(saved) + " h";
      $("#c-year").textContent = nf0.format(year) + " h";
      $("#c-eur").textContent = nf0.format(eur) + " €";
      summary = parts.join("; ") + ". Ergebnis: " + nf1.format(saved) + " h pro Woche, " + nf0.format(year) + " h pro Jahr (" + wochen + " Wochen), Gegenwert " + nf0.format(eur) + " € bei " + nf0.format(r) + " € pro Stunde.";
      var f = $("#l-rechner"); if (f && f.value) attach("l-rechner", summary, "Rechner-Ergebnis angehängt: " + nf1.format(saved) + " h pro Woche");
    }
    calc.addEventListener("input", calcRun); calcRun();
    $("#c-send").addEventListener("click", function () {
      var week = $("#c-week").textContent;
      if (attach("l-rechner", summary, "Rechner-Ergebnis angehängt: " + week + " pro Woche")) goLead("Laut Zeitspar-Rechner könnte ich rund " + week + " pro Woche sparen. ");
    });
  }

  /* KI-Glossar: Filter, aktiver Buchstabe, Sprungziel hervorheben */
  var gq = $("#gq");
  if (gq) {
    var terms = $$(".term"), heads = $$(".az-letter"), gcount = $("#gcount"), gEmpty = $(".gl-empty");
    function gRun() {
      var s = gq.value.trim().toLowerCase(), shown = 0;
      terms.forEach(function (t) { var ok = !s || t.dataset.search.indexOf(s) > -1; t.classList.toggle("hidden", !ok); if (ok) shown++; });
      heads.forEach(function (h) {
        var n = h.nextElementSibling, any = false;
        while (n && !n.classList.contains("az-letter")) { if (n.classList.contains("term") && !n.classList.contains("hidden")) any = true; n = n.nextElementSibling; }
        h.classList.toggle("hidden", !any);
      });
      if (gcount) gcount.textContent = s ? shown + " von " + terms.length : terms.length + " Begriffe";
      if (gEmpty) gEmpty.classList.toggle("hidden", shown > 0);
    }
    gq.addEventListener("input", gRun); gRun();
    var azLinks = $$(".az-letters a");
    if ("IntersectionObserver" in window) {
      var io4 = new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) { var id = e.target.id; azLinks.forEach(function (a) { a.classList.toggle("on", a.getAttribute("href") === "#" + id); }); } });
      }, { rootMargin: "-15% 0px -75% 0px" });
      heads.forEach(function (h) { io4.observe(h); });
    }
    function flash() {
      var id = location.hash ? decodeURIComponent(location.hash.slice(1)) : "", t = id && document.getElementById(id);
      if (t && t.classList.contains("term")) { t.classList.add("in", "flash"); setTimeout(function () { t.classList.remove("flash"); }, 1800); return t; }
    }
    window.addEventListener("hashchange", flash);
    // Beim Laden mit #begriff: nach dem Aufbau der Seite sicher hinspringen
    var t0 = flash(); if (t0) window.addEventListener("load", function () { t0.scrollIntoView({ block: "start", behavior: "instant" }); });
  }
  /* Startseite: Suche über alle Tools (tools.json), Treffer mit Link in die passende Schublade */
  var sp = $("#searchpanel");
  if (sp && q) {
    var DATA = null, loading = null, spGen = 0, spHits = [], spShown = 0, SP_STEP = 40, spList = $(".sp-list", sp), spCount = $("#sp-count"), spEmpty = $(".sp-empty", sp), spEu = $("#sp-eu"), spOss = $("#sp-oss");
    function spLoad() {
      if (DATA) return Promise.resolve(DATA);
      if (!loading) loading = fetch("tools.json").then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); }).then(function (j) {
        DATA = j.tools.map(function (t) { t._s = [t.name, t.beschreibung, t.kategorie, t.bereich].join(" ").toLowerCase(); return t; });
        return DATA;
      });
      return loading;
    }
    function favI(url) { try { return '<img loading="lazy" alt="" width="28" height="28" src="https://icons.duckduckgo.com/ip3/' + escH(new URL(url).hostname) + '.ico">'; } catch (e) { return ""; } }
    function spHide() { spGen++; sp.hidden = true; } // spätere Antworten einer alten Suche verwerfen
    function spRun(keepOpen) {
      var s = q.value.trim().toLowerCase(), my = ++spGen, filt = spEu.checked || spOss.checked;
      if (!s && !filt) { // ohne Suchwort reicht ein gesetzter Filter
        if (keepOpen === true && !sp.hidden) { spCount.textContent = "Tipp ein Suchwort oder wähl einen Filter."; spList.innerHTML = ""; spEmpty.classList.add("hidden"); }
        else sp.hidden = true;
        return;
      }
      spLoad().then(function (rows) {
        if (my !== spGen) return;
        var words = s ? s.split(/\s+/) : [];
        var hits = rows.filter(function (t) { return words.every(function (w) { return t._s.indexOf(w) > -1; }) && (!spEu.checked || t.eu) && (!spOss.checked || t.open_source); });
        if (s) hits.sort(function (a, b) { return (b.name.toLowerCase().indexOf(s) === 0) - (a.name.toLowerCase().indexOf(s) === 0); });
        spCount.textContent = hits.length + " von " + rows.length + " Tools";
        spHits = hits; spShown = 0; spList.innerHTML = "";
        spMore();
        spEmpty.classList.toggle("hidden", hits.length > 0);
        sp.hidden = false;
      }).catch(function () { if (my !== spGen) return; spCount.textContent = "Die Suche klemmt gerade. Lade die Seite neu."; spList.innerHTML = ""; sp.hidden = false; });
    }
    function spRow(t) {
      var badges = (t.eu ? '<span class="badge eu">EU</span>' : "") + (t.open_source ? '<span class="badge oss">OSS</span>' : "");
      return '<li>' + favI(t.url) + '<div><a class="name" href="' + escH(t.url) + '" target="_blank" rel="noopener">' + escH(t.name) + "</a> " + badges +
        '<span class="desc">' + escH(t.beschreibung) + '</span><a class="sp-cat" href="' + escH(t.seite) + '">' + svg("layers") + escH(t.kategorie) + (t.bereich ? " · " + escH(t.bereich) : "") + "</a></div></li>";
    }
    // Treffer in Portionen anhängen; der Knopf am Ende holt die nächsten, bis alle sichtbar sind
    function spMore() {
      var old = $(".sp-more", spList); if (old) old.remove();
      var next = spHits.slice(spShown, spShown + SP_STEP); spShown += next.length;
      spList.insertAdjacentHTML("beforeend", next.map(spRow).join(""));
      var rest = spHits.length - spShown;
      if (rest > 0) spList.insertAdjacentHTML("beforeend", '<li class="sp-more"><button type="button" class="btn btn-sm">' + svg("layers") + "Noch " + Math.min(rest, SP_STEP) + " von " + rest + " weiteren zeigen</button></li>");
      spList.querySelectorAll("img:not([data-e])").forEach(function (im) { im.dataset.e = "1"; im.addEventListener("error", function () { im.style.visibility = "hidden"; }); });
      if (window.kwAddMerk) window.kwAddMerk(spList);
    }
    // stopPropagation: der Knopf verschwindet beim Nachladen, sonst hielte der Außen-Klick-Handler ihn für "außerhalb"
    spList.addEventListener("click", function (e) { if (e.target.closest(".sp-more button")) { e.stopPropagation(); spMore(); } });
    // Sprunglinks auf diese Seite (z. B. zum Stack-Check) schließen das Panel, damit es das Ziel nicht verdeckt
    sp.addEventListener("click", function (e) {
      var a = e.target.closest("a[href]"); if (!a) return;
      var u = new URL(a.href, location.href);
      if (u.origin === location.origin && u.pathname === location.pathname && u.hash) spHide();
    });
    window.kwPanelRun = spRun;
    var spT; q.addEventListener("input", function () { clearTimeout(spT); spT = setTimeout(spRun, 120); });
    q.addEventListener("focus", function () { if (q.value.trim()) spRun(); });
    [spEu, spOss].forEach(function (c) { c.addEventListener("change", function () { spRun(true); }); });
    $$("[data-sp]").forEach(function (b) {
      b.addEventListener("click", function (e) {
        e.stopPropagation(); // sonst schließt der Klick-außerhalb-Handler das Panel sofort wieder
        q.value = ""; // "Alle …" heißt alle, nicht die Schnittmenge mit einem alten Suchwort
        spEu.checked = b.dataset.sp === "eu"; spOss.checked = b.dataset.sp === "oss"; spRun();
      });
    });
    $(".close", sp).addEventListener("click", function () { spHide(); q.focus(); });
    // Escape verwirft auch eine Suche, deren Antwort noch unterwegs ist
    document.addEventListener("keydown", function (e) { if (e.key !== "Escape") return; var open = !sp.hidden; spHide(); if (open) q.focus(); });
    document.addEventListener("click", function (e) { if (!sp.contains(e.target) && e.target !== q) spHide(); });
  }
  /* Formulare: im Hintergrund an FormSubmit senden, mit Status und Mail-Ausweg, falls der Dienst hängt.
     Ohne JavaScript bleibt der normale POST an FormSubmit. */
  var FS_TIMEOUT = 15000;
  function fsData(form) {
    var fd = new FormData(form), lines = [], subject = "Anfrage – KI-Werkstatt";
    fd.forEach(function (v, k) {
      if (k === "_subject") subject = String(v);
      if (k.charAt(0) === "_" || k === "einwilligung" || !String(v).trim()) return;
      lines.push(k + ": " + v);
    });
    return { fd: fd, subject: subject, text: lines.join("\n") };
  }
  function fsStatus(form) {
    var st = form.querySelector(".form-status");
    if (!st) {
      st = document.createElement("div"); st.className = "form-status"; st.setAttribute("role", "status"); st.setAttribute("aria-live", "polite");
      var btn = form.querySelector("button[type=submit]");
      if (btn) btn.insertAdjacentElement("afterend", st); else form.appendChild(st);
    }
    return st;
  }
  function fsMailto(form, data) {
    var to = decodeURIComponent((form.action.split("formsubmit.co/")[1] || "").replace(/^ajax\//, ""));
    return "mailto:" + to + "?subject=" + encodeURIComponent(data.subject) + "&body=" + encodeURIComponent(data.text.slice(0, 1800));
  }
  document.addEventListener("submit", function (e) {
    var form = e.target;
    if (!form || !form.action || form.action.indexOf("https://formsubmit.co/") !== 0 || !window.fetch || !window.FormData) return;
    e.preventDefault();
    if (form.dataset.busy === "1") return;
    var data = fsData(form), st = fsStatus(form), btn = form.querySelector("button[type=submit]");
    var honey = form.querySelector("[name=_honey]");
    if (honey && honey.value) { st.className = "form-status ok"; st.textContent = "Danke."; return; } // Bot: still verwerfen
    var next = (form.querySelector("[name=_next]") || {}).value || "danke.html", mail = fsMailto(form, data), done = false;
    function fallback(msg) {
      if (done) return; done = true;
      form.dataset.busy = "0"; if (btn) btn.disabled = false;
      st.className = "form-status warn";
      st.innerHTML = "<p>" + escH(msg) + '</p><a class="mailbtn" href="' + escH(mail) + '">' + svg("mail") + "Anfrage per E-Mail-Programm senden</a>" +
        "<small>Deine Angaben stehen schon drin, du musst nur noch auf Senden drücken. Oder schreib direkt an " + escH(mail.slice(7, mail.indexOf("?"))) + ".</small>";
      var mb = st.querySelector(".mailbtn"); if (mb) mb.focus();
    }
    form.dataset.busy = "1"; if (btn) btn.disabled = true;
    st.className = "form-status busy"; st.textContent = "Wird gesendet … Kurbel trägt den Zettel rüber.";
    var ctrl = window.AbortController ? new AbortController() : null;
    var tmr = setTimeout(function () { if (ctrl) ctrl.abort(); fallback("Der Formulardienst braucht gerade ungewöhnlich lange. Per Mail geht es sofort."); }, FS_TIMEOUT);
    fetch(form.action.replace("https://formsubmit.co/", "https://formsubmit.co/ajax/"), { method: "POST", body: data.fd, headers: { Accept: "application/json" }, signal: ctrl ? ctrl.signal : undefined })
      .then(function (r) {
        return r.json().catch(function () { return { success: "false", message: "HTTP " + r.status }; }).then(function (j) { j._ok = r.ok; return j; });
      })
      .then(function (j) {
        clearTimeout(tmr); if (done) return;
        if (j._ok && (j.success === true || j.success === "true")) {
          done = true; st.className = "form-status ok"; st.textContent = "Angekommen. Du wirst gleich weitergeleitet."; location.href = next; return;
        }
        if (/activat/i.test(String(j.message || ""))) return fallback("Das Formular ist noch nicht freigeschaltet: FormSubmit hat dafür eine Bestätigungsmail an Jean geschickt. Bis dahin klappt der Weg per Mail.");
        fallback("Der Formulardienst hat die Anfrage gerade nicht angenommen. Per Mail geht es sofort.");
      })
      .catch(function () { clearTimeout(tmr); fallback("Der Formulardienst antwortet gerade nicht. Kein Drama: Per Mail geht es sofort."); });
  }, true);
})();
