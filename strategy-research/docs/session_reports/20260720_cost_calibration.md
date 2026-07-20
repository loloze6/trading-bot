# Phase 1.2a — Cost-Model Calibration to Kraken: STOP (trading-bot edit required)

Date: 2026-07-20
Precondition check: PASSED — HEAD=618d548, `git status --porcelain` showed exactly
the two expected untracked report files, neither touched.

## Steps completed before the stop

### Step 1 candidate — spot-only confirmation (passed)

Read `campaign_knowledge_base.yaml` for both near-miss findings:

- `rsi_momentum_trending_cost_drag` (line 153): mechanism "RSI momentum in TRENDING
  regime", `evidence_runs: [run_018]`, `cost_drag_pct: 272.865`. No funding/perp/derivatives
  reference — a single-asset spot regime signal.
- `keltner_scoremode_no_edge` (line 102): mechanism "Keltner score-mode (composite
  multi-threshold, TRENDING)", `evidence_runs: [run_028, run_030]`, `exhausted_basis`
  cites "cost_drag=84% on the highest-IC variant (run_028)". No funding/perp/derivatives
  reference — also single-asset spot.

Both confirmed spot per the P2 universe (BTCUSDT/ETHUSDT/SOLUSDT/AVAXUSDT) that
`cost_model.yaml`'s `execution_style` block is scoped to. Kraken spot taker rate per
the venue survey (footnote 9, official fee-schedule page): **0.80% = 80 bps** at base
tier — this is the figure the dispatch specified, not the conflicting 0.40%/0.25%
secondary-source numbers the survey flagged as unresolved.

### Step 1 tool identification (passed)

Traced `protocol_result.yaml`'s `median_cost_drag_pct` for each run to confirm the
producing tool:
- run_018: `median_cost_drag_pct: 290.5301`→...→`272.865` (matches KB), `protocol_file:
  protocols\baseline_v1.json`.
- run_028: `median_cost_drag_pct: 84.2881` (matches KB's "84%" citation),
  `protocol_file: protocols\escalation_solusdt_4h.json`.

Both are `run_protocol.py` walk-forward outputs (per-window `core` block +
`median_cost_drag_pct` summary), not `prescreen_signal.py`.

## Step 2 — blocked: `cost_model.yaml` does not feed `cost_drag_pct`

Before editing `cost_model.yaml`, traced how `run_protocol.py` actually produces the
`cost_drag_pct` value both KB findings cite. This matches and extends yesterday's
`20260719_cost_model_recon.md`, which already flagged the risk (see its "Important
adjacent finding" and Step 3) — this dispatch's job was to confirm whether that risk
is load-bearing for these two specific candidates. It is:

1. `run_protocol.py`'s only read of `cost_model.yaml` (`_load_cost_model` /
   `_cost_paid_bps`, lines 83–94, 233–245) feeds exactly one field: the per-trade
   `cost_paid` bps entry inside `trade_diagnostics.json`. It is **not** an input to
   `cost_drag_pct`.
2. `cost_drag_pct` is computed in `trading-bot/reporting/run_artifact.py:180-182` as
   `(gross_pnl - net_pnl) / abs(gross_pnl) * 100`, where `net_pnl` sums
   `CompletedTrade.net_profit_loss_absolute` — a value the trading-bot backtest engine
   computes internally during the run, before `run_protocol.py` ever sees it.
3. That commission simulation is driven by `DEFAULT_COMMISSION_RATE = 0.001` (10 bps),
   a Python constant in `trading-bot/core/launcher.py:28`, independently duplicated in
   `trading-bot/performance/metrics.py` (`CompletedTrade.commission_rate` default,
   `EnhancedPerformanceTracker.__init__` default). None of these three sites read
   `cost_model.yaml`.
4. Confirmed no override path exists: `run_backtest()`
   (`trading-bot/core/launcher.py:469`) hardcodes `commission_rate=DEFAULT_COMMISSION_RATE`
   at line 519 and exposes no `commission_rate` parameter to its caller. `run_protocol.py`
   calls `run_backtest(...)` with no such argument (it can't — there isn't one).

**Consequence:** editing `cost_model.yaml`'s `fee_rate_bps` to Kraken's 80 bps and
re-running `run_protocol.py` for run_018's and run_028's protocols would reproduce
byte-identical `cost_drag_pct` values (272.865% and 84.2881%) — the backtest engine
never sees the new rate. Reporting those unchanged numbers as a "Kraken-calibrated
re-run" would be a fabricated result, not a real recomputation. Making the re-run
actually reflect Kraken's fee requires parameterizing `DEFAULT_COMMISSION_RATE` (or
threading a `commission_rate` argument through `run_backtest`) from a trading-bot
source — i.e., editing `trading-bot/core/launcher.py` and/or
`trading-bot/performance/metrics.py`.

## Outcome

Per this dispatch's explicit STOP condition ("any need to touch trading-bot →
full STOP, report"): **halted before any edit.** `cost_model.yaml` was not modified,
no re-run was executed, and no commit was made. `git status --porcelain` still shows
only the same two pre-existing untracked report files.

## Recommendation for a follow-up dispatch

Pick one, both out of scope for this dispatch:
- (a) Authorize a trading-bot change (small: parameterize `commission_rate` on
  `run_backtest`, default-preserving) so `run_protocol.py` can pass
  `cost_model.yaml`'s per-symbol `fee_rate_bps` into the actual simulation — this is
  the structural fix the 2026-07-19 recon already recommended.
- (b) Accept an explicit, clearly-labeled analytic recomputation of `cost_drag_pct`
  outside the tool (using each run's existing `gross_pnl`/`trade_count`/`fees_paid`
  and the new 80 bps rate) as a documented exception to "use whatever tool produced
  the original figures" — weaker evidence, but doesn't require a trading-bot edit.
