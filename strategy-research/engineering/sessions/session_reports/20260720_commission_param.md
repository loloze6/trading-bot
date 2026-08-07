# Phase 1.2 / Dispatch C — Expose commission_rate as an overridable parameter

Date: 2026-07-20
Precondition check: PASSED — HEAD=618d548, `git status --porcelain` showed exactly
the four expected untracked reports and nothing else.

## Summary

Added an optional `commission_rate` parameter to `core/launcher.py::run_backtest()`,
the function `strategy-research/tools/run_protocol.py` calls for every walk-forward
window. Omitted, it resolves to `DEFAULT_COMMISSION_RATE` exactly as before (confirmed
byte-identical). Set, it overrides the per-trade commission simulation for that
backtest only — this is what makes a real Kraken-fee-calibrated re-run of
`rsi_momentum_trending_cost_drag` / `keltner_scoremode_no_edge` (blocked in
`20260720_cost_calibration.md`) now possible, pending the independent audit this
roadmap requires before the parameter is used for any calibration re-run.

## file:line diff summary

**`trading-bot/core/launcher.py`**
- `:22` — import adds `DEFAULT_COMMISSION_RATE` from `performance.metrics` (was
  previously defined locally at this file's old line 28).
- `:27-29` — removed the local `DEFAULT_COMMISSION_RATE: float = 0.001` definition;
  left a one-line pointer comment to where it now lives.
- `:469-472` — `run_backtest()` signature gains `commission_rate: float = None`.
- `:508-511` — docstring documents the new parameter (no-op-when-omitted contract,
  same pattern as the existing `interval_seconds` docstring note).
- `:522-524` — new `resolved_commission_rate = commission_rate if commission_rate is
  not None else DEFAULT_COMMISSION_RATE`; the `TradingParams(...)` construction below
  now passes `commission_rate=resolved_commission_rate` instead of the hardcoded
  constant.
- **Not touched**: `_build_mock_stack()` (old lines 148-153, `EnhancedPerformanceTracker`
  / `MockPortfolioInfo` construction) — already read `params.commission_rate`
  generically; no edit needed. `run_bot()`'s `EnhancedPerformanceTracker(
  DEFAULT_COMMISSION_RATE)` (old line 199, live-trading path) — architecturally
  unreachable from `run_backtest()` (separate call graph, live trading is out of this
  dispatch's scope) and already single-sourced from the constant; left as-is.

**`trading-bot/performance/metrics.py`**
- `:35-38` — new module-level `DEFAULT_COMMISSION_RATE: float = 0.001` — the constant's
  new canonical home (chosen because `launcher.py` already imports from `metrics.py`;
  the reverse direction would create a circular import).
- `:55` — `TradeExecution.commission_rate` dataclass field default changed from the
  literal `0.001` to `DEFAULT_COMMISSION_RATE`.
- `:322` — `EnhancedPerformanceTracker.__init__`'s `commission_rate` parameter default
  changed from the literal `0.001` to `DEFAULT_COMMISSION_RATE`.
- Both confirmed dead in the live call graph before editing (every `TradeExecution(...)`
  and `EnhancedPerformanceTracker(...)` construction site in the repo already passes
  `commission_rate` explicitly) — this was a duplicate-literal cleanup, not a behavior
  change.

**`trading-bot/tests/test_commission_rate_param.py`** (new, 111 lines) — see below.

## Test count before/after

Full `trading-bot/` suite (`pytest tests/ -q -m "slow or not slow"`, i.e. every test
including the slow-marked integration tests):
- **Before** (HEAD=618d548, verified via `git stash`): 41 passed, 4 pre-existing
  errors in `test_regression_backtest.py` (`ValueError: invalid strategy_config` —
  confirmed present identically on unmodified HEAD, unrelated to this change).
- **After**: 44 passed, same 4 pre-existing errors, unchanged.
- Delta: exactly +3, all from the new file. Default fast suite (`-m "not slow"`,
  matches `pytest.ini`'s `addopts`): 38 passed both before and after (new tests are
  `slow`-marked, matching the existing `test_warmup_prefetch_bit_identical.py`
  convention since they run the real backtest engine).
- Suite stayed green; no new failures.

## Proof of (a) — byte-identical on omit

`test_omitted_matches_reference_fixture` reuses the pre-existing
`tests/fixtures/warmup_prefetch_reference.json` golden fixture (BTCUSDT,
2024-01-01→2024-01-11) and confirms `commission_rate` omitted reproduces its captured
`net_pnl=1.904077` / `sharpe=15.665`. `test_explicit_default_matches_omitted` goes
further: passing `commission_rate=DEFAULT_COMMISSION_RATE` explicitly produces a
`core` dict and `trades.json` list **identical** (`==`) to the omitted run — direct
manual verification (see below) confirms this at the full-precision level, not just
within the fixture's rounding tolerance.

Manual verification (`python -c` invoking `run_backtest` three times — omitted,
explicit `0.001`, and `0.008`):
```
omitted:          net_pnl=1.904077  sharpe=15.665   fees_paid=3.996909   cost_drag_pct=67.7329
explicit_default: net_pnl=1.904077  sharpe=15.665   fees_paid=3.996909   cost_drag_pct=67.7329   <- byte-identical to omitted
```

## Proof of (b) — divergent trade path, not just a fee rescale

Same manual run with `commission_rate=0.008` (Kraken's 80bps taker rate):
```
kraken_80bps: net_pnl=-26.010819  sharpe=-22.003  fees_paid=31.862725  cost_drag_pct=544.4846
```
Direction confirmed as expected: `fees_paid` and `cost_drag_pct` up, `sharpe` and
`net_pnl` down, vs. the default-rate run.

`matched_quantity` per trade (2 trades in this window):
- Trade 1 (index 0): `0.021427555150241445` at **both** the default rate and 0.008 —
  identical, as expected: its size is computed off the fixed initial balance
  (1000 USDT), before any commission has touched anything yet.
- Trade 2 (index 1): `0.02143575422858001` (default rate) vs.
  `0.021134778845379707` (0.008 rate) — **diverges**, confirming trade 2's sizing read
  a fee-eroded `total_portfolio_value` carried over from trade 1, exactly the
  compounding mechanism `20260720_run059_replay_feasibility.md` identified. This is
  what `test_nondefault_rate_changes_trade_path` asserts directly (`trades[0]` equal,
  `trades[1]` not equal, plus the four directional core-metric assertions above).

## Confirmation

`trading-bot/` was the only code touched (plus this report and the new test file).
No other trading-bot files were modified. A pre-existing test-run side effect
(`trading-bot/results/trades.json` being overwritten by `EnhancedPerformanceTracker`'s
default `log_file` path, independent of `results_root`) was caught and reverted
before commit — not part of this change, and not committed.

## Note for the mandated audit

Per this roadmap's Part 3, this parameter must not be used for any calibration
re-run (e.g. re-running `rsi_momentum_trending_cost_drag` / `keltner_scoremode_no_edge`
at Kraken's 80bps) until a third-party read-only auditor has reviewed this commit.
