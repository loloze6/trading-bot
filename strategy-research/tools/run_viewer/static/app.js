/* run viewer: router + views 1-3. Vanilla JS, no build. All data goes in through
   textContent / text nodes (never innerHTML). Relative URLs to this server only.
   Exposes window.RV = { api, el, setBreadcrumb, setToolbar, navigate } for view 4. */
(function () {
  "use strict";

  // ------------------------------------------------------------------ DOM helpers
  function append(parent, child) {
    if (child === null || child === undefined || child === false) return;
    if (Array.isArray(child)) { child.forEach(function (c) { append(parent, c); }); return; }
    if (child instanceof Node) { parent.appendChild(child); return; }
    parent.appendChild(document.createTextNode(String(child)));
  }

  function el(tag, attrs) {
    var n = document.createElement(tag);
    var children = Array.prototype.slice.call(arguments, 2);
    var isAttrs = attrs && typeof attrs === "object" && !(attrs instanceof Node) && !Array.isArray(attrs);
    if (isAttrs) {
      Object.keys(attrs).forEach(function (k) {
        var v = attrs[k];
        if (v === null || v === undefined || v === false) return;
        if (k === "class") n.className = v;
        else if (k === "text") n.textContent = String(v);
        else if (k.slice(0, 2) === "on" && typeof v === "function") n.addEventListener(k.slice(2), v);
        else n.setAttribute(k, v === true ? "" : String(v));
      });
    } else if (attrs !== null && attrs !== undefined) {
      children.unshift(attrs);
    }
    append(n, children);
    return n;
  }

  function clear(node) { while (node.firstChild) node.removeChild(node.firstChild); }

  // ------------------------------------------------------------------ value helpers
  function isNil(v) { return v === null || v === undefined; }
  function arr(v) { return Array.isArray(v) ? v : []; }
  function obj(v) { return v && typeof v === "object" && !Array.isArray(v) ? v : {}; }

  function fmtNum(v) {
    if (Number.isInteger(v)) return String(v);
    if (!isFinite(v)) return String(v);
    return String(Number(v.toPrecision(6)));
  }

  // text for a value inside a table cell / list (null shows a dash)
  function cellText(v) {
    if (isNil(v)) return "-";
    if (typeof v === "number") return fmtNum(v);
    if (typeof v === "boolean") return v ? "true" : "false";
    if (typeof v === "string") return v === "" ? "-" : v;
    try { return JSON.stringify(v); } catch (e) { return "unreadable (value)"; }
  }

  // text for a labelled header field (null shows "absent")
  function fieldText(v) {
    if (isNil(v) || v === "") return "absent";
    return cellText(v);
  }

  function resClass(s) {
    if (typeof s !== "string") return "";
    if (/(^|[\s=\/])PASS$/.test(s)) return "res-pass";
    if (/(^|[\s=\/])FAIL$/.test(s)) return "res-fail";
    if (/(^|[\s=\/])INCONCLUSIVE$/.test(s)) return "res-warn";
    return "";
  }

  // value node: " | " joined k=v strings become one part per line; PASS/FAIL coloured
  function valueNode(v) {
    var s = cellText(v);
    if (typeof v === "string" && s.indexOf(" | ") > -1 && s.indexOf("=") > -1) {
      var box = el("div", { class: "pre" });
      s.split(" | ").forEach(function (part) {
        box.appendChild(el("div", { class: resClass(part), text: part }));
      });
      return box;
    }
    return el("span", { class: "pre " + resClass(s), text: s });
  }

  function fmtDate(s) {
    if (isNil(s)) return "absent";
    if (typeof s !== "string") return cellText(s);
    var m = /^(\d{4}-\d\d-\d\d)[T ](\d\d:\d\d)(?::\d\d(?:\.\d+)?)?(Z|\+00:00)$/.exec(s);
    if (m) return m[1] + " " + m[2] + " UTC";
    return s;
  }

  function fmtDur(sec) {
    if (typeof sec !== "number" || !isFinite(sec)) return "absent";
    var s = Math.round(sec);
    if (s < 60) return s + "s";
    var m = Math.floor(s / 60);
    if (m < 60) return m + "m " + (s % 60) + "s";
    var h = Math.floor(m / 60);
    if (h < 48) return h + "h " + (m % 60) + "m";
    return Math.floor(h / 24) + "d " + (h % 24) + "h";
  }

  function fmtCost(c) {
    if (typeof c !== "number" || !isFinite(c)) return "absent";
    return "$" + c.toFixed(2);
  }

  function enc(s) { return encodeURIComponent(String(s)); }
  function hRun(id) { return "#/run/" + enc(id); }
  function hStep(id, name) { return hRun(id) + "/step/" + enc(name); }
  function hWin(id, v, w) { return hRun(id) + "/variant/" + enc(v) + "/window/" + enc(w); }

  // status -> css kind + label
  function stKind(s) {
    if (s === "ok" || s === "fail" || s === "warn" || s === "absent" || s === "unreadable") return s;
    return "absent";
  }
  function chip(label, kind) {
    return el("span", { class: "chip st-" + stKind(kind), text: String(label) });
  }
  function statusChip(s) {
    var k = stKind(s);
    var label = typeof s === "string" && s ? s.toUpperCase() : "ABSENT";
    if (k === "absent" && typeof s === "string" && s && s !== "absent") label = s.toUpperCase();
    return chip(label, k);
  }
  function ideaKind(s) {
    if (s === "validated") return "ok";
    if (s === "refuted") return "fail";
    if (s === "inconclusive") return "warn";
    return "absent";
  }

  function errorBox(title, detail) {
    return el("div", { class: "errorbox", role: "alert" },
      el("strong", { text: title }),
      detail ? el("div", { text: detail }) : null);
  }

  function toggleButton(labelOff, labelOn, target, onToggle) {
    var open = false;
    var b = el("button", { type: "button", class: "btn", "aria-expanded": "false" }, labelOff);
    b.addEventListener("click", function () {
      open = !open;
      b.setAttribute("aria-expanded", open ? "true" : "false");
      b.textContent = open ? labelOn : labelOff;
      if (target) target.classList.toggle("hidden", !open);
      if (onToggle) onToggle(open);
    });
    return b;
  }

  // ------------------------------------------------------------------ api
  var cache = {};   // winMap promises per run; cleared on reload

  function api(path) {
    return fetch(path, { cache: "no-store" }).then(function (res) {
      if (!res.ok) {
        return res.text().then(function (t) {
          var msg = "";
          try { msg = JSON.parse(t).error || ""; } catch (e) { msg = ""; }
          var err = new Error("HTTP " + res.status + (msg ? " - " + msg : "") + " (" + path + ")");
          err.status = res.status;
          throw err;
        });
      }
      return res.json().catch(function () {
        var err = new Error("response was not JSON (" + path + ")");
        err.status = res.status;
        throw err;
      });
    }, function (e) {
      var err = new Error("network error: " + (e && e.message ? e.message : "request failed") + " (" + path + ")");
      err.status = 0;
      throw err;
    });
  }

  // ------------------------------------------------------------------ chrome (top bar)
  var crumbsEl, toolbarEl, mainEl;

  function setBreadcrumb(items) {
    clear(crumbsEl);
    arr(items).forEach(function (it, i, all) {
      var last = i === all.length - 1;
      if (i > 0) crumbsEl.appendChild(el("span", { class: "sep", "aria-hidden": "true", text: ">" }));
      var label = it && !isNil(it.label) ? String(it.label) : "?";
      if (it && it.href && !last) crumbsEl.appendChild(el("a", { class: "crumb", href: it.href, text: label }));
      else if (it && it.href) crumbsEl.appendChild(el("a", { class: "crumb current", href: it.href, "aria-current": "page", text: label }));
      else crumbsEl.appendChild(el("span", { class: "crumb current", text: label }));
    });
    crumbsEl.scrollLeft = crumbsEl.scrollWidth;
  }

  function setToolbar(node) {
    clear(toolbarEl);
    if (node) { toolbarEl.appendChild(node); toolbarEl.hidden = false; }
    else toolbarEl.hidden = true;
  }

  function navigate(hash) {
    var h = String(hash || "#/");
    if (h.charAt(0) !== "#") h = "#" + h;
    if (location.hash === h) render();
    else location.hash = h;
  }

  // ------------------------------------------------------------------ responsive helpers
  // stacked cards for a table with > 2 columns (phone)
  function stackedCards(columns, rows, linkFor) {
    var box = el("div", { class: "cards" });
    rows.forEach(function (row, ri) {
      var r = arr(row);
      var titleNode = linkFor ? linkFor(ri, 0) : null;
      var head = titleNode || el("span", { text: cellText(r[0]) });
      var kv = el("div", { class: "kv" });
      for (var c = 1; c < columns.length; c++) {
        kv.appendChild(el("div", { class: "k", text: String(columns[c]) }));
        var linkNode = linkFor ? linkFor(ri, c) : null;
        kv.appendChild(el("div", { class: "v" }, linkNode || valueNode(r[c])));
      }
      box.appendChild(el("div", { class: "card st-absent" },
        el("div", { class: "card-head" }, el("span", { class: "card-title" }, head)),
        kv));
    });
    return box;
  }

  function wideTable(columns, rows, opts) {
    opts = opts || {};
    var thead = el("tr");
    columns.forEach(function (c, ci) {
      var hl = opts.headLink ? opts.headLink(ci) : null;
      thead.appendChild(el("th", { scope: "col" }, hl || String(c)));
    });
    var tbody = el("tbody");
    rows.forEach(function (row, ri) {
      var r = arr(row);
      var tr = el("tr");
      for (var c = 0; c < columns.length; c++) {
        var v = r[c];
        var linkNode = opts.linkFor ? opts.linkFor(ri, c) : null;
        var td = el("td", { class: typeof v === "number" ? "num" : "" });
        if (linkNode) td.appendChild(linkNode);
        else td.appendChild(el("span", { class: "cell " + resClass(cellText(v)), text: cellText(v) }));
        tr.appendChild(td);
      }
      if (opts.rowHref) {
        var href = opts.rowHref(ri);
        if (href) {
          tr.className = "click";
          tr.addEventListener("click", function (ev) {
            if (ev.target && ev.target.closest && ev.target.closest("a")) return;
            navigate(href);
          });
        }
      }
      tbody.appendChild(tr);
    });
    return el("div", { class: "scroll" }, el("table", { class: "t" }, el("thead", null, thead), tbody));
  }

  // ------------------------------------------------------------------ VIEW 1
  function runCard(r) {
    var idea = r.idea_status;
    var coins = Array.isArray(r.coins) ? r.coins.join(", ") : fieldText(r.coins);
    var bb = r.base_bars && typeof r.base_bars === "object" ? r.base_bars : null;
    var outcome = !isNil(r.outcome_letter) ? "outcome: " + r.outcome_letter : "outcome: " + (r.outcome_note || "not recorded");
    return el("a", { class: "card run-card st-" + ideaKind(idea), href: hRun(r.run_id) },
      el("div", { class: "card-head" },
        el("span", { class: "ids", text: String(r.run_id) }),
        el("span", null,
          r.legacy_shape ? el("span", { class: "tag", text: "legacy shape" }) : null,
          r.legacy_shape ? " " : null,
          chip(isNil(idea) ? "no idea_status" : String(idea), ideaKind(idea)))),
      el("div", { class: "meta" }, el("b", { text: "entry " }), fieldText(r.entry_id)),
      el("div", { class: "meta" },
        el("b", { text: "fold " }), fieldText(r.fold), "   ",
        el("b", { text: "coins x tf " }), coins + " x " + fieldText(r.timeframe)),
      el("div", { class: "meta" }, el("b", { text: "base bars " }), bb ? bb.passed + "/" + bb.total : "absent"),
      el("div", { class: "meta" }, el("b", { text: "cost " }), fmtCost(r.cost_usd), " (" + (r.cost_label || "") + ")"),
      el("div", { class: "meta" }, el("b", { text: "launched " }), fmtDate(r.launched_at),
        "   ", el("b", { text: "duration " }), fmtDur(r.duration_seconds)),
      el("div", { class: "meta", text: outcome }));
  }

  function runsTable(runs) {
    var cols = ["run", "idea_status", "entry", "fold", "coins x timeframe", "base bars", "cost", "launched", "duration", "outcome", "status / stage"];
    var rows = runs.map(function (r) {
      var bb = r.base_bars && typeof r.base_bars === "object" ? r.base_bars : null;
      var coins = Array.isArray(r.coins) ? r.coins.join(", ") : fieldText(r.coins);
      return [
        r.run_id + (r.legacy_shape ? "  (legacy shape)" : ""),
        isNil(r.idea_status) ? "absent" : r.idea_status,
        fieldText(r.entry_id), fieldText(r.fold),
        coins + " x " + fieldText(r.timeframe),
        bb ? bb.passed + "/" + bb.total : "absent",
        fmtCost(r.cost_usd) + " (" + (r.cost_label || "") + ")",
        fmtDate(r.launched_at), fmtDur(r.duration_seconds),
        !isNil(r.outcome_letter) ? "outcome: " + r.outcome_letter : "outcome: " + (r.outcome_note || "not recorded"),
        fieldText(r.status) + " / " + fieldText(r.pending_stage)
      ];
    });
    return wideTable(cols, rows, {
      linkFor: function (ri, ci) {
        if (ci !== 0) return null;
        return el("a", { href: hRun(runs[ri].run_id), text: rows[ri][0] });
      },
      rowHref: function (ri) { return hRun(runs[ri].run_id); }
    });
  }

  function cardsFromObjs(items, titleKey, fields, kindFor) {
    var box = el("div", { class: "cards" });
    items.forEach(function (it) {
      var o = obj(it);
      var kv = el("div", { class: "kv" });
      fields.forEach(function (f) {
        kv.appendChild(el("div", { class: "k", text: f.label }));
        kv.appendChild(el("div", { class: "v" }, f.node ? f.node(o) : valueNode(o[f.key])));
      });
      box.appendChild(el("div", { class: "card st-" + (kindFor ? kindFor(o) : "absent") },
        el("div", { class: "card-head" }, el("span", { class: "card-title", text: cellText(o[titleKey]) })),
        kv));
    });
    return box;
  }

  function notesNode(text) {
    var s = cellText(text);
    var p = el("div", { class: "pre clamp", text: s });
    var b = el("button", { type: "button", class: "btn", "aria-expanded": "false" }, "more");
    var open = false;
    b.addEventListener("click", function () {
      open = !open; p.classList.toggle("clamp", !open);
      b.textContent = open ? "less" : "more"; b.setAttribute("aria-expanded", open ? "true" : "false");
    });
    return el("div", null, p, s.length > 160 ? b : null);
  }

  function queueKind(status) {
    if (status === "ready" || status === "in_progress") return "ok";
    if (typeof status === "string" && status.indexOf("blocked") === 0) return "warn";
    return "absent";
  }

  function renderView1(data) {
    var d = obj(data);
    var runs = arr(d.runs);
    var frag = document.createDocumentFragment();
    frag.appendChild(el("h1", { text: "Campaign" }));

    var nLegacy = runs.filter(function (r) { return r && r.legacy_shape; }).length;
    var listHost = el("div");
    var hideLegacy = false;
    function paintRuns() {
      clear(listHost);
      var shown = runs.filter(function (r) { return r && !(hideLegacy && r.legacy_shape); });
      listHost.appendChild(el("div", { class: "cards narrow-only" }, shown.map(runCard)));
      listHost.appendChild(el("div", { class: "wide-only" }, runsTable(shown)));
      if (!shown.length) listHost.appendChild(el("p", { class: "muted", text: "No runs." }));
    }
    var legacyBtn = el("button", { type: "button", class: "btn", "aria-pressed": "false" },
      "Hide legacy-shape runs (" + nLegacy + ")");
    legacyBtn.addEventListener("click", function () {
      hideLegacy = !hideLegacy;
      legacyBtn.setAttribute("aria-pressed", hideLegacy ? "true" : "false");
      legacyBtn.textContent = hideLegacy ? "Show legacy-shape runs (" + nLegacy + ")" : "Hide legacy-shape runs (" + nLegacy + ")";
      paintRuns();
    });
    frag.appendChild(el("h2", { text: "Runs (newest first), " + runs.length }));
    if (nLegacy) frag.appendChild(el("div", { class: "row" }, legacyBtn));
    paintRuns();
    frag.appendChild(listHost);

    // queue
    var q = obj(d.queue);
    var entries = arr(q.entries);
    var counts = obj(q.counts);
    frag.appendChild(el("h2", { text: "Queue" }));
    var cc = el("div", { class: "chips" });
    var ck = Object.keys(counts);
    ck.forEach(function (k) { cc.appendChild(chip(k + ": " + counts[k], queueKind(k))); });
    if (!ck.length) cc.appendChild(el("span", { class: "muted", text: "no counts (queue absent or unreadable)" }));
    frag.appendChild(cc);
    if (entries.length) {
      frag.appendChild(el("p", { class: "note", text: "Entries listed here are the ones not done; done entries are only counted above." }));
      frag.appendChild(el("div", { class: "narrow-only" }, cardsFromObjs(entries, "id", [
        { label: "status", node: function (o) { return chip(cellText(o.status), queueKind(o.status)); } },
        { label: "priority", key: "priority" },
        { label: "notes", node: function (o) { return notesNode(o.notes); } },
        { label: "reason", key: "brief_status_reason" }
      ], function (o) { return queueKind(o.status); })));
      frag.appendChild(el("div", { class: "wide-only" }, wideTable(
        ["id", "status", "priority", "notes", "brief_status_reason"],
        entries.map(function (e) { e = obj(e); return [e.id, e.status, e.priority, e.notes, e.brief_status_reason]; }))));
    } else {
      frag.appendChild(el("p", { class: "muted", text: "No ready or blocked entries." }));
    }

    // blocks
    var b = obj(d.blocks);
    var blocks = arr(b.blocks);
    frag.appendChild(el("h2", { text: "Blocks (registry revision " + fieldText(b.revision) + "), " + blocks.length }));
    if (blocks.length) {
      var runIds = {};
      runs.forEach(function (r) { if (r && r.run_id) runIds[r.run_id] = true; });
      var runLink = function (o) {
        return runIds[o.validated_by_run]
          ? el("a", { href: hRun(o.validated_by_run), text: String(o.validated_by_run) })
          : valueNode(o.validated_by_run);
      };
      frag.appendChild(el("div", { class: "narrow-only" }, cardsFromObjs(blocks, "block_id", [
        { label: "status", node: function (o) { return chip(cellText(o.status), o.status === "active" ? "ok" : o.status === "voided" ? "warn" : "absent"); } },
        { label: "validated by run", node: runLink },
        { label: "kind", key: "kind" },
        { label: "hypothesis", key: "hypothesis_id" }
      ], function (o) { return o.status === "active" ? "ok" : o.status === "voided" ? "warn" : "absent"; })));
      frag.appendChild(el("div", { class: "wide-only" }, wideTable(
        ["block id", "validated by run", "status", "kind", "hypothesis"],
        blocks.map(function (x) { x = obj(x); return [x.block_id, x.validated_by_run, x.status, x.kind, x.hypothesis_id]; }),
        { linkFor: function (ri, ci) {
            if (ci !== 1) return null;
            var id = obj(blocks[ri]).validated_by_run;
            return runIds[id] ? el("a", { href: hRun(id), text: String(id) }) : null;
          } })));
    } else {
      frag.appendChild(el("p", { class: "muted", text: "No blocks recorded (registry absent or empty)." }));
    }
    frag.appendChild(sourcesBlock(d.sources));
    return frag;
  }

  // ------------------------------------------------------------------ sources
  function sourceState(s) {
    var o = obj(s);
    var st = o.state;
    var extra = o.reason || o.error;
    return { path: cellText(o.path), state: isNil(st) ? "absent" : String(st), extra: extra ? String(extra) : "" };
  }
  function sourcesBlock(sources) {
    var list = arr(sources);
    var d = el("details", { class: "sources" }, el("summary", { text: "Sources (" + list.length + ")" }));
    var ul = el("div", { class: "cards" });
    list.forEach(function (s) {
      var x = sourceState(s);
      var kind = x.state === "present" ? "ok" : x.state === "absent" ? "absent" : "unreadable";
      ul.appendChild(el("div", { class: "card st-" + kind },
        el("div", { class: "card-head" },
          el("span", { class: "mono", text: x.path }), chip(x.state, kind)),
        x.extra ? el("div", { class: "line", text: x.extra }) : null));
    });
    if (!list.length) ul.appendChild(el("p", { class: "muted", text: "No sources listed." }));
    d.appendChild(ul);
    return d;
  }

  // ------------------------------------------------------------------ VIEW 2
  function stepCard(runId, st) {
    var s = obj(st);
    var kind = stKind(s.status);
    var heads = el("ul", { class: "heads" });
    arr(s.headlines).forEach(function (h) {
      var o = obj(h);
      heads.appendChild(el("li", null, el("span", { class: "k", text: cellText(o.label) + ": " }),
        el("span", { text: fieldText(o.value) })));
    });
    return el("a", { class: "card step st-" + kind, href: hStep(runId, s.name) },
      el("div", { class: "card-head" },
        el("span", { class: "card-title", text: cellText(s.title || s.name) }),
        statusChip(s.status)),
      heads,
      el("div", { class: "line", text: fieldText(s.line) }));
  }

  function renderView2(runId, data) {
    var d = obj(data);
    var h = obj(d.header);
    var frag = document.createDocumentFragment();
    frag.appendChild(el("h1", { text: String(h.run_id || runId) }));
    frag.appendChild(el("p", { class: "meta" },
      el("b", { text: "entry " }), fieldText(h.entry_id), "   ",
      el("b", { text: "status " }), fieldText(h.status), "   ",
      el("b", { text: "stage " }), fieldText(h.pending_stage)));

    // PURPOSE
    frag.appendChild(el("h2", { text: "Purpose" }));
    var short = h.purpose, full = h.purpose_full;
    if (isNil(short) && isNil(full)) {
      frag.appendChild(el("p", { class: "muted", text: "absent (no brief for this run)" }));
    } else {
      var shortText = cellText(isNil(short) ? full : short);
      var fullText = cellText(isNil(full) ? short : full);
      var p = el("p", { class: "purpose pre clamp", text: shortText });
      var isOpen = false;
      var hasMore = fullText !== shortText || fullText.length > 220;
      var more = el("button", { type: "button", class: "btn", "aria-expanded": "false" }, "more");
      more.addEventListener("click", function () {
        isOpen = !isOpen;
        p.textContent = isOpen ? fullText : shortText;
        p.classList.toggle("clamp", !isOpen);
        more.textContent = isOpen ? "less" : "more";
        more.setAttribute("aria-expanded", isOpen ? "true" : "false");
      });
      frag.appendChild(p);
      if (hasMore) frag.appendChild(el("div", { class: "row" }, more));
    }

    // outcomes
    var outs = arr(h.outcomes);
    var outcomeLine = !isNil(h.outcome_letter) ? "outcome: " + h.outcome_letter : "outcome: " + (h.outcome_note || "not recorded");
    frag.appendChild(el("p", { class: "meta" }, el("b", { text: outcomeLine })));
    if (outs.length) {
      var ol = el("ul", { class: "outcomes hidden" });
      outs.forEach(function (o) {
        o = obj(o);
        ol.appendChild(el("li", null, el("span", { class: "letter", text: cellText(o.letter) }), el("span", { class: "pre", text: cellText(o.text) })));
      });
      frag.appendChild(el("div", { class: "row" }, toggleButton("show outcomes (" + outs.length + ")", "hide outcomes", ol)));
      frag.appendChild(ol);
    } else {
      frag.appendChild(el("p", { class: "muted", text: "Pre-registered outcomes: absent." }));
    }

    // cost
    frag.appendChild(el("p", { class: "meta" },
      el("b", { text: "cost " }), fmtCost(h.cost_usd), " - " + (h.cost_label || "model cost (stages that called a model)")));

    // audit
    var audit = arr(h.audit);
    frag.appendChild(el("h2", { text: "Audit (stages that called a model)" }));
    if (audit.length) {
      var acols = ["stage", "models", "cost", "turns", "tokens", "time"];
      var arows = audit.map(function (a) {
        a = obj(a);
        return [a.stage, Array.isArray(a.models) ? (a.models.join(", ") || "none") : a.models,
          fmtCost(a.cost_usd), a.num_turns, a.tokens_total,
          typeof a.execution_time_seconds === "number" ? fmtDur(a.execution_time_seconds) : null];
      });
      frag.appendChild(el("div", { class: "narrow-only" }, stackedCards(acols, arows)));
      frag.appendChild(el("div", { class: "wide-only" }, wideTable(acols, arows)));
    } else {
      frag.appendChild(el("p", { class: "muted", text: "No audit log." }));
    }

    // campaign log
    var logs = arr(h.campaign_log);
    if (logs.length) {
      var pre = el("pre", { class: "raw hidden", text: logs.join("\n") });
      frag.appendChild(el("div", { class: "row" }, toggleButton("show campaign log (" + logs.length + " lines)", "hide campaign log", pre)));
      frag.appendChild(pre);
    } else {
      frag.appendChild(el("p", { class: "muted", text: "Campaign log lines: absent." }));
    }

    // variants (names only)
    var vars = arr(h.variants);
    if (vars.length) frag.appendChild(el("p", { class: "meta" }, el("b", { text: "variants " }), vars.join(", ")));

    // steps
    frag.appendChild(el("h2", { text: "Steps" }));
    var steps = arr(d.steps);
    if (!steps.length) frag.appendChild(el("p", { class: "muted", text: "No steps." }));
    frag.appendChild(el("div", { class: "stepgrid" }, steps.map(function (s) { return stepCard(runId, s); })));
    frag.appendChild(sourcesBlock(d.sources));
    return frag;
  }

  // ------------------------------------------------------------------ VIEW 3
  function getWinMap(runId) {
    if (!cache[runId]) {
      cache[runId] = api("/api/run/" + enc(runId) + "/step/protocol").then(function (p) {
        var m = {};
        arr(obj(p).tables).forEach(function (t) {
          arr(obj(t).links).forEach(function (L) {
            L = obj(L);
            if (L.variant && L.window) {
              if (!m[L.variant]) m[L.variant] = [];
              if (m[L.variant].indexOf(L.window) < 0) m[L.variant].push(L.window);
            }
          });
        });
        return m;
      }).catch(function () { return null; });
    }
    return cache[runId];
  }

  function makeHref(runId, winMap, variant, win) {
    if (isNil(variant) || variant === "") return null;
    variant = String(variant);
    if (variant.indexOf("[sealed") === 0) return null;
    if (!isNil(win) && win !== "") {
      win = String(win);
      if (win.indexOf("[sealed") === 0) return null;
      if (winMap && !(winMap[variant] || []).includes(win)) return null;
      return hWin(runId, variant, win);
    }
    if (!winMap) return null;
    var ws = winMap[variant];
    return ws && ws.length ? hWin(runId, variant, ws[0]) : null;
  }

  var LINK_COLS = { variant: 1, variant_id: 1, trial_id: 1, window: 1 };
  function linkColumns(columns) {
    var set = {}, any = false;
    columns.forEach(function (c, i) { if (LINK_COLS[c]) { set[i] = true; any = true; } });
    if (!any && columns.length) set[0] = true;
    return set;
  }

  function sectionOf(x) { var s = obj(x).section; return typeof s === "string" && s ? s : ""; }
  function titleNoSection(title, section) {
    var t = cellText(title);
    if (section && t.indexOf(section + ": ") === 0) return t.slice(section.length + 2);
    return t;
  }

  function tableBlock(runId, winMap, tbl, section) {
    var t = obj(tbl);
    var columns = arr(t.columns).map(function (c) { return cellText(c); });
    var rows = arr(t.rows);
    var links = Array.isArray(t.links) ? t.links : null;
    var colLinks = Array.isArray(t.column_links) ? t.column_links : null;
    var lcols = linkColumns(columns);
    var hasWindowCol = columns.indexOf("window") > -1;
    var hasVariantCol = columns.indexOf("variant") > -1;

    var box = el("section", { class: "tblock" });
    box.appendChild(el("h2", { text: titleNoSection(t.title, section) }));
    if (!rows.length) {
      box.appendChild(el("p", { class: "muted", text: "No rows." }));
      return box;
    }

    function cellLink(ri, ci) {
      if (!links || !lcols[ci]) return null;
      var L = obj(links[ri]);
      if (isNil(L.variant)) return null;
      var href = makeHref(runId, winMap, L.variant, L.window);
      var v = arr(rows[ri])[ci];
      return href ? el("a", { class: "cell", href: href, text: cellText(v) }) : null;
    }
    function headLink(ci) {
      if (!colLinks) return null;
      var L = obj(colLinks[ci]);
      if (isNil(L.variant)) return null;
      var href = makeHref(runId, winMap, L.variant, L.window);
      return href ? el("a", { href: href, text: columns[ci] }) : null;
    }

    // ---- narrow
    var narrow = el("div", { class: "narrow-only" });
    var bo = t.by_option && typeof t.by_option === "object" ? t.by_option : null;
    var opts = bo ? arr(bo.options) : [];
    if (bo && opts.length) {
      var rbo = obj(bo.rows_by_option);
      var by = cellText(bo.by);
      var listHost = el("div");
      var openHost = el("div");
      var sel = el("select", { class: "sel", id: "sel-" + Math.random().toString(36).slice(2), "aria-label": by });
      opts.forEach(function (o) { sel.appendChild(el("option", { value: String(o), text: String(o) })); });
      var variantLike = by === "variant" || by === "variant_id";
      function trialVariant(o) {
        var m = /^(run_\d+):(.+)$/.exec(String(o));
        return m && m[1] === runId ? m[2] : null;
      }
      function paint() {
        var o = sel.value;
        clear(listHost); clear(openHost);
        var pairs = arr(rbo[o]);
        var optVariant = variantLike ? o : (by === "trial_id" ? trialVariant(o) : null);
        var kv = el("div", { class: "kv" });
        pairs.forEach(function (pr) {
          var pa = arr(pr);
          var label = cellText(pa[0]);
          var labNode = el("span", { text: label });
          if (optVariant && hasWindowCol) {
            var hw = makeHref(runId, winMap, optVariant, label);
            if (hw) labNode = el("a", { href: hw, text: label });
          } else if (by === "window" && hasVariantCol) {
            var hv = makeHref(runId, winMap, label, o);
            if (hv) labNode = el("a", { href: hv, text: label });
          }
          kv.appendChild(el("div", { class: "k" }, labNode));
          kv.appendChild(el("div", { class: "v" }, valueNode(pa[1])));
        });
        if (!pairs.length) listHost.appendChild(el("p", { class: "muted", text: "No rows for this option." }));
        else listHost.appendChild(kv);
        if (optVariant) {
          var oh = makeHref(runId, winMap, optVariant, null);
          if (oh) openHost.appendChild(el("a", { class: "btn", href: oh, style: "display:inline-flex;align-items:center;text-decoration:none", text: "Open " + optVariant + " chart" }));
        }
      }
      sel.addEventListener("change", paint);
      narrow.appendChild(el("div", { class: "row" }, el("label", { class: "field", for: sel.id }, by, sel), openHost));
      narrow.appendChild(listHost);
      paint();
    } else if (columns.length > 2) {
      narrow.appendChild(stackedCards(columns, rows, links ? cellLink : null));
    } else {
      narrow.appendChild(wideTable(columns, rows, { linkFor: cellLink }));
    }
    box.appendChild(narrow);

    // ---- wide
    box.appendChild(el("div", { class: "wide-only" }, wideTable(columns, rows, { linkFor: cellLink, headLink: headLink })));
    return box;
  }

  function textBlock(tx, section) {
    var o = obj(tx);
    var body = cellText(o.body);
    var long = body.length > 1500;
    var pre = el("pre", { class: "textblock plain" + (long ? " long" : ""), text: body });
    var wrap = el("div", { class: "txt" }, el("h3", { text: titleNoSection(o.title, section) }), pre);
    if (long) {
      var open = false;
      var b = el("button", { type: "button", class: "btn", "aria-expanded": "false" }, "show all (" + body.length + " chars)");
      b.addEventListener("click", function () {
        open = !open; pre.classList.toggle("long", !open);
        b.textContent = open ? "collapse" : "show all (" + body.length + " chars)";
        b.setAttribute("aria-expanded", open ? "true" : "false");
      });
      wrap.appendChild(el("div", { class: "row" }, b));
    }
    return wrap;
  }

  function rawBlock(r) {
    var o = obj(r);
    var path = cellText(o.path);
    var pre = el("pre", { class: "raw hidden", text: isNil(o.text) ? "absent" : String(o.text) });
    var note = o.truncated ? el("p", { class: "note", text: "truncated: this file is longer than the viewer's cap; only the start is shown." }) : null;
    var wrap = el("div", { class: "rawfile" });
    var b = el("button", { type: "button", class: "btn", "aria-expanded": "false" }, "Raw file");
    b.addEventListener("click", function () {
      var open = pre.classList.contains("hidden");
      pre.classList.toggle("hidden", !open);
      if (note) note.classList.toggle("hidden", !open);
      b.setAttribute("aria-expanded", open ? "true" : "false");
      b.textContent = open ? "Hide raw file" : "Raw file";
    });
    if (note) note.classList.add("hidden");
    wrap.appendChild(el("div", { class: "row" }, b, el("span", { class: "mono note", text: path })));
    if (note) wrap.appendChild(note);
    wrap.appendChild(pre);
    return wrap;
  }

  function safe(fn, label) {
    try { return fn(); }
    catch (e) { return el("p", { class: "muted", text: "unreadable (" + label + ": " + (e && e.message ? e.message : "render error") + ")" }); }
  }

  function renderView3(runId, name, data, winMap) {
    var s = obj(data);
    var frag = document.createDocumentFragment();
    var kind = stKind(s.status);
    var heads = el("ul", { class: "heads" });
    arr(s.headlines).forEach(function (h) {
      var o = obj(h);
      heads.appendChild(el("li", null, el("span", { class: "k", text: cellText(o.label) + ": " }), el("span", { text: fieldText(o.value) })));
    });
    frag.appendChild(el("div", { class: "card summary st-" + kind },
      el("div", { class: "card-head" },
        el("h1", { text: cellText(s.title || name), style: "margin:0" }), statusChip(s.status)),
      heads,
      el("div", { class: "line", text: fieldText(s.line) })));

    var tables = arr(s.tables), texts = arr(s.text);
    var mainTables = tables.filter(function (t) { return !sectionOf(t); });
    var mainTexts = texts.filter(function (t) { return !sectionOf(t); });
    mainTables.forEach(function (t) { frag.appendChild(safe(function () { return tableBlock(runId, winMap, t, ""); }, "table")); });
    if (mainTexts.length) mainTexts.forEach(function (t) { frag.appendChild(safe(function () { return textBlock(t, ""); }, "text")); });

    // sections ("re-run on a copy"), after the main content, in order of first appearance
    var order = [];
    tables.concat(texts).forEach(function (x) { var sec = sectionOf(x); if (sec && order.indexOf(sec) < 0) order.push(sec); });
    order.forEach(function (sec) {
      frag.appendChild(el("h2", { class: "section-head", text: sec, style: "margin-top:2rem;border-top:2px solid var(--line);padding-top:1rem" }));
      tables.filter(function (t) { return sectionOf(t) === sec; }).forEach(function (t) {
        frag.appendChild(safe(function () { return tableBlock(runId, winMap, t, sec); }, "table"));
      });
      texts.filter(function (t) { return sectionOf(t) === sec; }).forEach(function (t) {
        frag.appendChild(safe(function () { return textBlock(t, sec); }, "text"));
      });
    });

    var raws = arr(s.raw);
    if (raws.length) {
      frag.appendChild(el("h2", { text: "Raw files" }));
      raws.forEach(function (r) { frag.appendChild(safe(function () { return rawBlock(r); }, "raw")); });
    }
    frag.appendChild(sourcesBlock(s.sources));
    return frag;
  }

  // ------------------------------------------------------------------ router
  var token = 0;

  function parseHash() {
    var raw = (location.hash || "").replace(/^#/, "");
    var segs = raw.split("/").filter(function (x) { return x !== ""; }).map(function (x) {
      try { return decodeURIComponent(x); } catch (e) { return x; }
    });
    return segs;
  }

  function showError(err, retryable) {
    clear(mainEl);
    var status = err && typeof err.status === "number" ? err.status : null;
    var box = errorBox(status !== null ? "Could not load this view (HTTP status " + status + ")" : "Could not show this view",
      err && err.message ? err.message : "unknown error");
    if (retryable) box.appendChild(el("div", { class: "row" }, el("button", { type: "button", class: "btn", onclick: function () { render(); } }, "Retry")));
    mainEl.appendChild(box);
  }

  function render() {
    var my = ++token;
    var segs = parseHash();
    setToolbar(null);
    window.scrollTo(0, 0);
    clear(mainEl);
    mainEl.appendChild(el("p", { class: "muted", text: "Loading..." }));

    function done(frag) {
      if (my !== token) return;
      clear(mainEl);
      mainEl.appendChild(frag);
    }
    function fail(e) { if (my === token) showError(e, true); }

    try {
      if (segs.length === 0) {
        document.title = "Campaign - run viewer";
        setBreadcrumb([{ label: "Campaign", href: "#/" }]);
        api("/api/runs").then(function (d) { done(renderView1(d)); }).catch(fail);
        return;
      }
      if (segs[0] === "run" && segs.length === 2) {
        var id = segs[1];
        document.title = id + " - run viewer";
        setBreadcrumb([{ label: "Campaign", href: "#/" }, { label: id, href: hRun(id) }]);
        api("/api/run/" + enc(id)).then(function (d) { done(renderView2(id, d)); }).catch(fail);
        return;
      }
      if (segs[0] === "run" && segs[2] === "step" && segs.length === 4) {
        var rid = segs[1], step = segs[3];
        document.title = step + " - " + rid + " - run viewer";
        setBreadcrumb([{ label: "Campaign", href: "#/" }, { label: rid, href: hRun(rid) }, { label: step, href: hStep(rid, step) }]);
        api("/api/run/" + enc(rid) + "/step/" + enc(step)).then(function (d) {
          if (my !== token) return null;
          // use the step's own title in the breadcrumb once known
          if (d && typeof d.title === "string" && d.title) {
            setBreadcrumb([{ label: "Campaign", href: "#/" }, { label: rid, href: hRun(rid) }, { label: d.title, href: hStep(rid, step) }]);
          }
          var needsWin = arr(obj(d).tables).some(function (t) {
            return Array.isArray(obj(t).links) || Array.isArray(obj(t).column_links) || (obj(t).by_option && true);
          });
          return (needsWin ? getWinMap(rid) : Promise.resolve(null)).then(function (wm) {
            done(renderView3(rid, step, d, wm));
          });
        }).catch(fail);
        return;
      }
      if (segs[0] === "run" && segs[2] === "variant" && segs[4] === "window" && segs.length === 6) {
        var vr = segs[1], vv = segs[3], vw = segs[5];
        document.title = vv + " " + vw + " - " + vr + " - run viewer";
        setBreadcrumb([{ label: "Campaign", href: "#/" }, { label: vr, href: hRun(vr) },
          { label: vv, href: hRun(vr) }, { label: vw, href: hWin(vr, vv, vw) }]);
        clear(mainEl);
        var host = el("div", { id: "view4" });
        mainEl.appendChild(host);
        if (window.RV_VIEWS && typeof window.RV_VIEWS.variantWindow === "function") {
          try {
            var res = window.RV_VIEWS.variantWindow(host, { runId: vr, variant: vv, window: vw });
            if (res && typeof res.catch === "function") res.catch(function (e) { if (my === token) { clear(host); host.appendChild(errorBox("Chart view failed", e && e.message ? e.message : "error")); } });
          } catch (e) {
            host.appendChild(errorBox("Chart view failed", e && e.message ? e.message : "error"));
          }
        } else {
          host.appendChild(el("p", { class: "muted", text: "chart view not installed" }));
        }
        return;
      }
      document.title = "Not found - run viewer";
      setBreadcrumb([{ label: "Campaign", href: "#/" }, { label: "not found" }]);
      clear(mainEl);
      mainEl.appendChild(errorBox("Unknown address", "No view for: " + (location.hash || "(empty)")));
      mainEl.appendChild(el("p", null, el("a", { href: "#/", text: "Back to Campaign" })));
    } catch (e) {
      showError(e, true);
    }
  }

  // ------------------------------------------------------------------ boot
  window.RV = { api: api, el: el, setBreadcrumb: setBreadcrumb, setToolbar: setToolbar, navigate: navigate };

  function boot() {
    crumbsEl = document.getElementById("crumbs");
    toolbarEl = document.getElementById("toolbar");
    mainEl = document.getElementById("main");
    document.getElementById("reload").addEventListener("click", function () { cache = {}; render(); });
    window.addEventListener("hashchange", render);
    render();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
