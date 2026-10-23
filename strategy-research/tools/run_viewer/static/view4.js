/* run viewer, view 4: one variant in one protocol window (price, forecast, executed
 * position, trades, window equity) plus the chained equity across the run's windows.
 * Read-only; builds DOM with textContent only; no network request except this server's API.
 * Registers window.RV_VIEWS.variantWindow(container, {runId, variant, window}).
 */
(function () {
  'use strict';

  /* ------------------------------------------------------------------ RV fallback stub
   * app.js defines window.RV by plain assignment and replaces this. If it has not (page
   * opened without app.js), the stub routes #/run/<id>/variant/<v>/window/<label> only. */
  function rvStubIfNeeded() {
    if (window.RV) return;
    var api = function (path) {
      return fetch(path, { headers: { Accept: 'application/json' } }).then(function (r) {
        if (!r.ok) {
          var e = new Error('HTTP ' + r.status);
          e.status = r.status;
          throw e;
        }
        return r.json();
      });
    };
    var RVs = {
      __stub: true,
      api: api,
      el: function (tag, attrs) {
        return h.apply(null, arguments);
      },
      setBreadcrumb: function (items) {
        var c = document.getElementById('crumbs');
        if (!c) return;
        c.textContent = (items || []).map(function (i) { return i.label; }).join(' > ');
      },
      setToolbar: function (node) {
        var t = document.getElementById('toolbar');
        if (!t) return;
        t.textContent = '';
        if (node) { t.appendChild(node); t.hidden = false; } else { t.hidden = true; }
      },
      navigate: function (hash) {
        if (hash.charAt(0) !== '#') hash = '#' + hash;
        if (location.hash === hash) route(); else location.hash = hash;
      }
    };
    window.RV = RVs;
    function route() {
      if (!window.RV || !window.RV.__stub) return;
      var main = document.getElementById('main');
      if (!main) return;
      var m = /^#\/run\/([^/]+)\/variant\/([^/]+)\/window\/([^/]+)$/.exec(location.hash);
      if (!m) {
        main.textContent = 'view 4 stub: open #/run/<id>/variant/<v>/window/<label>';
        return;
      }
      var a = { runId: dec(m[1]), variant: dec(m[2]), window: dec(m[3]) };
      RVs.setBreadcrumb([{ label: a.runId }, { label: a.variant }, { label: a.window }]);
      window.RV_VIEWS.variantWindow(main, a);
    }
    document.addEventListener('DOMContentLoaded', function () {
      if (window.RV && window.RV.__stub) {
        route();
        window.addEventListener('hashchange', route);
      }
    });
  }

  function dec(s) { try { return decodeURIComponent(s); } catch (e) { return s; } }
  function enc(s) { return encodeURIComponent(s); }
  function rv() { return window.RV; }

  /* ------------------------------------------------------------------ DOM helper */
  function h(tag, attrs) {
    var e = document.createElement(tag);
    if (attrs) {
      Object.keys(attrs).forEach(function (k) {
        var v = attrs[k];
        if (v === null || v === undefined || v === false) return;
        if (k === 'class') e.className = v;
        else if (k === 'text') e.textContent = v;
        else if (k.slice(0, 2) === 'on' && typeof v === 'function') e.addEventListener(k.slice(2), v);
        else e.setAttribute(k, v === true ? '' : String(v));
      });
    }
    function add(c) {
      if (c === null || c === undefined || c === false) return;
      if (Array.isArray(c)) { c.forEach(add); return; }
      e.appendChild(typeof c === 'object' && c.nodeType ? c : document.createTextNode(String(c)));
    }
    for (var i = 2; i < arguments.length; i++) add(arguments[i]);
    return e;
  }

  rvStubIfNeeded();

  /* ------------------------------------------------------------------ data helpers */
  var TS_RE = /^(\d{4})-(\d{2})-(\d{2})(?:[ T](\d{2}):(\d{2})(?::(\d{2}))?)?/;

  /** "YYYY-MM-DD", "YYYY-MM-DD HH:MM:SS" or ISO with T -> epoch seconds (UTC), else null. */
  function parseTs(s) {
    if (typeof s !== 'string') return null;
    var m = TS_RE.exec(s.trim());
    if (!m) return null;
    var t = Date.UTC(+m[1], +m[2] - 1, +m[3], +(m[4] || 0), +(m[5] || 0), +(m[6] || 0));
    return isFinite(t) ? t / 1000 : null;
  }
  function num(v) { return (typeof v === 'number' && isFinite(v)) ? v : null; }
  function pad2(n) { return (n < 10 ? '0' : '') + n; }
  function fmtDate(sec, withTime) {
    var d = new Date(sec * 1000);
    var s = d.getUTCFullYear() + '-' + pad2(d.getUTCMonth() + 1) + '-' + pad2(d.getUTCDate());
    return withTime ? s + ' ' + pad2(d.getUTCHours()) + ':' + pad2(d.getUTCMinutes()) : s;
  }
  function group(v, dec_) {
    return v.toLocaleString('en-US', { minimumFractionDigits: dec_, maximumFractionDigits: dec_ });
  }
  function fmtAdaptive(v) {
    if (v === null || v === undefined) return '—';
    var a = Math.abs(v);
    return group(v, a >= 1000 ? 1 : a >= 100 ? 2 : a >= 1 ? 3 : 5);
  }
  function fmtFixed(v, d) { return v === null || v === undefined ? '—' : group(v, d); }
  function axisFmt(u, splits, ax, space, incr) {
    var d = incr > 0 ? Math.max(0, Math.min(6, Math.ceil(-Math.log10(incr) - 1e-9))) : 0;
    return splits.map(function (v) { return v === null ? '' : group(v, d); });
  }
  var MON = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'];
  /** single-line UTC time labels (uPlot's default two-line labels are clipped in a short axis) */
  function timeAxisFmt(u, splits, ax, space, incr) {
    return splits.map(function (v) {
      var d = new Date(v * 1000), y = d.getUTCFullYear(), mo = MON[d.getUTCMonth()], da = pad2(d.getUTCDate());
      if (incr >= 86400 * 360) return String(y);
      if (incr >= 86400 * 27) return y + '-' + mo;
      if (incr >= 86400) return mo + '-' + da;
      return pad2(d.getUTCHours()) + ':' + pad2(d.getUTCMinutes());
    });
  }
  function bisectNearest(xs, v) {
    var lo = 0, hi = xs.length - 1;
    if (hi < 0) return -1;
    while (hi - lo > 1) {
      var mid = (lo + hi) >> 1;
      if (xs[mid] <= v) lo = mid; else hi = mid;
    }
    return Math.abs(xs[lo] - v) <= Math.abs(xs[hi] - v) ? lo : hi;
  }
  function median(a) {
    if (!a.length) return 86400;
    var b = a.slice().sort(function (x, y) { return x - y; });
    return b[b.length >> 1];
  }
  function clamp(v, lo, hi) { return Math.min(hi, Math.max(lo, v)); }

  /** bars JSON -> aligned arrays; bars whose timestamp does not parse (e.g. masked) are skipped. */
  function prepareBars(b) {
    var c = (b && b.columns) || {};
    var ts = c.timestamp;
    if (!Array.isArray(ts)) return null;
    var pairs = [];
    for (var i = 0; i < ts.length; i++) {
      var t = parseTs(ts[i]);
      if (t !== null) pairs.push([t, i]);
    }
    pairs.sort(function (a, b2) { return a[0] - b2[0] || a[1] - b2[1]; });
    var keep = [];
    pairs.forEach(function (p) {
      if (!keep.length || keep[keep.length - 1][0] !== p[0]) keep.push(p);
    });
    if (keep.length < 2) return { xs: keep.map(function (p) { return p[0]; }), tooShort: true };
    var xs = keep.map(function (p) { return p[0]; });
    function col(name) {
      var a = c[name];
      if (!Array.isArray(a)) return null;
      var out = keep.map(function (p) { return num(a[p[1]]); });
      return out.some(function (v) { return v !== null; }) ? out : null;
    }
    var step = median(xs.slice(1).map(function (v, k) { return v - xs[k]; }));
    var withTime = xs.some(function (v) { return v % 86400 !== 0; });
    return {
      xs: xs, step: step, withTime: withTime,
      close: col('close'), forecast: col('forecast'),
      position: col('position'), equity: col('portfolio_value')
    };
  }

  /** chained-equity JSON -> one series with null points between windows (line breaks). */
  function prepareChain(eq, label) {
    var xs = [], ys = [], span = null, any = false, lastEnd = null;
    ((eq && eq.windows) || []).forEach(function (w) {
      if (!Array.isArray(w.timestamps) || !Array.isArray(w.equity) || w.timestamps.length !== w.equity.length) return;
      var pts = [];
      for (var i = 0; i < w.timestamps.length; i++) {
        var t = parseTs(w.timestamps[i]);
        if (t !== null) pts.push([t, num(w.equity[i])]);
      }
      pts.sort(function (a, b) { return a[0] - b[0]; });
      if (!pts.length) return;
      var first = pts[0][0];
      if (lastEnd !== null) {
        if (first <= lastEnd) {
          // overlapping window: start it after the previous one so x stays increasing
          pts = pts.filter(function (p) { return p[0] > lastEnd; });
          if (!pts.length) return;
          first = pts[0][0];
        }
        xs.push((lastEnd + first) / 2);
        ys.push(null);
      }
      pts.forEach(function (p) {
        if (xs.length && p[0] <= xs[xs.length - 1]) return;
        xs.push(p[0]);
        ys.push(p[1]);
        if (p[1] !== null) any = true;
      });
      lastEnd = pts[pts.length - 1][0];
      if (w.label === label) span = [pts[0][0], pts[pts.length - 1][0]];
    });
    if (!any || xs.length < 2) return null;
    return { xs: xs, ys: ys, span: span };
  }

  function tradeTimeText(s) {
    if (typeof s !== 'string') return '—';
    return s.replace('T', ' ').replace(/ 00:00:00$/, '');
  }

  /* ------------------------------------------------------------------ instance */
  var current = null;
  var tokenSeq = 0;

  function teardown() {
    if (current) { current.destroy(); current = null; }
  }

  function checkDetached() {
    if (current && !current.root.isConnected) teardown();
  }
  window.addEventListener('hashchange', function () {
    setTimeout(checkDetached, 0);
    setTimeout(checkDetached, 300);
  });

  function Instance(container, args) {
    this.container = container;
    this.args = args;
    this.token = ++tokenSeq;
    this.alive = true;
    this.charts = [];          // the four panes
    this.chain = null;         // chained equity chart
    this.listeners = [];
    this.paneListeners = [];
    this.view = null;          // {min, max}
    this.applying = false;
    this.lastW = 0;
    this.selIdx = null;
    this.data = null;
    this.markers = [];
    this.windows = [];
    this.variants = [args.variant];
    this.eqCache = {};
  }

  Instance.prototype.listen = function (target, type, fn, opts) {
    target.addEventListener(type, fn, opts);
    this.listeners.push([target, type, fn, opts]);
  };

  Instance.prototype.destroy = function () {
    this.alive = false;
    this.destroyCharts();
    if (this.ro) { try { this.ro.disconnect(); } catch (e) { /* ignore */ } this.ro = null; }
    this.listeners.forEach(function (l) { l[0].removeEventListener(l[1], l[2], l[3]); });
    this.listeners = [];
    if (this.root && this.root.parentNode) this.root.parentNode.removeChild(this.root);
  };

  Instance.prototype.destroyCharts = function () {
    this.paneListeners.forEach(function (l) { l[0].removeEventListener(l[1], l[2], l[3]); });
    this.paneListeners = [];
    this.charts.forEach(function (c) { try { c.u.destroy(); } catch (e) { /* ignore */ } });
    this.charts = [];
    if (this.chain) { try { this.chain.destroy(); } catch (e) { /* ignore */ } this.chain = null; }
  };

  Instance.prototype.start = function () {
    var self = this, a = this.args;
    this.container.textContent = '';
    this.root = h('div', { class: 'rv4' });
    this.container.appendChild(this.root);
    this.buildToolbar();
    this.body = h('div', { class: 'rv4-body' }, h('p', { class: 'rv4-note', text: 'Loading...' }));
    this.root.appendChild(this.body);

    this.ro = (typeof ResizeObserver === 'function') ? new ResizeObserver(function () {
      if (!self.alive) return;
      if (!self.root.isConnected) { teardown(); return; }
      self.onResize();
    }) : null;
    if (this.ro) this.ro.observe(this.root);
    if (window.matchMedia) {
      var mq = window.matchMedia('(prefers-color-scheme: dark)');
      var onScheme = function () { if (self.alive && self.data) self.buildCharts(); };
      this.listen(mq, 'change', onScheme);
    }

    var base = '/api/run/' + enc(a.runId);
    var runP = rv().api(base).then(function (j) {
      var vs = j && j.header && j.header.variants;
      return Array.isArray(vs) ? vs.filter(function (v) { return typeof v === 'string'; }) : null;
    }).catch(function () { return null; });
    var eqP = rv().api(base + '/variant/' + enc(a.variant) + '/equity');
    Promise.all([runP, eqP]).then(function (res) {
      if (!self.alive) return;
      var vs = res[0] || [];
      if (vs.indexOf(a.variant) < 0) vs = [a.variant].concat(vs);
      self.variants = vs;
      var eq = res[1];
      self.eqCache[a.variant] = eq;
      self.eq = eq;
      self.windows = ((eq && eq.windows) || []).map(function (w) { return w.label; });
      self.syncToolbar();
      if (!self.windows.length) {
        self.showMsg('no protocol windows for this variant', false);
        return;
      }
      if (self.windows.indexOf(a.window) < 0) {
        self.showMsg('window "' + a.window + '" is not a window of variant "' + a.variant + '". Choose one above.', true);
        return;
      }
      return rv().api(base + '/variant/' + enc(a.variant) + '/window/' + enc(a.window) + '/bars').then(function (b) {
        if (!self.alive) return;
        self.bars = b;
        self.renderBody();
      });
    }).catch(function (err) {
      if (!self.alive) return;
      self.showError(err);
    });
  };

  Instance.prototype.showMsg = function (text, isError) {
    this.body.textContent = '';
    this.body.appendChild(h('p', { class: isError ? 'rv4-error' : 'rv4-note', text: text }));
  };
  Instance.prototype.showError = function (err) {
    this.body.textContent = '';
    var st = err && err.status ? 'HTTP ' + err.status : 'error';
    this.body.appendChild(h('div', { class: 'rv4-error', role: 'alert' },
      h('strong', { text: 'Could not load this view (' + st + ')' }),
      h('div', { text: err && err.message ? String(err.message) : '' })));
  };

  /* ---------------------------------------------------------------- toolbar */
  Instance.prototype.buildToolbar = function () {
    var self = this, a = this.args;
    this.selVariant = h('select', {
      class: 'rv4-sel', 'aria-label': 'variant',
      onchange: function () { self.onVariantChange(self.selVariant.value); }
    });
    this.selWindow = h('select', {
      class: 'rv4-sel', 'aria-label': 'window',
      onchange: function () { self.go(self.args.variant, self.selWindow.value); }
    });
    this.btnReset = h('button', {
      type: 'button', class: 'rv4-btn', title: 'Reset zoom', disabled: true,
      onclick: function () { self.resetView(); }
    }, 'Reset zoom');
    var cells = [['date', 'date'], ['close', 'close'], ['forecast', 'forecast'], ['pos', 'position'], ['eq', 'equity']];
    this.stripVals = {};
    var strip = h('div', { class: 'rv4-strip', 'aria-label': 'values of the selected bar' });
    cells.forEach(function (c) {
      var v = h('span', { class: 'rv4-sv', text: '—' });
      self.stripVals[c[0]] = v;
      strip.appendChild(h('div', { class: 'rv4-sc rv4-sc-' + c[0] }, h('span', { class: 'rv4-sk', text: c[1] }), v));
    });
    this.toolbar = h('div', { class: 'rv4 rv4-toolbar' },
      h('div', { class: 'rv4-ctl' }, this.selVariant, this.selWindow, this.btnReset), strip);
    this.syncToolbar();
    rv().setToolbar(this.toolbar);
    // the app owns the toolbar slot; nothing more to do on destroy (the next view replaces it)
    void a;
  };

  function fillSelect(sel, values, selected) {
    sel.textContent = '';
    values.forEach(function (v) {
      var o = document.createElement('option');
      o.value = v; o.textContent = v;
      if (v === selected) o.selected = true;
      sel.appendChild(o);
    });
    sel.value = selected;
  }
  Instance.prototype.syncToolbar = function () {
    fillSelect(this.selVariant, this.variants, this.args.variant);
    fillSelect(this.selWindow, this.windows.length ? this.windows : [this.args.window], this.args.window);
  };

  Instance.prototype.go = function (variant, win) {
    rv().navigate('#/run/' + enc(this.args.runId) + '/variant/' + enc(variant) + '/window/' + enc(win));
  };

  Instance.prototype.onVariantChange = function (v) {
    var self = this, cur = this.args.window;
    function pick(eq) {
      var ws = ((eq && eq.windows) || []).map(function (w) { return w.label; });
      self.go(v, ws.indexOf(cur) >= 0 ? cur : (ws[0] || cur));
    }
    if (this.eqCache[v]) { pick(this.eqCache[v]); return; }
    rv().api('/api/run/' + enc(this.args.runId) + '/variant/' + enc(v) + '/equity').then(function (eq) {
      self.eqCache[v] = eq;
      pick(eq);
    }).catch(function () { pick(null); });
  };

  /* ---------------------------------------------------------------- strip */
  Instance.prototype.setStrip = function (i) {
    var d = this.data;
    if (!d || i === null || i === undefined || i < 0 || i >= d.xs.length) return;
    this.selIdx = i;
    var s = this.stripVals;
    s.date.textContent = fmtDate(d.xs[i], d.withTime);
    s.close.textContent = d.close ? fmtAdaptive(d.close[i]) : 'absent';
    s.forecast.textContent = d.forecast ? fmtFixed(d.forecast[i], 2) : 'absent';
    s.pos.textContent = d.position ? fmtFixed(d.position[i], 3) : 'absent';
    s.eq.textContent = d.equity ? fmtFixed(d.equity[i], 2) : 'absent';
  };
  Instance.prototype.stripLast = function () {
    if (this.data) this.setStrip(this.data.xs.length - 1);
  };

  /* ---------------------------------------------------------------- body */
  Instance.prototype.renderBody = function () {
    var self = this, b = this.bars || {};
    this.data = prepareBars(b);
    this.body.textContent = '';
    var d = this.data;

    var charts = h('section', { class: 'rv4-sec rv4-charts' });
    this.chartsEl = charts;
    this.body.appendChild(charts);
    if (!d || d.tooShort) {
      charts.appendChild(h('p', { class: 'rv4-note', text: d ? 'absent: fewer than two usable bars in this window' : 'absent: no bars (timestamps missing)' }));
      this.data = null;
    }

    this.chainEl = h('section', { class: 'rv4-sec' }, h('h3', { text: 'Chained equity, variant "' + this.args.variant + '", all windows' }));
    this.chainBox = h('div', { class: 'rv4-chartbox rv4-chain' });
    this.chainEl.appendChild(this.chainBox);
    this.body.appendChild(this.chainEl);

    this.body.appendChild(this.metricsSection(b.metrics));
    this.body.appendChild(this.tradesSection(b.trades));

    if (this.data) {
      this.markers = this.computeMarkers(b.trades);
      this.view = { min: this.data.xs[0], max: this.data.xs[this.data.xs.length - 1] };
      this.buildCharts();
    } else {
      this.buildChain();
    }
    void self;
  };

  Instance.prototype.computeMarkers = function (trades) {
    var d = this.data, out = [];
    if (!d || !Array.isArray(trades)) return out;
    var lo = d.xs[0] - d.step, hi = d.xs[d.xs.length - 1] + d.step;
    function at(s) {
      var t = parseTs(s);
      if (t === null || t < lo || t > hi) return -1;
      return bisectNearest(d.xs, t);
    }
    trades.forEach(function (t) {
      if (!t || typeof t !== 'object') return;
      var win = typeof t.net_profit_loss_percent === 'number' ? t.net_profit_loss_percent >= 0 : false;
      var short = String(t.side || '').toUpperCase() === 'SHORT';
      var ei = at(t.entry_time), xi = at(t.exit_time);
      if (ei >= 0) out.push({ i: ei, kind: 'entry', short: short, win: win });
      if (xi >= 0) out.push({ i: xi, kind: 'exit', short: short, win: win });
    });
    return out;
  };

  Instance.prototype.metricsSection = function (m) {
    var sec = h('section', { class: 'rv4-sec' }, h('h3', { text: 'Metrics' }));
    var rows = [
      ['net_return_pct', 'Net return %', function (v) { return fmtFixed(v, 2); }],
      ['sharpe', 'Sharpe', function (v) { return fmtFixed(v, 2); }],
      ['max_drawdown_pct', 'Max drawdown %', function (v) { return fmtFixed(v, 2); }],
      ['trade_count', 'Trades', function (v) { return fmtFixed(v, 0); }],
      ['win_rate', 'Win rate %', function (v) { return fmtFixed(v, 1); }]
    ];
    var dl = h('dl', { class: 'rv4-kv' }), n = 0;
    if (m && typeof m === 'object') {
      rows.forEach(function (r) {
        var v = num(m[r[0]]);
        if (v === null) return;
        dl.appendChild(h('dt', { text: r[1] }));
        dl.appendChild(h('dd', { text: r[2](v) }));
        n++;
      });
    }
    sec.appendChild(n ? dl : h('p', { class: 'rv4-note', text: 'absent' }));
    return sec;
  };

  Instance.prototype.tradesSection = function (trades) {
    var sec = h('section', { class: 'rv4-sec' });
    var list = Array.isArray(trades) ? trades.filter(function (t) { return t && typeof t === 'object'; }) : null;
    sec.appendChild(h('h3', { text: 'Trades' + (list ? ' (' + list.length + ')' : '') }));
    if (list === null) { sec.appendChild(h('p', { class: 'rv4-note', text: 'absent' })); return sec; }
    if (!list.length) { sec.appendChild(h('p', { class: 'rv4-note', text: 'no trades in this window' })); return sec; }
    var heads = ['Entry', 'Exit', 'Side', 'Net %', 'Duration (days)'];
    var tb = h('tbody');
    list.forEach(function (t) {
      var np = num(t.net_profit_loss_percent), dm = num(t.duration_minutes);
      tb.appendChild(h('tr', null,
        h('td', { 'data-label': heads[0], text: tradeTimeText(t.entry_time) }),
        h('td', { 'data-label': heads[1], text: tradeTimeText(t.exit_time) }),
        h('td', { 'data-label': heads[2], text: t.side ? String(t.side) : '—' }),
        h('td', { 'data-label': heads[3], class: 'rv4-num ' + (np === null ? '' : np >= 0 ? 'rv4-pos' : 'rv4-neg'),
          text: np === null ? '—' : (np >= 0 ? '+' : '') + group(np, 2) + '%' }),
        h('td', { 'data-label': heads[4], class: 'rv4-num', text: dm === null ? '—' : group(dm / 1440, 1) })));
    });
    sec.appendChild(h('table', { class: 'rv4-trades' },
      h('thead', null, h('tr', null, heads.map(function (x) { return h('th', { scope: 'col', text: x }); }))), tb));
    return sec;
  };

  /* ---------------------------------------------------------------- theme */
  Instance.prototype.theme = function () {
    var cs = getComputedStyle(this.root);
    function v(n, d) { var x = cs.getPropertyValue(n).trim(); return x || d; }
    return {
      axis: v('--rv4-axis', '#5b6470'), grid: v('--rv4-grid', 'rgba(128,128,128,.25)'),
      cursor: v('--rv4-cursor', '#888'), bg: v('--rv4-bg', '#fff'),
      price: v('--rv4-price', '#2563eb'), forecast: v('--rv4-forecast', '#7c3aed'),
      position: v('--rv4-position', '#0d9488'), positionFill: v('--rv4-position-fill', 'rgba(13,148,136,.25)'),
      equity: v('--rv4-equity', '#b45309'), win: v('--rv4-win', '#1a7f37'), loss: v('--rv4-loss', '#c62828'),
      shade: v('--rv4-shade', 'rgba(37,99,235,.15)'), zero: v('--rv4-zero', 'rgba(128,128,128,.6)')
    };
  };

  Instance.prototype.heights = function () {
    var wide = this.root.clientWidth >= 800;
    return wide ? { pane: [300, 150, 150, 170], chain: 190 } : { pane: [200, 110, 110, 120], chain: 150 };
  };

  /* ---------------------------------------------------------------- charts */
  function padRange(lo, hi, includeZero) {
    if (includeZero) { lo = Math.min(lo, 0); hi = Math.max(hi, 0); }
    if (!(isFinite(lo) && isFinite(hi))) return [0, 1];
    if (hi === lo) { var e = Math.abs(hi) * 0.01 || 1; return [lo - e, hi + e]; }
    var p = (hi - lo) * 0.08;
    return [includeZero && lo === 0 ? 0 - p * 0.0 : lo - p, hi + p];
  }

  function tri(ctx, x, y, s, dir, color, bg, hollow) {
    // dir +1: points up, body below the price point; dir -1: points down, body above it
    var px = window.devicePixelRatio || 1, gap = 2 * px, w = s * 0.6;
    var ya = y + (dir > 0 ? gap : -gap);          // apex, next to the price point
    var yb = ya + (dir > 0 ? s : -s);             // base
    ctx.beginPath();
    ctx.moveTo(x, ya);
    ctx.lineTo(x - w, yb);
    ctx.lineTo(x + w, yb);
    ctx.closePath();
    if (hollow) {
      ctx.globalAlpha = 0.85; ctx.fillStyle = bg; ctx.fill(); ctx.globalAlpha = 1;
      ctx.lineWidth = 2 * px; ctx.strokeStyle = color; ctx.stroke();
    } else {
      ctx.fillStyle = color; ctx.fill();
      ctx.lineWidth = px; ctx.strokeStyle = bg; ctx.stroke();
    }
  }

  Instance.prototype.paneSpecs = function (th) {
    var d = this.data, self = this;
    return [
      { key: 'close', cap: 'close, trades: entry (filled) / exit (hollow), green = win, red = loss',
        series: d.close, color: th.price, includeZero: false, fmt: axisFmt, markers: true },
      { key: 'forecast', cap: 'forecast', series: d.forecast, color: th.forecast, includeZero: true, zero: true },
      { key: 'position', cap: 'executed position', series: d.position, color: th.position, includeZero: true,
        zero: true, step: true, fill: th.positionFill },
      { key: 'equity', cap: 'window equity (portfolio value)', series: d.equity, color: th.equity, includeZero: false }
    ].map(function (s) { s.self = self; return s; });
  };

  Instance.prototype.commonOpts = function (th, key, w, hgt) {
    return {
      width: w, height: hgt, legend: { show: false }, padding: [6, 10, 0, 0],
      tzDate: function (ts) { return uPlot.tzDate(new Date(ts * 1e3), 'Etc/UTC'); },
      axes: [
        { stroke: th.axis, size: 24, gap: 2, font: '11px system-ui, sans-serif', values: timeAxisFmt,
          grid: { stroke: th.grid, width: 1 }, ticks: { stroke: th.grid, size: 4, width: 1 } },
        { stroke: th.axis, size: 54, gap: 2, font: '11px system-ui, sans-serif', values: axisFmt,
          grid: { stroke: th.grid, width: 1 }, ticks: { stroke: th.grid, size: 4, width: 1 } }
      ]
    };
  };

  Instance.prototype.buildCharts = function () {
    var self = this, d = this.data;
    this.destroyCharts();
    if (!d) { this.buildChain(); return; }
    var th = this.theme();
    var box = this.chartsEl;
    box.textContent = '';
    var w = Math.max(100, Math.floor(box.clientWidth || this.root.clientWidth || 360));
    this.lastW = w;
    var hs = this.heights();
    var key = 'rv4-' + this.token;
    var ready = false;

    this.paneSpecs(th).forEach(function (spec, idx) {
      var wrap = h('div', { class: 'rv4-pane' }, h('div', { class: 'rv4-cap', text: spec.cap }));
      box.appendChild(wrap);
      if (!spec.series) {
        wrap.appendChild(h('div', { class: 'rv4-absent', text: 'absent' }));
        return;
      }
      var cb = h('div', { class: 'rv4-chartbox' });
      wrap.appendChild(cb);
      var o = self.commonOpts(th, key, w, hs.pane[idx]);
      var lo = Infinity, hi = -Infinity;
      spec.series.forEach(function (v) { if (v !== null) { if (v < lo) lo = v; if (v > hi) hi = v; } });
      o.scales = {
        x: { time: true },
        y: { range: function (u, dmin, dmax) {
          var r = padRange(dmin === null || dmin === undefined ? lo : dmin, dmax === null || dmax === undefined ? hi : dmax, spec.includeZero);
          return r;
        } }
      };
      o.cursor = {
        sync: { key: key, setSeries: false },
        y: false,
        move: function (u, l, t) {
          if (l < 0) return [l, t];
          var i = bisectNearest(d.xs, u.posToVal(l, 'x'));
          if (i < 0) return [l, t];
          var x = u.valToPos(d.xs[i], 'x');
          return [isFinite(x) ? x : l, t];
        },
        drag: { x: true, y: false, setScale: true },
        points: { size: 7, width: 1 }
      };
      o.series = [{}, {
        stroke: spec.color, width: 1.5, points: { show: false }, spanGaps: false,
        fill: spec.fill || undefined,
        paths: spec.step ? uPlot.paths.stepped({ align: 1 }) : undefined
      }];
      o.hooks = {
        setCursor: [function (u) {
          if (!ready) return;
          var i = u.cursor.idx;
          if (i !== null && i !== undefined) self.setStrip(i);
        }],
        setScale: [function (u, k) {
          if (!ready || self.applying || k !== 'x') return;
          var s = u.scales.x;
          if (s.min !== null && s.max !== null) self.applyView(s.min, s.max, u);
        }],
        draw: [function (u) {
          if (spec.zero) {
            var y0 = u.valToPos(0, 'y', true), bb = u.bbox;
            if (y0 >= bb.top && y0 <= bb.top + bb.height) {
              var c = u.ctx;
              c.save(); c.strokeStyle = th.zero; c.lineWidth = 1 * (window.devicePixelRatio || 1);
              c.setLineDash([4, 4]); c.beginPath(); c.moveTo(bb.left, y0); c.lineTo(bb.left + bb.width, y0); c.stroke(); c.restore();
            }
          }
          if (spec.markers) self.drawMarkers(u, th);
        }],
        ready: [function (u) { self.wirePane(u); }]
      };
      var u = new uPlot(o, [d.xs, spec.series], cb);
      self.charts.push({ u: u, idx: idx });
    });

    ready = true;
    this.applyView(this.view.min, this.view.max, null);
    this.updateResetBtn();
    if (this.selIdx !== null) this.setStrip(this.selIdx); else this.stripLast();
    this.buildChain();
  };

  Instance.prototype.drawMarkers = function (u, th) {
    var d = this.data, ctx = u.ctx, close = d.close;
    if (!close || !this.markers.length) return;
    var px = window.devicePixelRatio || 1, s = 11 * px, bb = u.bbox;
    ctx.save();
    ctx.beginPath(); ctx.rect(bb.left - 8 * px, bb.top - 6 * px, bb.width + 16 * px, bb.height + 12 * px); ctx.clip();
    this.markers.forEach(function (m) {
      var yv = close[m.i];
      if (yv === null || yv === undefined) return;
      var x = u.valToPos(d.xs[m.i], 'x', true), y = u.valToPos(yv, 'y', true);
      var color = m.win ? th.win : th.loss;
      var isEntry = m.kind === 'entry';
      // entry: LONG points up (body under the price), SHORT points down; exit is the opposite way, hollow
      var up = isEntry ? !m.short : m.short;
      tri(ctx, x, y, s, up ? 1 : -1, color, th.bg, !isEntry);
    });
    ctx.restore();
  };

  /* ---------------------------------------------------------------- chained equity */
  Instance.prototype.buildChain = function () {
    var self = this, th = this.theme(), box = this.chainBox;
    if (this.chain) { try { this.chain.destroy(); } catch (e) { /* ignore */ } this.chain = null; }
    box.textContent = '';
    var ch = prepareChain(this.eq, this.args.window);
    if (!ch) { box.appendChild(h('div', { class: 'rv4-absent', text: 'absent' })); return; }
    var w = Math.max(100, Math.floor(box.clientWidth || this.root.clientWidth || 360));
    var hs = this.heights();
    var o = this.commonOpts(th, 'rv4c-' + this.token, w, hs.chain);
    var lo = Infinity, hi = -Infinity;
    ch.ys.forEach(function (v) { if (v !== null) { if (v < lo) lo = v; if (v > hi) hi = v; } });
    o.scales = { x: { time: true }, y: { range: function () { return padRange(lo, hi, false); } } };
    o.cursor = { y: false, drag: { x: false, y: false }, points: { size: 7, width: 1 } };
    o.series = [{}, { stroke: th.equity, width: 1.5, points: { show: false }, spanGaps: false }];
    o.hooks = {
      drawClear: [function (u) {
        if (!ch.span) return;
        var c = u.ctx, bb = u.bbox;
        var x0 = clamp(u.valToPos(ch.span[0], 'x', true), bb.left, bb.left + bb.width);
        var x1 = clamp(u.valToPos(ch.span[1], 'x', true), bb.left, bb.left + bb.width);
        c.save(); c.fillStyle = th.shade; c.fillRect(x0, bb.top, Math.max(1, x1 - x0), bb.height); c.restore();
      }]
    };
    this.chain = new uPlot(o, [ch.xs, ch.ys], box);
    void self;
  };

  /* ---------------------------------------------------------------- view (zoom) */
  Instance.prototype.fullRange = function () {
    var xs = this.data.xs;
    return [xs[0], xs[xs.length - 1]];
  };
  Instance.prototype.isFull = function () {
    var f = this.fullRange(), v = this.view;
    return !v || (v.min <= f[0] + 1e-6 && v.max >= f[1] - 1e-6);
  };
  Instance.prototype.updateResetBtn = function () {
    if (this.btnReset) this.btnReset.disabled = !this.data || this.isFull();
  };
  Instance.prototype.applyView = function (min, max, src) {
    if (!this.data || !(isFinite(min) && isFinite(max))) return;
    var f = this.fullRange(), full = f[1] - f[0];
    var minRange = Math.min(full, Math.max(this.data.step * 5, 1));
    var range = clamp(max - min, minRange, full);
    min = clamp(min, f[0], f[1] - range);
    max = min + range;
    this.view = { min: min, max: max };
    this.applying = true;
    try {
      this.charts.forEach(function (c) {
        var s = c.u.scales.x;
        if (s.min === min && s.max === max) return;
        c.u.setScale('x', { min: min, max: max });
      });
    } finally {
      this.applying = false;
    }
    this.updateResetBtn();
    void src;
  };
  Instance.prototype.resetView = function () {
    if (!this.data) return;
    var f = this.fullRange();
    this.applyView(f[0], f[1], null);
  };

  Instance.prototype.onResize = function () {
    var w = Math.floor(this.chartsEl && this.chartsEl.clientWidth || 0);
    var hs = this.heights();
    if (w > 0 && this.charts.length) {
      this.charts.forEach(function (c) { c.u.setSize({ width: w, height: hs.pane[c.idx] }); });
    }
    var cw = Math.floor(this.chainBox && this.chainBox.clientWidth || 0);
    if (this.chain && cw > 0) this.chain.setSize({ width: cw, height: hs.chain });
    if (w > 0) this.lastW = w;
  };

  /* ---------------------------------------------------------------- pointer / touch */
  Instance.prototype.selectAt = function (u, clientX) {
    var d = this.data;
    if (!d) return;
    var rect = u.over.getBoundingClientRect();
    var left = clamp(clientX - rect.left, 0, rect.width);
    var i = bisectNearest(d.xs, u.posToVal(left, 'x'));
    if (i < 0) return;
    this.setStrip(i);
    var self = this;
    this.charts.forEach(function (c) {
      var x = c.u.valToPos(d.xs[i], 'x');
      if (isFinite(x)) c.u.setCursor({ left: x, top: 1 }, false, false);
    });
    void self;
  };

  Instance.prototype.wirePane = function (u) {
    var self = this, over = u.over;
    var listen = function (t, type, fn, opts) { t.addEventListener(type, fn, opts); self.paneListeners.push([t, type, fn, opts]); };
    // mouse: leave -> back to the last bar; double click -> reset zoom
    listen(over, 'pointerleave', function (e) {
      if (e.pointerType === 'mouse') self.stripLast();
    });
    listen(over, 'dblclick', function () { self.resetView(); });

    var st = null;
    function plotW() { return over.getBoundingClientRect().width || 1; }
    function posOf(clientX) {
      var r = over.getBoundingClientRect();
      return clamp((clientX - r.left) / (r.width || 1), 0, 1);
    }
    function startOne(t) {
      st = { mode: 'one', x0: t.clientX, y0: t.clientY, view0: { min: self.view.min, max: self.view.max }, dir: null };
    }
    listen(over, 'touchstart', function (e) {
      if (!self.data) return;
      if (e.touches.length === 1) {
        startOne(e.touches[0]);
        self.selectAt(u, e.touches[0].clientX);
      } else if (e.touches.length >= 2) {
        var a = e.touches[0], b = e.touches[1];
        var cx = (a.clientX + b.clientX) / 2;
        var v0 = { min: self.view.min, max: self.view.max };
        st = {
          mode: 'pinch', d0: Math.max(24, Math.abs(a.clientX - b.clientX)), view0: v0,
          anchor: v0.min + posOf(cx) * (v0.max - v0.min)
        };
      }
    }, { passive: true });
    listen(over, 'touchmove', function (e) {
      if (!st || !self.data) return;
      if (st.mode === 'pinch' && e.touches.length >= 2) {
        var a = e.touches[0], b = e.touches[1];
        var dist = Math.max(24, Math.abs(a.clientX - b.clientX));
        var range = (st.view0.max - st.view0.min) * (st.d0 / dist);
        var frac = posOf((a.clientX + b.clientX) / 2);
        self.applyView(st.anchor - frac * range, st.anchor - frac * range + range, u);
      } else if (st.mode === 'one' && e.touches.length === 1) {
        var t = e.touches[0], dx = t.clientX - st.x0, dy = t.clientY - st.y0;
        if (st.dir === null && (Math.abs(dx) > 6 || Math.abs(dy) > 6)) {
          st.dir = Math.abs(dx) >= Math.abs(dy) * 1.2 ? 'h' : 'v';
        }
        if (st.dir === 'h') {
          if (self.isFull()) {
            self.selectAt(u, t.clientX);        // nothing to pan: scrub the strip
          } else {
            var r0 = st.view0.max - st.view0.min;
            var shift = -dx / plotW() * r0;
            self.applyView(st.view0.min + shift, st.view0.max + shift, u);
          }
        }
      }
    }, { passive: true });
    function end(e) {
      if (!st) return;
      if (e.touches && e.touches.length === 1 && st.mode === 'pinch') {
        startOne(e.touches[0]);
        st.dir = 'h';
      } else if (!e.touches || e.touches.length === 0) {
        st = null;
      }
    }
    listen(over, 'touchend', end, { passive: true });
    listen(over, 'touchcancel', function () { st = null; }, { passive: true });
  };

  /* ---------------------------------------------------------------- registration */
  // read-only snapshot of the zoom state (used to check gestures; harmless otherwise)
  window.RV_VIEWS = window.RV_VIEWS || {};
  window.RV_VIEWS.variantWindowState = function () {
    if (!current || !current.data) return null;
    var f = current.fullRange();
    return { min: current.view.min, max: current.view.max, fullMin: f[0], fullMax: f[1], sel: current.selIdx, n: current.data.xs.length };
  };
  window.RV_VIEWS = window.RV_VIEWS || {};
  window.RV_VIEWS.variantWindow = function (container, args) {
    teardown();
    if (!container || !args) return;
    var inst = new Instance(container, args);
    current = inst;
    inst.start();
  };
})();
