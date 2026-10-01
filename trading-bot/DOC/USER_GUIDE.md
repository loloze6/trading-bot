# Trading Bot Engine — User Guide

Not sure this is the doc you need? See [`strategy-research/DOC_INDEX.md`](../../strategy-research/DOC_INDEX.md)
first — that file maps every doc in this monorepo by the question you arrived with.

This is a **capability reference**, not an engineering history or a forced-read
doc. It exists for a reader (human or a fresh agent) who wants to understand
what the `trading-bot/` engine currently does, from outside the day-to-day
workflow/engineering process. Written as Story S4 of Linear epic
[E-045](https://linear.app/culito/project/e-045-split-docs-into-forced-read-engineering-and-capability-reference-f5ccbab469f1)
("Split docs into forced-read, engineering, and capability-reference").

**Verification stance.** Every non-trivial claim below cites a stable name —
a class/method/function, or a dotted config-key path for JSON files — that
the author actually confirmed on this checkout by opening the source (git SHA
`d8379415`, branch `fix/cul-275-mark-close-positions-tests-slow`, 2026-09-11,
updated 2026-09-11 to name-based citations). Citations deliberately omit line
numbers: they drift every time the cited file changes, while a symbol name
stays greppable and accurate for as long as the symbol exists. If a citation
is bare (just a file path, no `::Symbol`), the symbol is already named in the
adjacent prose — no need to repeat it. Several features described in E-045's
own addenda (gap-response tiers, the CUL-273 warmup/required_bars sync,
per-strategy `min_allocation_change`, the E-010 cost model) are **real,
tested, and reviewed, but not yet merged to this base** — they live on named
branches/commits. Those are called out explicitly as "pending merge"
wherever they appear, with the branch or commit they were verified against,
so this guide never blurs "will exist" with "exists now."

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
<!-- TOC:END -->

---

## 1. What This System Does

This is an automated crypto trading engine that runs one continuous
**forecast → allocation → rebalance** pipeline, identically in live and
backtest mode. Every time a candle closes for the traded symbol, the engine:
classifies the current market regime, combines a set of configured indicator
components into a single forecast in `[-20, +20]`, converts that forecast to
a target portfolio allocation in `[-2, +2]` (i.e. -200%..+200% of equity —
up to 2x leverage before any risk-manager cap, see §7), and either executes
or rejects the rebalance needed to reach that target,
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

**What it's for.** This file controls how the bot is *operated* — which
symbols and venue, what timeframe, how much the risk layer lets a single
rebalance move, where logs go — without touching code. It says nothing about
trading *logic*; that's `strategy_config.json` (§2.2).

Loaded by `ConfigManager` (`trading-bot/config/settings.py`).
`Launcher.__init__` (`core/launcher.py`) calls
`initialize_config_and_logger()` (`core/launcher.py`), which builds a
`ConfigManager('config.json')`, calls `.validate()`, and — only if that
passes — builds the shared logger from `logging.file_path`/`logging.level`.
A validation failure exits the process (`sys.exit(1)`, `core/launcher.py::Launcher.__init__`)
before anything else runs.

Sections actually present in the committed `config.json`
(`trading-bot/config.json`), and what each key concretely controls:

| Key | What it does |
|---|---|
| `api.key` / `api.secret` | Unused — real Binance keys come from environment variables, not this file (`config/settings.py`) |
| `trading.symbols` | Symbols to trade/backtest, e.g. `["BTCUSDT"]`. Must be non-empty |
| `trading.interval` | Candle size the strategy trades on, in seconds |
| `trading.check_interval_seconds` | Live mode only — how often to poll Binance for a price tick |
| `trading.test_mode` | `true` = Binance testnet, picks which API keys/base URL are used |
| `trading.exchange` | Optional, default `binance`. Which venue's price cache gets read (§3.3a) |
| `trading.fetch_interval_seconds` | Optional, default = `interval`. Fetch OHLCV finer than the trading timeframe and aggregate up (§3.2) |
| `risk_management.controls.max_allocation_change.max` | Largest single-bar allocation swing the risk manager approves (§8.1). Committed default `4.0` |
| `risk_management.controls.min_allocation_change.threshold` | Smallest allocation change worth acting on — anything smaller is skipped (§8.1). Committed default `0.2` |
| `risk_management.portfolio_controls` | Absent by default (off). Turns on the portfolio-level risk gate (§8.2): allocation cap, drawdown kill switch, daily loss limit |
| `logging.level` / `logging.file_path` | Log verbosity and log file destination |

`risk_management` is a small, entirely-committed block on this checkout.

**Not in this table: a `strategy` section also exists in the committed
file** (`max_abs_range_forecast`, `name`, `BuyAndHoldXPeriodsStrategy`,
`SimpleMovingAverageStrategy`) but is dead — no current code path reads it
(confirmed: zero hits for any of its keys under `core/`, `strategies/`,
`config/`, `execution/`, `data/`, or `main.py`). The strategy that actually
runs is entirely defined by `strategy_config.json` (§2.2), not this section.

`ConfigManager.validate()` (`config/settings.py`) currently checks:
symbols non-empty; `risk_management.portfolio_controls`, if present, passes
`validate_portfolio_controls()` (§8); and `trading.fetch_interval_seconds`, if
present, is `<= trading.interval` and divides it evenly (mirroring
`DataManager.__init__`'s own two `ValueError`s, §3, so a bad value fails at
config load rather than deep inside a `DataManager` construction).

### 2.2 `strategy_config.json` — regime detector + strategy components

**What it's for.** This file *is* the trading strategy — which indicators
feed which regime, how they combine into a forecast, what counts as
"trending" vs. "chop." Changing trading logic normally means editing this
file, not writing Python (§1). For a field-by-field guide to writing one,
see [`STRATEGY_DESIGN_GUIDE.md`](../../strategy-research/docs/STRATEGY_DESIGN_GUIDE.md) and
[`COMPONENT_CATALOG.md`](../../strategy-research/docs/COMPONENT_CATALOG.md).

Loaded directly by `AdvancedStrategy.__init__` (`strategies/main_strategy.py`)
— **not** through `ConfigManager` at all, and not automatically re-validated
at every load unless the caller does so: `AdvancedStrategy.__init__` calls
`tools.validate_config.validate(config)` itself (`main_strategy.py`) and
raises `ValueError("invalid strategy_config")` on any violation
(`main_strategy.py`). Two top-level keys are required:
`regime_detector` and `strategies`.

`tools/validate_config.py::validate()` currently implements checks **V1
through V10** (`tools/validate_config.py`; this checkout has no V11 yet —
see the pending-merge note below):

| Check | What it enforces (plain-language) |
|---|---|
| V1 | The file has both required sections (`regime_detector`, `strategies`), correctly shaped |
| V2 | Every indicator ID referenced by a veto or a rule is actually defined in the components list |
| V3 | Every transform name used (e.g. `zscore`, `clip`) is a real, known transform |
| V4 | Every transform used has a known minimum warmup length defined |
| V5 | Within one component, transforms that need history run before transforms that just tweak a single value |
| V6 | If a component sets its own lookback, it's long enough for the transforms it uses |
| V7 | Every regime name used anywhere is one of the four real regimes (`trending`, `mean_reversion`, `chop`, `unknown`) |
| V8 | Every strategy component has a numeric weight, and each regime's weights add up to something positive |
| V9 | The fallback regime can't quietly bypass the regime rules — unless there are no rules at all (the deliberate "no regime gate" pattern) |
| V10 | The fallback regime can't point at an empty strategy block, which would forecast 0 forever with no error |

Both `V9`'s and `V10`'s "fully ungated" exemption is a deliberately supported
config pattern for a strategy with no regime gate at all (see
`tools/validate_config.py::validate()` and `tests/test_ungated_config_pattern.py`).

**Pending, not yet merged (E-055,** `feat(E-055)` **commit** `e756614a` **on
branch** `fix/cul-275-mark-close-positions-tests-slow` **as of this checkout's
own local history, ahead of the worktree HEAD used for this guide):** a new
**V11** validates `strategies.min_allocation_change`, if present, as a
non-negative number (`git show e756614a:trading-bot/tools/validate_config.py`,
new block after the current V8). See §8 for what it does.

---

## 3. Data Management

### 3.1 `DataManager` / `CandleBuilder` — live vs. backtest paths

`CandleBuilder` (`data/data_manager.py`) is the single OHLCV
aggregation engine, used identically by both paths — it "knows nothing about
auxiliary feeds" (`data_manager.py`). It is fed differently per mode:

- **Live:** `DataManager._rest_price_fetcher()` polls Binance REST
  (`data_manager.py`) and pushes `PriceTick`s onto a queue;
  `live_main_candle_processing_loop()` drains the queue and calls
  `CandleBuilder.add_tick()` (`data_manager.py`).
- **Backtest:** `DataManager._process_backtest_tick()` feeds the historical
  DataFrame row at the current cursor into `CandleBuilder.add_row()`
  (`data_manager.py`) — it uses `close` as the ingested
  price specifically "to avoid look-ahead bias on entries decided at bar
  close" (`data_manager.py`).

Both converge on `_ingest()` (`data_manager.py`), which opens a new
candle on the first tick for a symbol, updates the running candle while
`elapsed < interval_seconds`, and — once `elapsed >= interval_seconds` —
closes the candle, fires `candle_completion_callback` synchronously, and
opens the next one. `_align()` (`data_manager.py`) floors every
timestamp to its interval boundary via explicit UTC epoch integer division
(a deliberate fix for a real, previously-shipped bug: naive
`datetime.timestamp()` silently used the *local* timezone, which broke daily
candle alignment on a non-UTC host — see the comment at
`data_manager.py` and `tests/test_funding_rate_component.py`).

### 3.2 Fetch-timeframe vs. trade-timeframe (`fetch_interval_seconds`, CUL-250)

`CcxtFetcher.cache_key(symbol)` (`data/fetchers/ccxt_fetcher.py`)
returns `"{prefix}{symbol}_{ccxt_timeframe}"` (e.g. `BTCUSDT_1h`,
`kraken_BTCUSD_4h`) — the cache is keyed at the **exact timeframe the
fetcher was constructed with**, not at the strategy's candle interval. On its
own that would mean a 4h backtest strictly requires a `BTCUSDT_4h.csv` cache
to exist.

`DataManager` closes that gap with an independent, optional
`fetch_interval_seconds` (`data_manager.py::DataManager.__init__`): when set, OHLCV is
fetched/cached at *that* resolution and `CandleBuilder` aggregates the finer
rows up to the strategy's `interval_seconds` during replay (e.g.
`fetch_interval_seconds=3600` with `interval_seconds=14400` backtests a 4h
strategy off an hourly cache, `data_manager.py::DataManager.__init__`). `DataManager`
raises `ValueError` if `fetch_interval_seconds > interval_seconds` or does
not divide it evenly (`data_manager.py::DataManager.__init__`). It is wired end to end:
`config.json`'s `trading.fetch_interval_seconds` →
`Launcher._read_trading_params()` (`core/launcher.py`) →
`TradingParams.fetch_interval` → `DataManager(fetch_interval_seconds=...)`
(`core/launcher.py::Launcher._build_mock_stack`), and independently as a `run_backtest()`
keyword for research callers (`core/launcher.py`). A run
that uses this folds `fetch_interval_seconds` into its provenance config
(hash + manifest) precisely when it diverges from `interval_seconds`
(`core/backtester.py::BacktestEngine._end_of_backtest`), so a derived-timeframe run is distinguishable
from a native one.

### 3.3 Auxiliary feeds — two distinct mechanisms

**What's an "aux feed"?** Any data column a strategy component can read
that *isn't* OHLCV price — e.g. the funding rate, or the Fear & Greed
index. These don't arrive in neat, bar-sized chunks the way price does
(funding updates every 8 hours; Fear & Greed once a day), so getting them
onto the engine safely raises two separate questions, handled by two
separate, unrelated pieces of code:

1. **Which file on disk has this data?** — a routing/caching question,
   answered once, before any bars are processed.
2. **Once we have the raw data, how do we attach it to the right price bar
   without ever letting a bar "see" a value it couldn't have known about
   yet (look-ahead bias)?** — a timing/alignment question, answered per bar.

A bug in one doesn't imply a bug in the other — which is also why the code
splits them into different functions, not because the code overcomplicates
a simple problem.

**(a) Which cache file gets read.** This is the same kind of question as
§3.2's exchange selection, just for a different data source.
`core/launcher.py::_validated_exchange()` (`core/launcher.py`) is the
single choke point every venue string passes through.

- It checks the string against `ccxt.exchanges` and `sys.exit(1)`s loudly on
  a typo, rather than letting it silently reach `CcxtFetcher` — which would
  just log, leave its client `None`, and surface far later as an empty
  DataFrame ("No data", `core/launcher.py`).
- The docstring is explicit that this names "the venue whose PRICE CACHE the
  backtest engine resolves... not the venue orders would be sent to"
  (`core/launcher.py::Launcher._read_trading_params`).
- The validated exchange id becomes part of the cache filename for both
  price data (`CcxtFetcher.cache_key()`, `ccxt_fetcher.py`) and,
  independently, for `FundingRateFetcher.cache_key()`. Binance stays
  unprefixed for backward compatibility with every cache file written before
  multi-venue support existed; any other exchange gets an `{exchange}_`
  prefix (`ccxt_fetcher.py::CcxtFetcher.cache_key`).

**(b) How aux data lands on the candle grid, without leaking the future.**
Every feed a component wants to use is registered once via
`DataManager.register_feed()` (`data_manager.py`), which attaches a
`BaseFetcher` under a column name. Registration forces the caller to
declare two things up front:

- A **required** `window_seconds` — how far forward from its timestamp a
  reading stays valid. There's no default; a feed that skips this is a
  `TypeError` at registration time (`data_manager.py`). This is the number
  the causality check below relies on.
- An `agg` of `'last' | 'mean' | 'sum'` (default `'last'`, validated at
  `data_manager.py`) — how to collapse multiple raw readings into one value
  per bar, if the feed publishes more often than the strategy trades.

In **backtest** mode, this all happens *before replay starts*, once per
symbol, via `DataManager.initialize()` calling `_premerge_aux_feeds()`
(`data_manager.py`) — a one-shot batch step, not something recomputed bar
by bar:

1. Resample the feed's raw readings onto the strategy's own candle interval
   (`.resample(f"{interval_seconds}s", origin="epoch")`, `data_manager.py` —
   `origin="epoch"` deliberately matches `CandleBuilder._align()`'s own
   epoch floor, so aux bucket boundaries can never silently drift out of
   phase with price bar boundaries on an interval that doesn't divide a day
   evenly, `data_manager.py`).
2. Merge that resampled series onto the price DataFrame, always looking
   backward in time (`merge_asof(direction='backward')`), via
   `_merge_asof_with_causality_guard()` (`data_manager.py`).
3. That guard is the actual look-ahead safeguard: it raises
   `AuxFeedCausalityError` if a matched reading's declared `window_seconds`
   would still be valid *after* the bar it's being attached to — i.e. it
   refuses to attach a value the strategy could not yet have had
   (`data_manager.py`).

**Live mode does this differently, on purpose.** There's no "before replay"
moment in live trading, so it can't precompute anything. Instead each feed
is polled continuously on its own background thread
(`_aux_feed_poll_loop()`, `data_manager.py`), and the most recent polled
value is broadcast as a constant column at candle close
(`_attach_aux_columns()`, `data_manager.py`). This is a structurally
different, incremental mechanism from the backtest path above — a known
gap tracked as CUL-254, not an oversight in this guide.

**Production feed registry.** `data/feed_registry.py::FEED_REGISTRY`
(`feed_registry.py`) currently registers exactly two feeds,
`funding_rate` and `fear_greed`, both `window_seconds=0` (instantaneous, no forward window,
`feed_registry.py::FEED_WINDOW_SECONDS`; fear & greed is used one day after its date,
`FEED_DELAY_SECONDS`, CUL-356) — this is why `agg='last'` is correct-by-design
for both (confirmed: `FundingRateMeanReversionComponent` only reads at
settlement boundaries; `fear_greed` prints once daily). A **second**,
deliberately unmerged registry, `RESERVED_FEED_REGISTRY`
(`feed_registry.py`), holds six whale-footprint columns gated behind
an explicit opt-in and `campaign_data_policy.yaml` — being listed there is
"only the wiring," not a release (`feed_registry.py`). Those feeds
declare `window_seconds = DEFAULT_BAR_SECONDS` (a genuine forward window,
not instantaneous), which is why `agg='last'` would be a **currently-dormant
latent gap** if one were ever registered at a native granularity finer than
its consuming strategy's candle interval (tracked as CUL-253 — not yet
triggered because no whale feed is in the default registry).

`BacktestEngine.load_data()`'s **V1 registration guard**
(`core/backtester.py`) raises `FeedRequirementError` before any fetch
if the strategy's `required_feeds` (declared per-component via
`consumes_feeds`, aggregated by `AdvancedStrategy.required_feeds`,
`main_strategy.py`) are not present in the feed set the caller is
about to register — configuration is intent, so a component declared under
any regime requires its feed even if that regime never activates in a given
run.

---

## 4. The Main Loop: Bar-by-Bar Processing

`TradingBot._process_symbol_candle_completion()`
(`core/trading_bot.py`) is the one method both live and backtest
share (`BacktestEngine` extends `TradingBot` and reuses it unchanged). Per
completed candle, in order:

1. **Fetch enriched history.** `data_manager.get_data_history(symbol, count=1)`
   (`trading_bot.py`) — OHLCV plus any aux columns (§3). An empty frame
   logs a warning and returns without touching portfolio state
   (`trading_bot.py`).
2. **Warmup-only short-circuit.** If `warmup_cutoff_timestamp` is set and
   this bar is before it, `strategy.update(data)` runs (so indicators are
   primed) and the method returns — no trade, no portfolio-state record
   (`trading_bot.py`). Default `None` means every bar always trades,
   byte-identical to before this mechanism existed
   (`core/backtester.py::BacktestEngine.__init__`).
3. **Read balances, mark to market.** `portfolio_info.get_account_balance()`
   then `_calculate_total_portfolio_value(balances, close)`
   (`trading_bot.py`).
4. **Optional funding accrual** (`model_funding`, off by default,
   `trading_bot.py`) — charged on the position **held into** this
   bar, using this bar's close as mark, before the rebalance below.
5. **Optional `PortfolioRiskGate.observe()`** (§8, off by default,
   `trading_bot.py`) folds this bar's decision-time equity into any
   stateful drawdown/daily-loss tracking, before the forecast is even
   computed.
6. **Compute previous (actual) allocation**
   (`portfolio_info._calculate_actual_allocation`, `trading_bot.py`).
7. **Update strategy, generate signal.** `strategy.update(data)` then
   `strategy.generate_signals()` (`trading_bot.py`) — see §5/§6.
8. **Forecast → allocation.** `forecast_manager.forecast_to_allocation(signal.forecast)`
   (`trading_bot.py`) — see §7.
9. **Optional `PortfolioRiskGate.apply()`** (§8, off by default,
   `trading_bot.py`) clamps/overrides the target allocation.
10. **Allocation delta.** `forecast_manager.calculate_allocation_change(target, previous)`
    (`trading_bot.py`).
11. **The only drift check that gates a trade attempt at all** is
    `if abs(allocation_change) != 0.0` (`trading_bot.py`) — but see §8:
    this is **not** the only gate on whether the trade is *approved*.
    Whenever the risk gate is latched flat (killed or daily-halted), the
    forced flatten instead bypasses `approve_allocation_change` entirely and
    goes straight to `_execute_portfolio_rebalance`
    (`trading_bot.py`) — the same direct-execute path
    `_close_all_positions_at_end` uses, so a residual position smaller than
    the min-Δ band can still be force-closed.
12. **Risk-manager approval** (§8) then execution
    (`execution_handler._execute_portfolio_rebalance`, §9,
    `trading_bot.py`).
13. **Record bar state** into `portfolio_state_tracker`
    (`trading_bot.py`) — one row per bar, later written to
    `portfolio_states.csv`/`bars.csv` (§10).

At shutdown (live `stop()`, or end of a backtest run),
`_close_all_positions_at_end()` (`trading_bot.py`) force-flattens any
still-open position through the same direct execution path, and merges its
post-close numbers onto the same bar's already-recorded row rather than
appending a second row for the same instant (`replace_if_same_bar`,
`execution/portfolio_info.py`).

### 4.1 Gap detection and gap-response tiers

Merged (CUL-261, CUL-271, CUL-273/273b; recovery rules fixed by CUL-359).

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

Recovery (CUL-359): the middle and large tiers both clear once
`bars_since_gap >= strategy.required_bars` real bars have passed (checked
before the bar's own update, so on the `required_bars + 1`-th real bar after
the gap). Before CUL-359 the large tier never cleared and kept the symbol
flat for the rest of the run. An ignore-tier gap during an active tier counts
as one real bar and does not cancel it; a middle gap during a large re-warm
keeps `large`. Each `data_quality` event records `bars_missing`, `tier` (as
classified) and, for middle/large gaps, `active_tier` (after that rule). When
gap detection is on, the gap settings are part of run identity.

Worked example (from the branch): `candle_interval_seconds=3600`,
`ignore_max_bars=2`, `large_min_bars=24`. A gap of 5 missing hourly bars is
"middle" — position held, new entries blocked until 24+ real bars have
passed since. A gap of 30 missing bars is "large" — immediate flatten plus
full re-warm.

---

## 5. Warmup of the Strategy and Its Components

`AdvancedStrategy.is_ready()` (`strategies/main_strategy.py`) is an AND
of three gates, evaluated in this order:

1. `self.data_buffer.size < self.required_bars` → not ready
   (`main_strategy.py`). `data_buffer` is a `RollingBuffer`
   (`strategy_base.py`) sized `required_bars + 100`
   (`main_strategy.py::AdvancedStrategy.__init__`).
2. `self.regime_engine.is_ready()` → not ready (`main_strategy.py`).
   For `threshold_rules` mode this means every detector-component history has
   `len >= 1`; for `score`/`score_product` mode every history must be full to
   its `lookback` (`strategies/regime_engine.py::ConfigDrivenRegimeEngine.is_ready`).
3. The **current** bar's regime is classified first (`self._classify_once()`,
   `main_strategy.py`) — a deliberate ordering fix (labeled
   "F7" in the code) so `strategy_engine.is_ready(regime)` checks readiness
   for the regime this bar just resolved to, not last bar's regime (which,
   on the very first ready-candidate bar, would otherwise be the
   `MarketRegime.UNKNOWN` class-init default and vacuously "ready" for any
   regime with no components registered under that key).
   `ConfigDrivenStrategyEngine.is_ready(regime)`
   (`strategies/strategy_engine.py`) requires every component history
   deque *for that regime* to have `len >= self._warmup`.

`required_bars = max(regime_engine.get_required_periods(),
strategy_engine.get_required_periods(), 24)` (`main_strategy.py::AdvancedStrategy.__init__`) — the
`24` is the hardcoded `stddev_24` period the data buffer also computes as a
lazy calculated column (`main_strategy.py::AdvancedStrategy.__init__`).

**A currently-real drift between `required_bars` and the strategy engine's
own internal `_warmup`.** On this checkout,
`ConfigDrivenStrategyEngine.__init__` derives `_warmup` independently from
its own local config — `min(config.get("warmup", self.lookback), min_buf)`
(`strategy_engine.py`) — **not** from `AdvancedStrategy.required_bars`
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

### 5.1 Effective warmup is ~2x `required_bars`, not `required_bars`

A gap this guide's first draft missed, since re-added from
`TIMEFRAME_CHANGE_PLAYBOOK.md` §1 and re-verified directly against
`core/launcher.py` on this checkout. `AdvancedStrategy.required_bars` (§5
above) tells you when a component's OWN `is_ready()` first goes true — but
`strategy_engine.is_ready()` additionally requires each component's history
DEQUE to reach length `strategy_engine._warmup`, and that deque only starts
accepting entries once the component is already ready. So the total bars
needed before the STRATEGY itself is ready is `required_bars + _warmup - 2`,
not `required_bars` alone. Since `_warmup <= required_bars` always, `2 x
required_bars` is a safe, easy-to-verify upper bound without needing the
exact formula.

At 1h this is invisible (`required_bars` is small, ~24-50 bars, absorbed into
any reasonably-sized backtest window). At 1d, with `required_bars` around
100 (e.g. a 100-day SMA), the gap between "component ready" and "strategy
ready" is ~100 EXTRA days — large enough that a walk-forward window shorter
than ~200 days never trades at all, for every window, regardless of true
signal quality.

**The fix, verified present:** `core/launcher.py::run_backtest`'s
`warmup_prefetch` parameter (`launcher.py`, `bool = False` — off by
default, byte-identical when omitted, per
`tests/test_warmup_prefetch_bit_identical.py`). When `True`: fetches `2 *
strategy.required_bars` of EXTRA history before the window's `start`
(`launcher.py`), feeds it through `strategy.update()` silently via
`BacktestEngine.warmup_cutoff_timestamp` (bars before this timestamp update
indicators but never trade or touch portfolio state —
`core/backtester.py`, `core/trading_bot.py`), then asserts
`is_ready()` is actually true by `start` — failing loudly, not silently, if
the 2x margin is ever insufficient for some future config
(`launcher.py`).

**Do not "optimize" the 2x multiplier down to 1x.** It looks wasteful, but
`_warmup` is not `0` for any component using `strategy_config.json`'s
`strategies.warmup` field — every production config sets one. 1x silently
reintroduces the exact under-warmed-strategy bug this fixes.

**Left-edge / exchange-history constraint.** The prefetch has to come from
somewhere. If `window_start - 2*required_bars` predates the exchange's
actual listing date (e.g. BTCUSDT/ETHUSDT: 2017-08-17 on Binance — a locally
cached `_1d.csv`/`_1h.csv` may start later than that for unrelated
historical reasons), the first scored window(s) silently underrun their
warmup. Resolve this BEFORE registering a protocol: extend the backfill to
the true exchange start (verify with `tools/check_data.py` afterward), and
set the first scored window far enough past the true start to leave a real
margin, not just clear the bare minimum.

---

## 6. Update and Forecast Calculation

The real, currently-executing call chain, traced directly (not from
comments, which describe a different, superseded mechanism — see below):

```
AdvancedStrategy.generate_forecast()             (strategies/main_strategy.py)
  -> regime, debug_regime = self._classify_once()       (regime_engine.classify(), regime_engine.py)
  -> forecast, debug_components = self.strategy_engine.forecast(regime)
                                                          (strategy_engine.py)
       -> for each component in regimes[regime].components:
            h = self._history[regime.value][component_id]   (deque, populated by update())
            value = apply_transform_pipeline(pd.Series(h), c["transforms"], self._data)
                                                          (strategies/registry.py)
            ensemble += (weight / total_weight) * value
       -> return clip(ensemble, -20.0, 20.0)             (np.clip, strategy_engine.py)
```

`ConfigDrivenStrategyEngine.update()` (`strategy_engine.py`) runs **every**
component in **every** regime unconditionally each bar — not just the
active regime's — so inactive-regime histories stay warm across a regime
switch (see `DOC/STRATEGY_FRAMEWORK.md` invariant #8, re-verified against
this file directly).

- A component's raw value is appended to its regime/component history only
  once that component's own `is_ready()` fires
  (`strategy_engine.py::ConfigDrivenStrategyEngine.update()`) — this is a
  length check, not a NaN check, so a NaN-producing component's NaN values
  do get pushed into history once ready; they are never filtered
  (`strategy_engine.py::ConfigDrivenStrategyEngine.update()`, no guard
  present).
- `history_transforms`, if declared on a component spec, run once **at
  append time** and define what the deque actually stores
  (`strategy_engine.py::ConfigDrivenStrategyEngine.update()`); `transforms`,
  applied inside `forecast()`, run fresh every bar over the stored history
  (`registry.py::apply_transform_pipeline`).
- `apply_transform_pipeline` seeds `value = history[-1]` and applies each op
  in order — history-based ops (`identity`, `percentile`,
  `negate_percentile`, `zscore`, `ratio_to_mean`, `ema`) recompute from the
  full history and discard the accumulated `value`; scalar/data-aware ops
  (`scale`, `threshold_filter`, `clip`, `sigmoid`, `negate`,
  `vol_normalize`, `vol_adjusted`, `price_normalized`, `volume_filter`)
  operate on it — 15 ops total in `TRANSFORM_OPS_REGISTRY` as read on this
  checkout (`registry.py`).

`ConfigDrivenRegimeEngine.classify()` (`strategies/regime_engine.py`)
evaluates vetoes first, unconditionally, regardless of mode — a veto that
fires for `consecutive_bars` in a row force-sets the regime and returns
immediately (`regime_engine.py`). It then dispatches by `regime_detector.mode`
to one of three classifiers:

- `threshold_rules` — priority-ordered if/else over the latest raw
  component values (`regime_engine.py::ConfigDrivenRegimeEngine._classify_threshold_rules`).
- `score` — weighted transformed components, argmax with a minimum score
  and margin (`regime_engine.py::ConfigDrivenRegimeEngine._classify_score`).
- `score_product` — the multiplicative variant
  (`regime_engine.py::ConfigDrivenRegimeEngine._classify_score_product`).

### 6.1 A documentation trap: describe this, not the dead mechanism

Root `CLAUDE.md`'s own "Strategy hierarchy" section (and, more broadly,
prose elsewhere in this repo describing a "raw forecast is normalized by
`stddev_24 * close`... then scaled so the mean or target quantile maps to
±10" mechanism) describes `SubStrategyComponent.generate_forecast()` /
`.standardize_forecast()` / `.store_raw_forecast()`
(`strategies/strategy_base.py`) — **this is not what runs**.
Confirmed independently three ways on this checkout:

1. A literal grep for `CompositeStrategy(` (the only class whose
   `generate_forecast()` calls a component's `generate_forecast()`,
   `strategy_base.py`) across the entire tree returns **zero
   instantiations** — only its own class definition
   (`strategy_base.py`).
2. `AdvancedStrategy.__init__` builds `ConfigDrivenRegimeEngine` and
   `ConfigDrivenStrategyEngine` directly (`main_strategy.py`); neither
   of those classes references `SubStrategyComponent.generate_forecast`,
   `.standardize_forecast`, or `.store_raw_forecast` anywhere.
3. `strategies/registry.py::TRANSFORM_OPS_REGISTRY` is a fixed dict of
   plain lambdas with no `self`/component-instance access
   (`registry.py`) — nothing there could reach the dead methods
   dynamically either.

`SubStrategyComponent.generate_forecast()` et al. remain in the tree,
unused. Whether to delete them is a separate cleanup decision (tracked as
CUL-281 in the E-045 addenda) — out of scope for this guide.

---

## 7. Allocation Calculation

`ForecastManager` (`execution/forecast_manager.py`) is stateless —
`__init__` takes no arguments (`forecast_manager.py`). Two pure
functions:

- `forecast_to_allocation(forecast)` = `forecast / 10.0`
  (`forecast_manager.py`, `FORECAST_FOR_100_INVESTMENT = 10.0`,
  `forecast_manager.py`) — maps the `[-20, +20]` forecast range to a
  `[-2.0, +2.0]` target allocation (a forecast of ±10 is ±100% of equity;
  the clip to `[-20,+20]` upstream means the realistic target range is
  `[-2.0, +2.0]`, i.e. up to 2x leverage, before any risk-manager cap is
  applied — see §8).
- `calculate_allocation_change(target, current)` = `target - current`
  (`forecast_manager.py`).

**The docstring on this checkout is stale — a real issue in the code itself,
not just in surrounding documentation: it currently claims "NO DRIFT
THRESHOLD LIVES HERE, and none lives anywhere else either"
(`forecast_manager.py::ForecastManager`). That is false, and has been false since
before this checkout — `RiskManager._ctrl_min_allocation_change`
(`risk/risk_manager.py`) already rejects any rebalance where
`abs(allocation_change) < risk_management.controls.min_allocation_change.threshold`
(`config.json`, default `0.2`) — see §8.** A pending, not-yet-merged
commit (`e756614a`, E-055) corrects this exact docstring and adds the
per-strategy override described in §8.

---

## 8. Acceptance Check of Order (Risk Gate)

Two independent risk layers exist. Only the first is on by default.

### 8.1 `RiskManager` — the per-trade allocation-change band (always active)

`RiskManager.approve_allocation_change(symbol, change, data)`
(`risk/risk_manager.py`) iterates `self.controls` (from `config.json`'s
`risk_management.controls`,
`core/launcher.py::Launcher._build_risk_and_forecast_managers`). For each
control name present, it calls `self._ctrl_{name}` if that method exists
(`risk_manager.py::RiskManager.approve_allocation_change`) — an
unrecognized control name is silently skipped, not an error. Two controls
are wired on this checkout:

- `_ctrl_max_allocation_change` (`risk_manager.py`): rejects if
  `abs(change) > controls.max_allocation_change.max + 1e-6`. Committed
  value: `4.0` (`risk_management.controls.max_allocation_change.max`).
- `_ctrl_min_allocation_change` (`risk_manager.py`): rejects if
  `abs(change) < controls.min_allocation_change.threshold - 1e-6`.
  Committed value: `0.2` (`risk_management.controls.min_allocation_change.threshold`).

So the band is `0.2 <= |Δ| <= 4.0` on the committed config (§7). Rejection
just logs and skips the rebalance for that bar
(`trading_bot.py::TradingBot._process_symbol_candle_completion`) — the position is simply left where it was.

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

`risk/portfolio_risk_gate.py::PortfolioRiskGate` implements three additional,
independently-configurable controls, built only when
`config.json`'s `risk_management.portfolio_controls` is a non-empty dict
(`core/launcher.py::Launcher._build_risk_and_forecast_managers`; **absent on the committed config.json**, so this
gate is `None` and every one of the following is inert by default):

- **`absolute_allocation_cap`** — stateless: clamps the target allocation to
  `[-cap, +cap]` (`portfolio_risk_gate.py::PortfolioRiskGate.apply`).
- **`max_drawdown_kill`** — stateful, terminal: tracks the running peak of
  decision-time equity; once drawdown `>= threshold` it **latches** for the
  rest of the run, forcing the target to `0.0` every subsequent bar
  (`portfolio_risk_gate.py::PortfolioRiskGate.observe`,
  `PortfolioRiskGate.apply`). Un-latching requires a
  fresh run.
- **`daily_loss_limit`** — stateful, day-scoped: anchors day-start equity per
  a configurable timezone (default `Europe/Paris`, tz-aware, derived from
  the UTC bar timestamp); once intraday loss `>= threshold` it halts for the
  remainder of that calendar day and re-arms at the next midnight rollover
  with a fresh anchor (`portfolio_risk_gate.py::PortfolioRiskGate.observe`).

Validated by `validate_portfolio_controls()` (`portfolio_risk_gate.py`)
— shared by both `ConfigManager.validate()` (the `config.json` path) and
`run_backtest()`'s `risk_controls` override — unknown keys and out-of-range
values (thresholds must be finite numbers in `(0, 1)`) fail loud rather than
silently arming or skipping a control.

When active, the gate composes with `TradingBot._process_symbol_candle_completion()`
as described in §4: `observe()` runs before the forecast is computed,
`apply()` runs after the target allocation is derived but before the
allocation delta, and a latched-flat gate bypasses `RiskManager` entirely via
the same direct-execute path the end-of-run force-close uses
(`trading_bot.py::TradingBot._process_symbol_candle_completion`) — otherwise the `0.2` min-Δ band would block a
small residual position from ever fully flattening.

### 8.3 Gap-response tiers as a third layer

See §4.1. The "middle" tier blocks new entries and the "large"
tier forces an immediate flatten composed the same way the `PortfolioRiskGate`
latch is — both act on `target_allocation` before `allocation_change` is
derived, so whichever fires, the delta is computed consistently
(verified on `fix/cul-273b-reindex-wiring-and-standardization-nan`).

---

## 9. Portfolio / Execution

`BaseExecutionHandler` (`execution/execution_handler.py`) contains all
orchestration shared by `ExecutionHandler` (live, Binance margin API) and
`MockExecutionHandler` (backtest simulation) — subclasses implement only
three primitives: `open_long_position`, `open_short_position`,
`close_position`, each returning `(success: bool, debug: dict)`. The call
chain per rebalance:

- `_execute_portfolio_rebalance()` (`execution_handler.py`) dispatches to
- `_handle_allocation_change()` (`execution_handler.py`), which either
  routes through
- `_execute_position_transition()` (a sign flip — short/neutral to
  long/neutral or vice versa, close-then-open, `execution_handler.py`), or
  does a simple add/reduce of the existing position.

`MockExecutionHandler.open_long_position()` / `open_short_position()` /
`close_position()` (`execution_handler.py`) fill at the bar's raw
`close` price — **there is no slippage model in this checkout's execution
path.** Cost enters only through `CommonPortfolioDef.update_local_balance()`'s
flat `commission_rate` (`execution/portfolio_info.py`, default
`0.001` i.e. 10bps, `DEFAULT_COMMISSION_RATE` in
`performance/metrics.py`), applied identically to every trade regardless
of symbol or venue.

**Pending merge (E-010 S3, commit `5846dd3d` on branch
`feat/e010-s3-real-slippage-defaults` — real, tested, not on this
checkout):** `config/cost_model.py::resolve_cost_model(exchange, market_type,
symbol=None)` resolves `(fee_bps, slippage_bps)` from `config/cost_model.json`,
keyed by `(exchange, market_type)` with a per-symbol `slippage_bps` map.

- Mandatory `"default"` fallback key — a missing symbol falls back to the
  venue's conservative default, logged loudly so a fallback estimate never
  silently reads as calibrated (`resolve_cost_model` docstring).
- An unconfigured `(exchange, market_type)` combination raises
  `UnknownCostModelError` rather than defaulting — deny by default, matching
  this project's general convention.
- Calibrated defaults on that commit: binance/margin `{BTCUSDT: 1bps,
  ETHUSDT: 1.5bps, default: 1.5bps}`; kraken/futures `{BTCUSD: 2.5bps,
  ETHUSD: 4bps, AVAXUSD/SOLUSD: 7.5bps, default: 7.5bps}`.
- `MockExecutionHandler` on that branch resolves slippage per symbol at fill
  time instead of a flat float threaded in at construction; `core/backtester.py`
  folds the effective cost model into run provenance (`config_sha256`)
  unconditionally, closing a gap where two runs could otherwise share
  config/data/git hashes yet differ in cost economics purely because
  `cost_model.json` changed between them.
- Declared default-behavior change on that commit: real slippage went from
  0bps to BTCUSDT=1bps, moving the reference anchor from
  `net_pnl -231.758912` to `-238.279247` (trade count unchanged at 24).

`MockPortfolioInfo`/`PortfolioInfo` (both extend `CommonPortfolioDef`,
`execution/portfolio_info.py`) track balances as a flat
`{asset: {free, locked}}` dict.

- `update_local_balance()` (`portfolio_info.py`) applies the trade and
  commission per `trade_type` (`LONG`/`SHORT`/`REDUCE_LONG`/`REDUCE_SHORT`/`CLOSE`),
  including margin-borrow bookkeeping for a buy that exceeds free USDT.
- `apply_funding()` (`portfolio_info.py`) is the separate, off-by-default
  perpetual-funding cash-flow accrual described in §4 step 4 — pure
  USDT-balance mutation, independent of the trade path and never
  interacting with commission.
- `PortfolioStateTracker.record_state()` (`portfolio_info.py`) appends one
  row per bar (merging rather than duplicating a row when
  `replace_if_same_bar` fires at end-of-run, as described in §4).

---

## 10. Backtest Output / Artifacts

Every backtest writes to `results/runs/<UTC-timestamp>_<config-sha8>/`
(`reporting/run_artifact.py::new_run_dir`) — or, for
research callers that pass `runs_root`, directly under that root without a
`runs/` subdirectory. `<config-sha8>` is the first 8 hex chars of a SHA-256
over the canonicalized (sorted-keys) provenance config
(`run_artifact.py::new_run_dir`), the same `_provenance_config` that folds in
`model_funding`/`fetch_interval_seconds`/cost-model provenance when they
diverge from their defaults (`core/backtester.py::BacktestEngine._end_of_backtest`, §3.2).

Files written (`reporting/run_artifact.py`, `trading-bot/DOC/RUN_ARTIFACT.md`
— re-verified against the writer functions directly):

- **`manifest.json`** (`write_manifest`, `run_artifact.py`) —
  `run_id`, `created_utc`, the full `config` snapshot, `config_sha256`, a
  `data` block (`symbols`, `timeframe`, `start`, `end`, `bar_count`,
  `data_sha256` — a hash over `timestamp,open,high,low,close,volume` only,
  `run_artifact.py`), `git_sha` (with a `-dirty` suffix if any
  **tracked** file differs from `HEAD`, deliberately ignoring the
  permanently-untracked `results/runs/` evidence dirs,
  `run_artifact.py::_get_git_sha`), and `engine.{lookback, warmup}` (read from
  `strategy.strategy_engine.lookback`/`._warmup`, `core/backtester.py::BacktestEngine._end_of_backtest`
  — so this field currently reflects the config-derived `_warmup`, not
  `required_bars`; see §5's pending CUL-273 note). An optional `feeds` block
  (registered/dropped/required feed names) is added only when a caller
  passed a non-`None` `drop_feeds` (`core/backtester.py::BacktestEngine._end_of_backtest`).
- **`metrics.json`** (`write_metrics_json`, `run_artifact.py`) —
  `core` (§11), `per_regime`, `forecast_bins`, `dynamic` (per-component
  per-regime mean/std), plus optional `regime_validity`, `bar_equity`,
  `risk_controls` and `data_quality` blocks, each present only when the
  corresponding off-by-default feature is enabled for that run;
  `component_errors` whenever a real strategy ran; and `nan_forecast`
  (CUL-274) only when at least one bar's forecast was NaN or infinite --
  those bars hold the current position (`policy: hold`).
- **`trades.json`** — one record per `CompletedTrade.to_dict()`
  (`run_artifact.py::write_trades_json`; fields listed in §11).
- **`bars.csv`** — the full per-bar `portfolio_state_tracker` frame, rounded
  to 6 decimals (`write_bars_csv`, `run_artifact.py`), with
  dict-valued columns (like `debug_info.components.*`) flattened to
  dot-separated scalar columns first (`flatten_dict_columns`,
  `execution/portfolio_info.py`).
- **`forecast_distribution.csv`** — per-regime forecast histogram over 8
  fixed bins (`write_forecast_distribution`, `run_artifact.py`).
- **`tradesxl.xlsx`** — Excel mirror of `trades.json` plus a
  `Performance_Metrics` sheet with per-metric explanatory comments
  (`export_trades_to_excel`/`export_metrics_to_excel`, `performance/metrics.py`).
- **`portfolio_states.csv`** — written by `PortfolioStateTracker.to_csv()`
  into the same run directory (`core/backtester.py::BacktestEngine._end_of_backtest`) — the
  un-rounded twin of `bars.csv`, the input `performance/bar_equity.py`'s
  functions and `build_bar_equity()` (§11) actually consume.

---

## 11. Metrics Calculated

`EnhancedPerformanceTracker` (`performance/metrics.py`) matches
trade executions **LIFO** (Last-In-First-Out) inside
`_process_executed_trades()` (`metrics.py`): an opposite-direction
execution walks the open `Position`'s executions from most recent to oldest
(`metrics.py`), closing each in turn until the new execution's quantity
is fully matched, producing one `CompletedTrade` per match
(`metrics.py`); any quantity left over after the whole position is
closed becomes a **reversal** — a brand-new position in the opposite
direction (`metrics.py`).

`CompletedTrade` (`metrics.py`) exposes, among others:
`profit_loss_percent`/`profit_loss_absolute` (gross), `entry_commission` /
`exit_commission` / `total_commission` (fee-tier-aware: whether the fee is
deducted from the received or the quote asset depends on LONG vs. SHORT and
entry vs. exit, `metrics.py`), `net_profit_loss_percent`
/`net_profit_loss_absolute`, `net_portfolio_profit_loss_percent` (impact on
total equity, not just the trade's own return), `duration_minutes`, and
`entry_forecast`/`entry_regime`/`entry_confidence` (and the `exit_*` twins) —
carried straight from the `TradeExecution` that opened/closed the position.

**Trade-exit-basis Sharpe/drawdown** (`calculate_sharpe_ratio`/
`calculate_max_drawdown`, `metrics.py`, used by
`_calculate_standard_metrics` → `metrics.json`'s `core` block): both group
completed trades by **exit date**, reindex onto the full calendar from first
to last trade, and fill every non-trading day with a synthetic `0.0` return
(`metrics.py::EnhancedPerformanceTracker.calculate_sharpe_ratio`) before computing an annualized (`sqrt(365)`) Sharpe
and a running-max drawdown over the compounded daily-return equity curve.
This means Sharpe/drawdown here sample only as many points as there are
distinct trade-exit days — 24 points on the committed reference window per
`CLAUDE.fork.md`'s own figures, re-derivable from `trades.json`'s trade
count on that window.

**Bar-level alternative** (`bar_equity`, off by default,
`performance/bar_equity.py` + `reporting/run_artifact.py::build_bar_equity`):
computed instead from the full per-bar
`postRebalance_total_value` series, **excluding** every bar whose `regime`
normalizes to `"NOT_READY"` (`run_artifact.py::build_bar_equity` — the same string
`MainStrategy.generate_signals()` emits at `strategy_base.py`, so a
warmup bar the strategy could not have acted on never dilutes the volatility
estimate). Every degenerate input here raises `ValueError` rather than
silently producing a wrong number: missing required columns, zero bars
surviving the warmup exclusion, NaN among the surviving bars, or a
non-finite `max_drawdown_pct` (`run_artifact.py::build_bar_equity`). Turnover is
computed from **executed** allocation deltas
(`postRebalance_current_allocation` vs. `previous_allocation`,
`run_artifact.py::build_bar_equity`), not the raw `allocation_change` field, which
also counts rejected rebalance attempts. Reference figures recorded at
`fix/metrics-bar-equity`'s merge (`CLAUDE.fork.md` backlog item 3): maxDD
−24.77 vs. trade-exit −24.59, Sharpe −5.12 vs. −5.65, Sortino −5.05
(downside deviation `sqrt(mean(min(r,0)^2))` over **all** daily returns
against a target of 0, not the sample std of negative days alone,
`run_artifact.py::build_bar_equity`).

<!-- Fast suite re-run on this checkout after the first draft: 556 passed,
33 skipped, 47 deselected, 0 failed -- confirms nothing in this guide
contradicts the current test suite's actual behavior. This does not by
itself re-verify every specific byte-identity NUMBER cited above (§3.2, §7,
§9) -- those would need the named slow tests run individually with their
asserted values compared -- but it does rule out the broader risk that this
guide describes behavior the codebase's own tests disagree with. Citations
in this guide were converted from file:line to name-based form on
2026-09-11 (mechanical pass, 6 parallel verification agents, one per major
section) -- see git history for the prior line-numbered revision if an old
citation is needed for archaeology. The former §11.1 (a research-tooling
modeling decision living in strategy-research/, not trading-bot/) and §12
("Known Documentation Discrepancies") were removed the same day, per a
scope call: this guide covers trading-bot/ engine capabilities only --
discrepancies with OTHER docs (root CLAUDE.md, CLAUDE.fork.md) belong fixed
in those docs directly, not tracked here. See git history for that content
if needed. -->
