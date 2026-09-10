# DATA_AVAILABILITY.md

**Read this in full, every time a timeframe, symbol, or venue changes for a
hypothesis.** It is short by design — a forced-read light doc (E-045 S2), not
a browsable reference. Extracted from `TIMEFRAME_CHANGE_PLAYBOOK.md` §2
(bar-count/signal-shape half only) and §8/8a/8b; that playbook is being
retired once every section has a confirmed new home — do not treat it as
current for anything covered here.

---

## 1. What's actually cacheable

OHLCV caches are keyed **exact-timeframe**, per exchange, per symbol:
`{exchange_prefix}{SYMBOL}_{ccxt_timeframe}.csv` (Binance unprefixed for
backward compatibility; any other venue gets an `{exchange}_` prefix). There
is no "closest available" lookup — `CcxtFetcher.cache_key()` returns exactly
what it was constructed with, nothing more forgiving.

## 2. The exact-cache-missing rule (current engine behavior, since CUL-250 / PR #133, 2026-09-03)

**This is corrected from the old playbook, which is now stale.** The old
claim — "a coarser timeframe is always derived from a finer cache
automatically" — is **not** how it works, and never fully was:

- Deriving a coarser timeframe from a finer cache is an **explicit, off-by-default
  opt-in**, not automatic detection. It requires setting `trading.fetch_interval_seconds`
  (config) to a resolution finer than the strategy's `interval_seconds`. When
  set, OHLCV is fetched/cached at that finer resolution and `CandleBuilder`
  aggregates it up during replay. Left unset (the default), the engine fetches
  and looks up the cache at the exact target timeframe only — no fallback,
  byte-identical to pre-CUL-250 behavior.
- If you move a hypothesis to a timeframe with no native cache, and you do
  **not** set `fetch_interval_seconds`, the run raises `"No historical data"` —
  it does not search for or silently fall back to a finer cache on its own.
- Constraints enforced, fail-loud: `fetch_interval_seconds` must be
  `<= interval_seconds` and must evenly divide it. A non-dividing source (e.g.
  a 4h bar from 90-minute rows) is refused outright, never silently misaligned.
- **Action when registering a new timeframe**: check whether a native cache
  exists first; if not, explicitly set `fetch_interval_seconds` to the
  coarsest cache that evenly divides your target timeframe, or fetch the
  native cache directly. Don't assume the engine will find it for you.
- Full mechanism, file:line references, and provenance/manifest behavior:
  `trading-bot/DOC/USER_GUIDE.md` §3.2. Do not re-derive it here.

## 3. Registered aux feeds (pointer only)

- `funding_rate`, `fear_greed` — native `window_seconds=0` (instantaneous),
  `agg='last'` correct by design for both.
- whale-footprint feeds — reserved/opt-in only, native window = one bar
  forward; `agg='last'` would be a latent correctness gap if ever registered
  at a native granularity finer than the consuming strategy's candle interval
  (tracked, not yet triggered — CUL-253).
- Full mechanism (`register_feed()`, `_premerge_aux_feeds()`, cache-key vs.
  merge-timing split, live-vs-backtest divergence): `trading-bot/DOC/USER_GUIDE.md`
  §3.3. Do not duplicate that explanation here.

## 4. Bar-count / signal-shape sweep — run this on ANY timeframe or config change

- [ ] Hardcoded periods/block sizes near `period`/`window`/`lookback`/`block_size` —
      do they assume the OLD timeframe's bar count?
- [ ] Annualization factors (`sqrt(365)` vs `sqrt(8760)`, etc.) — does the
      function group to calendar time first (safe), or work directly in raw
      bar units (timeframe-sensitive)?
- [ ] Walk-forward window length vs. the signal's OWN expected trade
      frequency (from the brief's pre-registration, not a guess) — still long
      enough to hold a meaningful sample at the NEW timeframe?
- [ ] Minimum-trade / minimum-sample gates copied from a prior timeframe's
      protocol file — still reachable at the new bar frequency, for a signal
      with this expected trade count?

## 5. Zero data is not a finding

If a timeframe or config change makes the loader come back with zero bars,
the run must **raise** — never silently emit a route, a trial, or a
`no_signal` verdict from zero bars. `no_signal_artifact` means the signal did
not fire **on real data**; it must never share an output with "no data was
loaded at all."

## 6. Corrected status: `block_24_dense_fallback` (was "still open")

The old playbook said the `block_24_dense_fallback` label
(`episode_significance.py:209`) was "still open." **It is not — verified in
Linear**: CUL-51 is Done (merged via PR #76). Its sibling, the A8.6
power-gate per-timeframe block-size problem, is also Done (CUL-9). Treat
both as closed; if a future audit finds either regressed, that's a new
finding, not a reopening of these two.
