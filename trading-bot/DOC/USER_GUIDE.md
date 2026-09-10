# Trading Bot Engine — User Guide

Not sure this is the doc you need? See [`strategy-research/DOC_INDEX.md`](../../strategy-research/DOC_INDEX.md)
first — that file maps every doc in this monorepo by the question you arrived with.

This is a **capability reference**, not an engineering history or a forced-read
doc. It exists for a reader (human or a fresh agent) who wants to understand
what the `trading-bot/` engine currently does, from outside the day-to-day
workflow/engineering process. Written as Story S4 of Linear epic
[E-045](https://linear.app/culito/project/e-045-split-docs-into-forced-read-engineering-and-capability-reference-f5ccbab469f1)
("Split docs into forced-read, engineering, and capability-reference").

**Verification stance.** Every non-trivial claim below cites a `file:line` the
author actually read on this checkout (git SHA `d8379415`, branch
`fix/cul-275-mark-close-positions-tests-slow`, 2026-09-11). Several features
described in E-045's own addenda (gap-response tiers, the CUL-273 warmup/
required_bars sync, per-strategy `min_allocation_change`, the E-010 cost
model) are **real, tested, and reviewed, but not yet merged to this base** —
they live on named branches/commits. Those are called out explicitly as
"pending merge" wherever they appear, with the branch or commit they were
verified against, so this guide never blurs "will exist" with "exists now."

---

## Table of Contents

<!-- TOC:START -->
- [1. What This System Does](#1-what-this-system-does)
- [2. Config Retrieval](#2-config-retrieval)
- [3. Data Management](#3-data-management)
- [4. The Main Loop: Bar-by-Bar Processing](#4-the-main-loop-bar-by-bar-processing)
- [5. Warmup of the Strategy and Its Components](#5-warmup-of-the-strategy-and-its-components)
- [6. Update and Forecast Calculation](#6-update-and-forecast-calculation)
- [7. Allocation Calculation](#7-allocation-calculation)
- [8. Acceptance Check of Order (Risk Gate)](#8-acceptance-check-of-order-risk-gate)
- [9. Portfolio / Execution](#9-portfolio--execution)
- [10. Backtest Output / Artifacts](#10-backtest-output--artifacts)
- [11. Metrics Calculated](#11-metrics-calculated)
- [12. Known Documentation Discrepancies Found Writing This Guide](#12-known-documentation-discrepancies-found-writing-this-guide)
<!-- TOC:END -->

---

## 1. What This System Does

This is an automated crypto trading engine that runs one continuous
**forecast → allocation → rebalance** pipeline, identically in live and
backtest mode. Every time a candle closes for the traded symbol, the engine:
classifies the current market regime, combines a set of configured indicator
components into a single forecast in `[-20, +20]`, converts that forecast to
a target portfolio allocation in `[-1, +1]` (i.e. -100%..+100% of equity), and
either executes or rejects the rebalance needed to reach that target,
depending on a small set of risk controls. Live trading is explicitly
disabled by team convention (see `trading-bot/CLAUDE.fork.md` — "Never run
live") — this codebase is exercised almost exclusively through its backtest
path, `trading-bot/main.py simulate` or `core/launcher.py::run_backtest()`.

The strategy itself is entirely **config-driven**: `strategy_config.json`
declares the regime detector and the per-regime indicator ensembles as data,
not code, so a new strategy variant is normally a new config file, not a new
Python class.

---

## 2. Config Retrieval

Two separate JSON files drive the engine, loaded by two separate mechanisms:

### 2.1 `config.json` — runtime config

Loaded by `ConfigManager` (`trading-bot/config/settings.py:26-124`).
`Launcher.__init__` (`core/launcher.py:131-136`) calls
`initialize_config_and_logger()` (`core/launcher.py:58-74`), which builds a
`ConfigManager('config.json')`, calls `.validate()`, and — only if that
passes — builds the shared logger from `logging.file_path`/`logging.level`.
A validation failure exits the process (`sys.exit(1)`, `core/launcher.py:134`)
before anything else runs.

Sections actually present in the committed `config.json`
(`trading-bot/config.json`): `api` (Binance testnet keys, read via
`config/settings.py:1-18` from environment, not from this file), `trading`
(`symbols`, `interval`, `exchange`, `fetch_interval_seconds`,
`check_interval_seconds`, `test_mode`), `risk_management.controls`
(`max_allocation_change`, `min_allocation_change` — see §8), and `logging`
(`level`, `file_path`). `config.json:26-31` is the entire
`risk_management` block on this checkout — `portfolio_controls` (§8's
`PortfolioRiskGate`) is absent by default and therefore off.

`ConfigManager.validate()` (`config/settings.py:127-185`) currently checks:
symbols non-empty; `risk_management.portfolio_controls`, if present, passes
`validate_portfolio_controls()` (§8); and `trading.fetch_interval_seconds`, if
present, is `<= trading.interval` and divides it evenly (mirroring
`DataManager.__init__`'s own two `ValueError`s, §3, so a bad value fails at
config load rather than deep inside a `DataManager` construction).

### 2.2 `strategy_config.json` — regime detector + strategy components

Loaded directly by `AdvancedStrategy.__init__` (`strategies/main_strategy.py:17-32`)
— **not** through `ConfigManager` at all, and not automatically re-validated
at every load unless the caller does so: `AdvancedStrategy.__init__` calls
`tools.validate_config.validate(config)` itself (`main_strategy.py:28`) and
raises `ValueError("invalid strategy_config")` on any violation
(`main_strategy.py:29-32`). Two top-level keys are required:
`regime_detector` and `strategies`.

`tools/validate_config.py::validate()` currently implements checks **V1
through V10** (`tools/validate_config.py:53-278`; this checkout has no V11 —
see §12):

| Check | What it enforces |
|---|---|
| V1 | Top-level structure: `regime_detector`/`strategies` keys present; `strategies.regimes.*` is object or null |
| V2 | Every veto/rule-condition/score-component id is declared in `regime_detector.components` |
| V3 | Every `transforms`/`history_transforms` op exists in `TRANSFORM_OPS_REGISTRY` |
| V4 | Every used op has a `TRANSFORM_MIN_PERIODS` entry |
| V5 | No history-based op appears after a scalar/data-aware op in one transforms list |
| V6 | A component's explicit `lookback` override is `>=` the max transform `min_periods` it needs |
| V7 | Every regime name used anywhere is one of `{trending, mean_reversion, chop, unknown}` |
| V8 | Every strategy-engine component has a numeric `weight`; per-regime total weight `> 0` |
| V9 | `default_regime` may not alias `trending`/`mean_reversion`/`chop` while `rules` is non-empty (would silently bypass the regime gate) — except the fully-ungated pattern (`components: []` and `rules: []`) |
| V10 | A fully-ungated `regime_detector` must not point `default_regime` at a null `strategies.regimes` entry (would forecast 0.0 forever with no error) |

Both `V9`'s and `V10`'s "fully ungated" exemption is a deliberately supported
config pattern for a strategy with no regime gate at all (see
`tools/validate_config.py:204-257` and `tests/test_ungated_config_pattern.py`).

**Pending, not yet merged (E-055,** `feat(E-055)` **commit** `e756614a` **on
branch** `fix/cul-275-mark-close-positions-tests-slow` **as of this checkout's
own local history, ahead of the worktree HEAD used for this guide):** a new
**V11** validates `strategies.min_allocation_change`, if present, as a
non-negative number (`git show e756614a:trading-bot/tools/validate_config.py`,
new block after the current V8). See §8 for what it does.

---

## 3. Data Management

### 3.1 `DataManager` / `CandleBuilder` — live vs. backtest paths

`CandleBuilder` (`data/data_manager.py:405-638`) is the single OHLCV
aggregation engine, used identically by both paths — it "knows nothing about
auxiliary feeds" (`data_manager.py:409`). It is fed differently per mode:

- **Live:** `DataManager._rest_price_fetcher()` polls Binance REST
  (`data_manager.py:1370-1396`) and pushes `PriceTick`s onto a queue;
  `live_main_candle_processing_loop()` drains the queue and calls
  `CandleBuilder.add_tick()` (`data_manager.py:1407-1434`, `435-442`).
- **Backtest:** `DataManager._process_backtest_tick()` feeds the historical
  DataFrame row at the current cursor into `CandleBuilder.add_row()`
  (`data_manager.py:1455-1463`, `444-462`) — it uses `close` as the ingested
  price specifically "to avoid look-ahead bias on entries decided at bar
  close" (`data_manager.py:448-449`).

Both converge on `_ingest()` (`data_manager.py:506-556`), which opens a new
candle on the first tick for a symbol, updates the running candle while
`elapsed < interval_seconds`, and — once `elapsed >= interval_seconds` —
closes the candle, fires `candle_completion_callback` synchronously, and
opens the next one. `_align()` (`data_manager.py:610-638`) floors every
timestamp to its interval boundary via explicit UTC epoch integer division
(a deliberate fix for a real, previously-shipped bug: naive
`datetime.timestamp()` silently used the *local* timezone, which broke daily
candle alignment on a non-UTC host — see the comment at
`data_manager.py:617-632` and `tests/test_funding_rate_component.py`).

### 3.2 Fetch-timeframe vs. trade-timeframe (`fetch_interval_seconds`, CUL-250)

`CcxtFetcher.cache_key(symbol)` (`data/fetchers/ccxt_fetcher.py:101-124`)
returns `"{prefix}{symbol}_{ccxt_timeframe}"` (e.g. `BTCUSDT_1h`,
`kraken_BTCUSD_4h`) — the cache is keyed at the **exact timeframe the
fetcher was constructed with**, not at the strategy's candle interval. On its
own that would mean a 4h backtest strictly requires a `BTCUSDT_4h.csv` cache
to exist.

**This gap is now closed** (CUL-250, confirmed present on this checkout, not
just "landed elsewhere"): `DataManager.__init__` accepts an independent
`fetch_interval_seconds` (`data_manager.py:706-760`) — when set, OHLCV is
fetched/cached at *that* resolution and `CandleBuilder` aggregates the finer
rows up to the strategy's `interval_seconds` during replay (e.g.
`fetch_interval_seconds=3600` with `interval_seconds=14400` backtests a 4h
strategy off an hourly cache, `data_manager.py:721-733`). `DataManager`
raises `ValueError` if `fetch_interval_seconds > interval_seconds` or does
not divide it evenly (`data_manager.py:746-760`). It is wired end to end:
`config.json`'s `trading.fetch_interval_seconds` →
`Launcher._read_trading_params()` (`core/launcher.py:175-186`) →
`TradingParams.fetch_interval` → `DataManager(fetch_interval_seconds=...)`
(`core/launcher.py:210-215`), and independently as a `run_backtest()`
keyword for research callers (`core/launcher.py:657-666`, `697-703`). A run
that uses this folds `fetch_interval_seconds` into its provenance config
(hash + manifest) precisely when it diverges from `interval_seconds`
(`core/backtester.py:452-470`), so a derived-timeframe run is distinguishable
from a native one.

**This corrects a claim in this repo's own root** `CLAUDE.md` **(the
"Architecture overview" section), which currently states there is "NO
fallback that reads a finer existing cache and aggregates up" and that a 4h
backtest "raises 'No historical data' instead" — that was true when it was
written (2026-09-03, before PR #133/CUL-250 shipped) but is stale now.** See
§12.

### 3.3 Auxiliary feeds — two distinct mechanisms

E-045's own addenda are explicit that these are two different things, and
this checkout's code confirms the split:

**(a) Which cache file gets read — `cache_key()` / `_validated_exchange()`.**
`core/launcher.py::_validated_exchange()` (`core/launcher.py:92-114`) is the
single choke point every venue string passes through: it checks the string
against `ccxt.exchanges` and `sys.exit(1)`s loudly on a typo rather than
letting it silently reach `CcxtFetcher`, which would log, leave its client
`None`, and surface far later as an empty DataFrame ("No data",
`core/launcher.py:99-101`). The docstring is explicit that this names "the
venue whose PRICE CACHE the backtest engine resolves... not the venue orders
would be sent to" (`core/launcher.py:163-166`). The validated exchange id
becomes part of the cache filename for both price data
(`CcxtFetcher.cache_key()`, `ccxt_fetcher.py:101-124`) and, independently,
for `FundingRateFetcher.cache_key()`. Binance stays unprefixed for backward
compatibility with every cache file written before multi-venue support
existed; any other exchange gets an `{exchange}_` prefix
(`ccxt_fetcher.py:115-124`).

**(b) How aux data lands on the candle grid — `register_feed()` /
`_premerge_aux_feeds()`.** `DataManager.register_feed()`
(`data_manager.py:804-863`) attaches a `BaseFetcher` under a column name,
with a **required** `window_seconds` causality declaration (no default — a
feed that doesn't declare it is a `TypeError` at registration,
`data_manager.py:849-855`) and an `agg` of `'last' | 'mean' | 'sum'`
(default `'last'`, validated at `data_manager.py:847-848`). In **backtest**
mode, `DataManager.initialize()` calls `_premerge_aux_feeds()`
(`data_manager.py:957-1091`) once per symbol, **before replay starts**: it
resamples the feed's raw readings to the strategy's own candle interval
(`.resample(f"{interval_seconds}s", origin="epoch")`, `data_manager.py:1062-1068`
— `origin="epoch"` deliberately matches `CandleBuilder._align()`'s own epoch
floor, so aux bucket boundaries can never silently drift out of phase with
price bar boundaries on an interval that doesn't divide a day evenly,
`data_manager.py:1047-1061`), then `merge_asof(direction='backward')`s the
resampled series onto the price DataFrame via
`_merge_asof_with_causality_guard()` (`data_manager.py:350-398`). That guard
raises `AuxFeedCausalityError` if any matched row's declared source window
would end **after** the bar it's being attached to — i.e. it refuses to
attach a value the strategy could not yet have had (`data_manager.py:291-317`,
`383-397`). This whole mechanism is **explicitly backtest-only, one-shot batch
precompute**: live mode instead polls each feed on its own background thread
(`_aux_feed_poll_loop()`, `data_manager.py:1336-1368`) and broadcasts the
latest polled value as a constant column at candle close
(`_attach_aux_columns()`, `data_manager.py:934-937`) — a structurally
different, incremental mechanism, tracked as a known future gap in CUL-254.

**Production feed registry.** `data/feed_registry.py::FEED_REGISTRY`
(`feed_registry.py:42-51`) currently registers exactly two feeds,
`funding_rate` and `fear_greed`, both `window_seconds=0` (instantaneous,
published *at* their timestamp, no forward window,
`feed_registry.py:69-72`) — this is why `agg='last'` is correct-by-design
for both (confirmed: `FundingRateMeanReversionComponent` only reads at
settlement boundaries; `fear_greed` prints once daily). A **second**,
deliberately unmerged registry, `RESERVED_FEED_REGISTRY`
(`feed_registry.py:74-121`), holds six whale-footprint columns gated behind
an explicit opt-in and `campaign_data_policy.yaml` — being listed there is
"only the wiring," not a release (`feed_registry.py:74-95`). Those feeds
declare `window_seconds = DEFAULT_BAR_SECONDS` (a genuine forward window,
not instantaneous), which is why `agg='last'` would be a **currently-dormant
latent gap** if one were ever registered at a native granularity finer than
its consuming strategy's candle interval (tracked as CUL-253 — not yet
triggered because no whale feed is in the default registry).

`BacktestEngine.load_data()`'s **V1 registration guard**
(`core/backtester.py:189-205`) raises `FeedRequirementError` before any fetch
if the strategy's `required_feeds` (declared per-component via
`consumes_feeds`, aggregated by `AdvancedStrategy.required_feeds`,
`main_strategy.py:100-110`) are not present in the feed set the caller is
about to register — configuration is intent, so a component declared under
any regime requires its feed even if that regime never activates in a given
run.

---

## 4. The Main Loop: Bar-by-Bar Processing

`TradingBot._process_symbol_candle_completion()`
(`core/trading_bot.py:184-366`) is the one method both live and backtest
share (`BacktestEngine` extends `TradingBot` and reuses it unchanged). Per
completed candle, in order:

1. **Fetch enriched history.** `data_manager.get_data_history(symbol, count=1)`
   (`trading_bot.py:203`) — OHLCV plus any aux columns (§3). An empty frame
   logs a warning and returns without touching portfolio state
   (`trading_bot.py:205-207`).
2. **Warmup-only short-circuit.** If `warmup_cutoff_timestamp` is set and
   this bar is before it, `strategy.update(data)` runs (so indicators are
   primed) and the method returns — no trade, no portfolio-state record
   (`trading_bot.py:215-217`). Default `None` means every bar always trades,
   byte-identical to before this mechanism existed
   (`core/backtester.py:78-84`).
3. **Read balances, mark to market.** `portfolio_info.get_account_balance()`
   then `_calculate_total_portfolio_value(balances, close)`
   (`trading_bot.py:222-236`).
4. **Optional funding accrual** (`model_funding`, off by default,
   `trading_bot.py:231-234`) — charged on the position **held into** this
   bar, using this bar's close as mark, before the rebalance below.
5. **Optional `PortfolioRiskGate.observe()`** (§8, off by default,
   `trading_bot.py:244-245`) folds this bar's decision-time equity into any
   stateful drawdown/daily-loss tracking, before the forecast is even
   computed.
6. **Compute previous (actual) allocation**
   (`portfolio_info._calculate_actual_allocation`, `trading_bot.py:247`).
7. **Update strategy, generate signal.** `strategy.update(data)` then
   `strategy.generate_signals()` (`trading_bot.py:250-251`) — see §5/§6.
8. **Forecast → allocation.** `forecast_manager.forecast_to_allocation(signal.forecast)`
   (`trading_bot.py:255`) — see §7.
9. **Optional `PortfolioRiskGate.apply()`** (§8, off by default,
   `trading_bot.py:264-265`) clamps/overrides the target allocation.
10. **Allocation delta.** `forecast_manager.calculate_allocation_change(target, previous)`
    (`trading_bot.py:267`).
11. **The only drift check that gates a trade attempt at all** is
    `if abs(allocation_change) != 0.0` (`trading_bot.py:305`) — but see §8:
    this is **not** the only gate on whether the trade is *approved*.
    Whenever the risk gate is latched flat (killed or daily-halted), the
    forced flatten instead bypasses `approve_allocation_change` entirely and
    goes straight to `_execute_portfolio_rebalance`
    (`trading_bot.py:283-303`) — the same direct-execute path
    `_close_all_positions_at_end` uses, so a residual position smaller than
    the min-Δ band can still be force-closed.
12. **Risk-manager approval** (§8) then execution
    (`execution_handler._execute_portfolio_rebalance`, §9,
    `trading_bot.py:305-328`).
13. **Record bar state** into `portfolio_state_tracker`
    (`trading_bot.py:340-360`) — one row per bar, later written to
    `portfolio_states.csv`/`bars.csv` (§10).

At shutdown (live `stop()`, or end of a backtest run),
`_close_all_positions_at_end()` (`trading_bot.py:401-493`) force-flattens any
still-open position through the same direct execution path, and merges its
post-close numbers onto the same bar's already-recorded row rather than
appending a second row for the same instant (`replace_if_same_bar`,
`execution/portfolio_info.py:429-490`).

### 4.1 Gap detection and gap-response tiers — **pending merge**

Verified on branch `fix/cul-273b-reindex-wiring-and-standardization-nan`
(commits `45020746` CUL-261, `badd45ef` CUL-271, `5923aaa4`/`81802278`
CUL-273/273b), **not present on this guide's base checkout** — grepping this
worktree for `gap_detection`/`gap_policy`/`_check_and_record_gap` returns
nothing. Described here because it is real, tested, and directly relevant to
how the engine is meant to behave once merged:

`TradingBot._check_and_record_gap(symbol, data_time)` runs on every candle
completion (both live and backtest) when `gap_detection=True` (off by
default). It compares this candle's timestamp to the immediately preceding
one for the same symbol; any delta other than exactly one
`candle_interval_seconds` step is recorded as a gap. When `gap_policy` is
also set (`{"ignore_max_bars": int, "large_min_bars": int}`),
`_classify_gap_tier(bars_missing)` sorts each gap into one of three tiers:

- **ignore** (`bars_missing <= ignore_max_bars`) — no special handling;
  trading resumes on the next real bar.
- **middle** — the existing position is kept, but a *new* entry (flat →
  nonzero) is blocked until `bars_since_gap >= strategy.required_bars`, so
  the contaminated rolling windows have time to flush with real post-gap
  data. Rolling windows still span the gap itself by design — full
  segment-and-re-warm was tried and rejected on the research side of this
  repo (it destroyed 91% of a real sample) — so only *new* risk is withheld,
  not existing exposure.
- **large** (`bars_missing >= large_min_bars`) — immediate forced flatten via
  the same direct-execute bypass the risk-gate kill-switch uses, plus
  `AdvancedStrategy.reset_history()` (§5) — a genuine segment split that
  clears `data_buffer` and both engines' component history so the strategy
  re-warms from scratch on real post-gap bars. No separate re-entry block is
  needed afterward: the ordinary `is_ready()`/`required_bars` gate already
  forces `forecast=0.0`/`NOT_READY` until enough real bars re-accumulate.

Worked example (from the branch): `candle_interval_seconds=3600`,
`ignore_max_bars=2`, `large_min_bars=24`. A gap of 5 missing hourly bars is
"middle" — position held, new entries blocked until 24+ real bars have
passed since. A gap of 30 missing bars is "large" — immediate flatten plus
full re-warm.

---

## 5. Warmup of the Strategy and Its Components

`AdvancedStrategy.is_ready()` (`strategies/main_strategy.py:81-98`) is an AND
of three gates, evaluated in this order:

1. `self.data_buffer.size < self.required_bars` → not ready
   (`main_strategy.py:82-84`). `data_buffer` is a `RollingBuffer`
   (`strategy_base.py:381-421`) sized `required_bars + 100`
   (`main_strategy.py:46`).
2. `self.regime_engine.is_ready()` → not ready (`main_strategy.py:85-87`).
   For `threshold_rules` mode this means every detector-component history has
   `len >= 1`; for `score`/`score_product` mode every history must be full to
   its `lookback` (`strategies/regime_engine.py:91-94`).
3. The **current** bar's regime is classified first (`self._classify_once()`,
   `main_strategy.py:88-94`, `72-79`) — a deliberate ordering fix (labeled
   "F7" in the code) so `strategy_engine.is_ready(regime)` checks readiness
   for the regime this bar just resolved to, not last bar's regime (which,
   on the very first ready-candidate bar, would otherwise be the
   `MarketRegime.UNKNOWN` class-init default and vacuously "ready" for any
   regime with no components registered under that key).
   `ConfigDrivenStrategyEngine.is_ready(regime)`
   (`strategies/strategy_engine.py:84-91`) requires every component history
   deque *for that regime* to have `len >= self._warmup`.

`required_bars = max(regime_engine.get_required_periods(),
strategy_engine.get_required_periods(), 24)` (`main_strategy.py:39-44`) — the
`24` is the hardcoded `stddev_24` period the data buffer also computes as a
lazy calculated column (`main_strategy.py:47-49`).

**A currently-real drift between `required_bars` and the strategy engine's
own internal `_warmup`.** On this checkout,
`ConfigDrivenStrategyEngine.__init__` derives `_warmup` independently from
its own local config — `min(config.get("warmup", self.lookback), min_buf)`
(`strategy_engine.py:65-70`) — **not** from `AdvancedStrategy.required_bars`
at all. There is no `set_warmup()` call anywhere in `main_strategy.py` on
this checkout (confirmed by reading the whole file). This means the two
numbers can genuinely disagree depending on `strategy_config.json`'s own
`strategies.warmup` key versus the `required_bars` the readiness gate above
actually enforces.

**Pending merge (CUL-273, verified on** `fix/cul-273b-reindex-wiring-and-standardization-nan`**,
commit** `5923aaa4`**):** `required_bars` is computed, then immediately
followed by `self.strategy_engine.set_warmup(self.required_bars)`, making
`required_bars` the single source of truth for `_warmup` (still capped at
the smallest per-component deque size, since warmup can never exceed what a
deque can hold). Until that lands, treat `_warmup` as config-derived and
`required_bars` as buffer-sizing-only — they are not guaranteed equal on
this base.

`AdvancedStrategy.reset_history()` — the method the gap-response "large" tier
(§4.1) relies on to force a full re-warm — **does not exist on this
checkout** either (grep for `reset_history` across `trading-bot/` returns
nothing). It ships alongside the CUL-271/273 gap-response work on the same
branch; when present, it clears `data_buffer`, both engines' component
history, and the memoized `_regime_classification`. It does **not** touch
`SubStrategyComponent.rolling_forecast`/`standardization_count` (§6) — those
attributes are unreachable dead-code state on the real call path, not a gap
in the reset.

---

## 6. Update and Forecast Calculation

The real, currently-executing call chain, traced directly (not from
comments, which describe a different, superseded mechanism — see below):

```
AdvancedStrategy.generate_forecast()             (strategies/main_strategy.py:137-153)
  -> regime, debug_regime = self._classify_once()       (regime_engine.classify(), regime_engine.py:109-136)
  -> forecast, debug_components = self.strategy_engine.forecast(regime)
                                                          (strategy_engine.py:108-133)
       -> for each component in regimes[regime].components:
            h = self._history[regime.value][component_id]   (deque, populated by update())
            value = apply_transform_pipeline(pd.Series(h), c["transforms"], self._data)
                                                          (strategies/registry.py:90-112)
            ensemble += (weight / total_weight) * value
       -> return clip(ensemble, -20.0, 20.0)             (np.clip, strategy_engine.py:133)
```

`ConfigDrivenStrategyEngine.update()` (`strategy_engine.py:72-82`) runs
**every** component in **every** regime unconditionally each bar — not just
the active regime's — so inactive-regime histories stay warm across a
regime switch (see `DOC/STRATEGY_FRAMEWORK.md` invariant #8, re-verified
against this file directly). A component's raw value is appended to its
regime/component history only once that component's own `is_ready()` fires
(`strategy_engine.py:77-82`); this is a length check, not a NaN check, so a
NaN-producing component's NaN values do get pushed into history once ready —
they are never filtered (`strategy_engine.py:77-82`, no guard present).
`history_transforms`, if declared on a component spec, run once **at append
time** and define what the deque actually stores (`strategy_engine.py:79-81`);
`transforms`, applied inside `forecast()`, run fresh every bar over the
stored history (`registry.py:90-112`). `apply_transform_pipeline` seeds
`value = history[-1]` and applies each op in order — history-based ops
(`identity`, `percentile`, `negate_percentile`, `zscore`, `ratio_to_mean`,
`ema`) recompute from the full history and discard the accumulated `value`;
scalar/data-aware ops (`scale`, `threshold_filter`, `clip`, `sigmoid`,
`negate`, `vol_normalize`, `vol_adjusted`, `price_normalized`,
`volume_filter`) operate on it — 15 ops total in
`TRANSFORM_OPS_REGISTRY` as read on this checkout (`registry.py:51-87`).

`ConfigDrivenRegimeEngine.classify()` (`strategies/regime_engine.py:109-136`)
evaluates vetoes first (unconditionally, regardless of mode) — a veto that
fires for `consecutive_bars` in a row force-sets the regime and returns
immediately (`regime_engine.py:117-126`) — then dispatches to
`threshold_rules` (priority-ordered if/else over the latest raw component
values, `regime_engine.py:141-146`), `score` (weighted transformed
components, argmax with a minimum score and margin,
`regime_engine.py:173-193`), or `score_product` (multiplicative variant,
`regime_engine.py:198-218`), selected by `regime_detector.mode`.

### 6.1 A documentation trap: describe this, not the dead mechanism

Root `CLAUDE.md`'s own "Strategy hierarchy" section (and, more broadly,
prose elsewhere in this repo describing a "raw forecast is normalized by
`stddev_24 * close`... then scaled so the mean or target quantile maps to
±10" mechanism) describes `SubStrategyComponent.generate_forecast()` /
`.standardize_forecast()` / `.store_raw_forecast()`
(`strategies/strategy_base.py:116-196`) — **this is not what runs**.
Confirmed independently three ways on this checkout:

1. A literal grep for `CompositeStrategy(` (the only class whose
   `generate_forecast()` calls a component's `generate_forecast()`,
   `strategy_base.py:241-259`) across the entire tree returns **zero
   instantiations** — only its own class definition
   (`strategy_base.py:197`).
2. `AdvancedStrategy.__init__` builds `ConfigDrivenRegimeEngine` and
   `ConfigDrivenStrategyEngine` directly (`main_strategy.py:36-37`); neither
   of those classes references `SubStrategyComponent.generate_forecast`,
   `.standardize_forecast`, or `.store_raw_forecast` anywhere.
3. `strategies/registry.py::TRANSFORM_OPS_REGISTRY` is a fixed dict of
   plain lambdas with no `self`/component-instance access
   (`registry.py:51-87`) — nothing there could reach the dead methods
   dynamically either.

`SubStrategyComponent.generate_forecast()` et al. remain in the tree,
unused. Whether to delete them is a separate cleanup decision (tracked as
CUL-281 in the E-045 addenda) — out of scope for this guide.

---

## 7. Allocation Calculation

`ForecastManager` (`execution/forecast_manager.py:21-71`) is stateless —
`__init__` takes no arguments (`forecast_manager.py:41-42`). Two pure
functions:

- `forecast_to_allocation(forecast)` = `forecast / 10.0`
  (`forecast_manager.py:44-58`, `FORECAST_FOR_100_INVESTMENT = 10.0`,
  `forecast_manager.py:19`) — maps the `[-20, +20]` forecast range to a
  `[-2.0, +2.0]` target allocation (a forecast of ±10 is ±100% of equity;
  the clip to `[-20,+20]` upstream means the realistic target range is
  `[-2.0, +2.0]`, i.e. up to 2x leverage, before any risk-manager cap is
  applied — see §8).
- `calculate_allocation_change(target, current)` = `target - current`
  (`forecast_manager.py:60-71`).

**The docstring on this checkout is stale, and this is a live, verified
discrepancy worth flagging (see §12): it currently claims "NO DRIFT
THRESHOLD LIVES HERE, and none lives anywhere else either"
(`forecast_manager.py:30-38`). That is false, and has been false since
before this checkout — `RiskManager._ctrl_min_allocation_change`
(`risk/risk_manager.py:48-51`) already rejects any rebalance where
`abs(allocation_change) < risk_management.controls.min_allocation_change.threshold`
(`config.json:26-30`, default `0.2`) — see §8.** A pending, not-yet-merged
commit (`e756614a`, E-055) corrects this exact docstring and adds the
per-strategy override described in §8.

---

## 8. Acceptance Check of Order (Risk Gate)

Two independent risk layers exist. Only the first is on by default.

### 8.1 `RiskManager` — the per-trade allocation-change band (always active)

`RiskManager.approve_allocation_change(symbol, change, data)`
(`risk/risk_manager.py:16-52`) iterates `self.controls` (from
`config.json`'s `risk_management.controls`, `core/launcher.py:143-145`) and,
for each control name present, calls `self._ctrl_{name}` if it exists
(`risk_manager.py:27-40`) — an unrecognized control name is silently
skipped, not an error. Two controls are wired on this checkout:

- `_ctrl_max_allocation_change` (`risk_manager.py:42-46`): rejects if
  `abs(change) > controls.max_allocation_change.max + 1e-6`. Committed
  value: `4.0` (`config.json:28`).
- `_ctrl_min_allocation_change` (`risk_manager.py:48-51`): rejects if
  `abs(change) < controls.min_allocation_change.threshold - 1e-6`.
  Committed value: `0.2` (`config.json:29`).

So the band is `0.2 <= |Δ| <= 4.0` on the committed config — matching the
architecture-map claim in `CLAUDE.fork.md` ("risk checks (only 0.2 ≤ |Δ| ≤
4.0)"), **but contradicting root `CLAUDE.md`'s "There is no drift gating"
claim** (§7, §12). Rejection just logs and skips the rebalance for that bar
(`trading_bot.py:330-331`) — the position is simply left where it was.

**Pending merge (E-055, commit `e756614a` — real, tested, not on this
checkout's base):** `strategy_config.json` gains a top-level
`strategies.min_allocation_change` key. When set, `core/launcher.py`'s
`_build_risk_and_forecast_managers()` replaces only the
`min_allocation_change` sub-dict of `controls_cfg` before constructing
`RiskManager` — `max_allocation_change` and any other control pass through
untouched (`git show e756614a` diff to `core/launcher.py`). Absent (the
default) is byte-identical to current behavior. Verified on that commit:
fast tests 10/10, slow bit-identity 8/8, and threshold `0.2`/`0.02`/`1.5`
distinguishably produced `46`/`53`/`44` approved rebalances on the reference
window. `tools/validate_config.py`'s pending V11 (§2.2) validates this key
is a non-negative number.

### 8.2 `PortfolioRiskGate` — portfolio-level controls (off by default)

`risk/portfolio_risk_gate.py:146-335` implements three additional,
independently-configurable controls, built only when
`config.json`'s `risk_management.portfolio_controls` is a non-empty dict
(`core/launcher.py:154-155`; **absent on the committed config.json**, so this
gate is `None` and every one of the following is inert by default):

- **`absolute_allocation_cap`** — stateless: clamps the target allocation to
  `[-cap, +cap]` (`portfolio_risk_gate.py:302-304`).
- **`max_drawdown_kill`** — stateful, terminal: tracks the running peak of
  decision-time equity; once drawdown `>= threshold` it **latches** for the
  rest of the run, forcing the target to `0.0` every subsequent bar
  (`portfolio_risk_gate.py:240-249`, `299-301`). Un-latching requires a
  fresh run.
- **`daily_loss_limit`** — stateful, day-scoped: anchors day-start equity per
  a configurable timezone (default `Europe/Paris`, tz-aware, derived from
  the UTC bar timestamp); once intraday loss `>= threshold` it halts for the
  remainder of that calendar day and re-arms at the next midnight rollover
  with a fresh anchor (`portfolio_risk_gate.py:251-273`).

Validated by `validate_portfolio_controls()` (`portfolio_risk_gate.py:81-143`)
— shared by both `ConfigManager.validate()` (the `config.json` path) and
`run_backtest()`'s `risk_controls` override — unknown keys and out-of-range
values (thresholds must be finite numbers in `(0, 1)`) fail loud rather than
silently arming or skipping a control.

When active, the gate composes with `TradingBot._process_symbol_candle_completion()`
as described in §4: `observe()` runs before the forecast is computed,
`apply()` runs after the target allocation is derived but before the
allocation delta, and a latched-flat gate bypasses `RiskManager` entirely via
the same direct-execute path the end-of-run force-close uses
(`trading_bot.py:283-303`) — otherwise the `0.2` min-Δ band would block a
small residual position from ever fully flattening.

### 8.3 Gap-response tiers as a third layer — pending merge

See §4.1. Once merged, the "middle" tier blocks new entries and the "large"
tier forces an immediate flatten composed the same way the `PortfolioRiskGate`
latch is — both act on `target_allocation` before `allocation_change` is
derived, so whichever fires, the delta is computed consistently
(verified on `fix/cul-273b-reindex-wiring-and-standardization-nan`).

---

## 9. Portfolio / Execution

`BaseExecutionHandler` (`execution/execution_handler.py:30-149`) contains
all orchestration shared by `ExecutionHandler` (live, Binance margin API) and
`MockExecutionHandler` (backtest simulation) — subclasses implement only
three primitives: `open_long_position`, `open_short_position`,
`close_position`, each returning `(success: bool, debug: dict)`.
`_execute_portfolio_rebalance()` (`execution_handler.py:45-64`) dispatches to
`_handle_allocation_change()` (`execution_handler.py:66-94`), which either
routes through `_execute_position_transition()` (a sign flip — short/neutral
to long/neutral or vice versa, close-then-open, `execution_handler.py:96-125`)
or a simple add/reduce of the existing position.

`MockExecutionHandler.open_long_position()` / `open_short_position()` /
`close_position()` (`execution_handler.py:280-325`) fill at the bar's raw
`close` price — **there is no slippage model in this checkout's execution
path.** Cost enters only through `CommonPortfolioDef.update_local_balance()`'s
flat `commission_rate` (`execution/portfolio_info.py:85-202`, default
`0.001` i.e. 10bps, `DEFAULT_COMMISSION_RATE` in
`performance/metrics.py:40`), applied identically to every trade regardless
of symbol or venue.

**Pending merge (E-010 S3, commit `5846dd3d` on branch
`feat/e010-s3-real-slippage-defaults` — real, tested, not on this
checkout):** `config/cost_model.py::resolve_cost_model(exchange, market_type,
symbol=None)` resolves `(fee_bps, slippage_bps)` from
`config/cost_model.json`, keyed by `(exchange, market_type)` with a
per-symbol `slippage_bps` map (mandatory `"default"` fallback key — a
missing symbol falls back to the venue's conservative default, logged loudly
so a fallback estimate never silently reads as calibrated,
`resolve_cost_model` docstring). An unconfigured `(exchange, market_type)`
combination raises `UnknownCostModelError` rather than defaulting — deny by
default, matching this project's general convention. Calibrated defaults on
that commit: binance/margin `{BTCUSDT: 1bps, ETHUSDT: 1.5bps, default:
1.5bps}`; kraken/futures `{BTCUSD: 2.5bps, ETHUSD: 4bps, AVAXUSD/SOLUSD:
7.5bps, default: 7.5bps}`. `MockExecutionHandler` on that branch resolves
slippage per symbol at fill time instead of a flat float threaded in at
construction; `core/backtester.py` folds the effective cost model into run
provenance (`config_sha256`) unconditionally, closing a gap where two runs
could otherwise share config/data/git hashes yet differ in cost economics
purely because `cost_model.json` changed between them. Declared default-
behavior change on that commit: real slippage went from 0bps to
BTCUSDT=1bps, moving the reference anchor from `net_pnl -231.758912` to
`-238.279247` (trade count unchanged at 24).

`MockPortfolioInfo`/`PortfolioInfo` (both extend `CommonPortfolioDef`,
`execution/portfolio_info.py:85-379`) track balances as a flat
`{asset: {free, locked}}` dict; `update_local_balance()`
(`portfolio_info.py:89-202`) applies the trade and commission per
`trade_type` (`LONG`/`SHORT`/`REDUCE_LONG`/`REDUCE_SHORT`/`CLOSE`), including
margin-borrow bookkeeping for a buy that exceeds free USDT. `apply_funding()`
(`portfolio_info.py:204-251`) is the separate, off-by-default perpetual-
funding cash-flow accrual described in §4 step 4 — pure USDT-balance
mutation, independent of the trade path and never interacting with
commission. `PortfolioStateTracker.record_state()`
(`portfolio_info.py:429-490`) appends one row per bar (merging rather than
duplicating a row when `replace_if_same_bar` fires at end-of-run, as
described in §4).

---

## 10. Backtest Output / Artifacts

Every backtest writes to `results/runs/<UTC-timestamp>_<config-sha8>/`
(`reporting/run_artifact.py::new_run_dir`, `run_artifact.py:26-33`) — or, for
research callers that pass `runs_root`, directly under that root without a
`runs/` subdirectory. `<config-sha8>` is the first 8 hex chars of a SHA-256
over the canonicalized (sorted-keys) provenance config
(`run_artifact.py:27-28`), the same `_provenance_config` that folds in
`model_funding`/`fetch_interval_seconds`/cost-model provenance when they
diverge from their defaults (`core/backtester.py:427-470`, §3.2).

Files written (`reporting/run_artifact.py`, `trading-bot/DOC/RUN_ARTIFACT.md`
— re-verified against the writer functions directly):

- **`manifest.json`** (`write_manifest`, `run_artifact.py:66-99`) —
  `run_id`, `created_utc`, the full `config` snapshot, `config_sha256`, a
  `data` block (`symbols`, `timeframe`, `start`, `end`, `bar_count`,
  `data_sha256` — a hash over `timestamp,open,high,low,close,volume` only,
  `run_artifact.py:40-44`), `git_sha` (with a `-dirty` suffix if any
  **tracked** file differs from `HEAD`, deliberately ignoring the
  permanently-untracked `results/runs/` evidence dirs,
  `run_artifact.py:47-59`), and `engine.{lookback, warmup}` (read from
  `strategy.strategy_engine.lookback`/`._warmup`, `core/backtester.py:503-504`
  — so this field currently reflects the config-derived `_warmup`, not
  `required_bars`; see §5's pending CUL-273 note). An optional `feeds` block
  (registered/dropped/required feed names) is added only when a caller
  passed a non-`None` `drop_feeds` (`core/backtester.py:482-493`).
- **`metrics.json`** (`write_metrics_json`, `run_artifact.py:120-145`) —
  `core` (§11), `per_regime`, `forecast_bins`, `dynamic` (per-component
  per-regime mean/std), plus optional `regime_validity`, `bar_equity`, and
  `risk_controls` blocks, each present only when the corresponding
  off-by-default feature is enabled for that run.
- **`trades.json`** — one record per `CompletedTrade.to_dict()`
  (`run_artifact.py:106-113`; fields listed in §11).
- **`bars.csv`** — the full per-bar `portfolio_state_tracker` frame, rounded
  to 6 decimals (`write_bars_csv`, `run_artifact.py:152-153`), with
  dict-valued columns (like `debug_info.components.*`) flattened to
  dot-separated scalar columns first (`flatten_dict_columns`,
  `execution/portfolio_info.py:400-412`).
- **`forecast_distribution.csv`** — per-regime forecast histogram over 8
  fixed bins (`write_forecast_distribution`, `run_artifact.py:160-174`).
- **`tradesxl.xlsx`** — Excel mirror of `trades.json` plus a
  `Performance_Metrics` sheet with per-metric explanatory comments
  (`export_trades_to_excel`/`export_metrics_to_excel`, `performance/metrics.py:599-751`).
- **`portfolio_states.csv`** — written by `PortfolioStateTracker.to_csv()`
  into the same run directory (`core/backtester.py:561-564`) — the
  un-rounded twin of `bars.csv`, the input `performance/bar_equity.py`'s
  functions and `build_bar_equity()` (§11) actually consume.

---

## 11. Metrics Calculated

`EnhancedPerformanceTracker` (`performance/metrics.py:319-...`) matches
trade executions **LIFO** (Last-In-First-Out) inside
`_process_executed_trades()` (`metrics.py:437-570`): an opposite-direction
execution walks the open `Position`'s executions from most recent to oldest
(`metrics.py:466`), closing each in turn until the new execution's quantity
is fully matched, producing one `CompletedTrade` per match
(`metrics.py:520-527`); any quantity left over after the whole position is
closed becomes a **reversal** — a brand-new position in the opposite
direction (`metrics.py:545-564`).

`CompletedTrade` (`metrics.py:121-317`) exposes, among others:
`profit_loss_percent`/`profit_loss_absolute` (gross), `entry_commission` /
`exit_commission` / `total_commission` (fee-tier-aware: whether the fee is
deducted from the received or the quote asset depends on LONG vs. SHORT and
entry vs. exit, `metrics.py:181-203`), `net_profit_loss_percent`
/`net_profit_loss_absolute`, `net_portfolio_profit_loss_percent` (impact on
total equity, not just the trade's own return), `duration_minutes`, and
`entry_forecast`/`entry_regime`/`entry_confidence` (and the `exit_*` twins) —
carried straight from the `TradeExecution` that opened/closed the position.

**Trade-exit-basis Sharpe/drawdown** (`calculate_sharpe_ratio`/
`calculate_max_drawdown`, `metrics.py:1444-1499`, used by
`_calculate_standard_metrics` → `metrics.json`'s `core` block): both group
completed trades by **exit date**, reindex onto the full calendar from first
to last trade, and fill every non-trading day with a synthetic `0.0` return
(`metrics.py:1484-1487`) before computing an annualized (`sqrt(365)`) Sharpe
and a running-max drawdown over the compounded daily-return equity curve.
This means Sharpe/drawdown here sample only as many points as there are
distinct trade-exit days — 24 points on the committed reference window per
`CLAUDE.fork.md`'s own figures, re-derivable from `trades.json`'s trade
count on that window.

**Bar-level alternative** (`bar_equity`, off by default,
`performance/bar_equity.py` + `reporting/run_artifact.py::build_bar_equity`,
`run_artifact.py:341-419`): computed instead from the full per-bar
`postRebalance_total_value` series, **excluding** every bar whose `regime`
normalizes to `"NOT_READY"` (`run_artifact.py:377-378` — the same string
`MainStrategy.generate_signals()` emits at `strategy_base.py:349`, so a
warmup bar the strategy could not have acted on never dilutes the volatility
estimate). Every degenerate input here raises `ValueError` rather than
silently producing a wrong number: missing required columns, zero bars
surviving the warmup exclusion, NaN among the surviving bars, or a
non-finite `max_drawdown_pct` (`run_artifact.py:368-397`). Turnover is
computed from **executed** allocation deltas
(`postRebalance_current_allocation` vs. `previous_allocation`,
`run_artifact.py:406-408`), not the raw `allocation_change` field, which
also counts rejected rebalance attempts. Reference figures recorded at
`fix/metrics-bar-equity`'s merge (`CLAUDE.fork.md` backlog item 3): maxDD
−24.77 vs. trade-exit −24.59, Sharpe −5.12 vs. −5.65, Sortino −5.05
(downside deviation `sqrt(mean(min(r,0)^2))` over **all** daily returns
against a target of 0, not the sample std of negative days alone,
`run_artifact.py:413-418`).

### 11.1 A deliberate modeling decision: positions across a data gap

Not found in `trading-bot/` itself (it lives in
`strategy-research/tools/prescreen_signal.py::_compute_turnover_proxy`, part
of the research tooling that pre-screens signals before a full backtest),
but the E-045 epic explicitly asks that this be recorded here since it
directly affects how trade count and holding time should be interpreted
whenever a real data gap is present in a window: **a position held across a
real data gap is treated as closed and reopened, not continued** —
`_compute_turnover_proxy`'s `prev_sign` resets at the start of each
contiguous time segment. This is a genuine stance, not a forced correctness
fix (one could argue a position was economically still open through an
unobserved gap); the chosen stance *raises* the counted trade count and
*lowers* the reported average holding time across a gap, making the cost
hurdle more conservative. <!-- TODO: verify whether an equivalent segment-
reset exists anywhere in trading-bot/performance/metrics.py itself, or
whether this decision is currently scoped only to the research prescreen
tool — not fully confirmed this session. -->

---

## 12. Known Documentation Discrepancies Found Writing This Guide

Per this guide's own ground rules: where the same topic is described
differently elsewhere in this repo, the real, re-verified current behavior
is documented above; this section only names the discrepancy so nobody
mistakes it for something this guide broke.

1. **Root `CLAUDE.md`'s "Core flow" section claims a 4h backtest cannot run
   off a 1h cache** ("there is NO fallback that reads a finer existing cache
   and aggregates up"). **Stale as of this checkout.** CUL-250 (PR #133)
   added exactly that fallback — `DataManager(fetch_interval_seconds=...)`,
   confirmed present and wired end-to-end (§3.2). The root doc's own text
   dates itself to 2026-09-03, before the fix shipped later that day.
2. **Root `CLAUDE.md`'s "There is no drift gating" claim under "Key data
   structures"** ("the engine rebalances toward target on every bar
   whenever the delta is nonzero at all... `risk_management.rebalance_threshold`
   is dead"). **Confirmed false on this checkout, independent of any pending
   branch.** `RiskManager._ctrl_min_allocation_change` (`risk_manager.py:48-51`)
   already enforces a `0.2` minimum `|Δ|` via `config.json`'s
   `risk_management.controls.min_allocation_change` — a live, wired
   mechanism, distinct from the actually-dead `rebalance_threshold` key the
   doc correctly identifies as unused. `ForecastManager`'s own docstring
   (`forecast_manager.py:30-38`) currently repeats the same stale claim (see
   §7). Both are corrected by a pending, not-yet-merged commit (`e756614a`,
   E-055) — this guide describes the real current (pre-merge) behavior.
3. **Root `CLAUDE.md`'s "Strategy hierarchy" section** describes
   `WeightedComponentRegimeDetector`/`CompositeStrategy`/
   `SubStrategyComponent.generate_forecast()`/`.standardize_forecast()` as
   the live mechanism. **Confirmed dead** — see §6.1. This guide's own
   diagram (§6) is the real one.
4. **`trading-bot/DOC/STRATEGY_FRAMEWORK.md`** is, by contrast, accurate and
   consistent with everything re-verified for this guide (its per-bar data
   flow, readiness gating, and invariant list all matched the code read
   directly) — it should be treated as the more reliable of the two existing
   architecture docs until root `CLAUDE.md` is corrected (out of scope for
   this guide to fix).
5. **Component count.** `trading-bot/CLAUDE.fork.md`'s module map says "23
   components" (`strategies/strategy_components.py`). **Re-verified directly
   (`grep -c "^class.*SubStrategyComponent"`): the real count is 24**, not 23
   and not the 22 this guide's first draft reported (that draft's own grep
   pass undercounted by one). Both prior numbers were wrong; 24 is confirmed.
6. **`TRANSFORM_OPS_REGISTRY` op count.** An E-045 addendum (citing root
   `CLAUDE.md`) describes it as "a fixed dict of 14 named lambdas." **Re-verified
   directly: the real count is 15** (`strategies/registry.py:51-87`), matching
   this guide's own §6 body text. The exact count matters for anyone reasoning
   about "nothing else could reach the dead forecast-standardization methods
   dynamically" (§6.1)
   — re-verify the current count before repeating either number.

<!-- Fast suite re-run on this checkout after the first draft: 556 passed,
33 skipped, 47 deselected, 0 failed -- confirms nothing in this guide
contradicts the current test suite's actual behavior. This does not by
itself re-verify every specific byte-identity NUMBER cited above (§3.2, §7,
§9) -- those would need the named slow tests run individually with their
asserted values compared -- but it does rule out the broader risk that this
guide describes behavior the codebase's own tests disagree with. -->
