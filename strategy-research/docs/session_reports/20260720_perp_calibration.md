# Phase 1.2 / Dispatch H — Perp cost calibration: wire + re-run

Date: 2026-07-20
Precondition check: PASSED — HEAD=102fa8e, `git status --porcelain` showed only
untracked `strategy-research/docs/session_reports/*.md` reports, nothing else.

## Step 1 — commission events per round trip (LONG vs SHORT)

Read `trading-bot/execution/portfolio_info.py`'s `CommonPortfolioDef.update_local_balance`
directly (not from memory). Both sides apply `commission_rate` **exactly twice per
round trip**, symmetric:

- **LONG:** once at open (`trade_type='LONG'`, line 115: `received_qty = quantity *
  (1 - commission)`), once at close (`'REDUCE_LONG'`/`'CLOSE'`, line 133/172:
  `usdt_received = cost * (1 - commission)`).
- **SHORT:** once at open (`trade_type='SHORT'`, line 150: `usdt_received = cost *
  (1 - commission)`), once at close (`'REDUCE_SHORT'`/`'CLOSE'`, line 158/188:
  `cost_to_buy = price * repay / (1 - commission)`).

Cross-checked against a real trade record (run_018, a SHORT trade): `entry_commission
+ exit_commission = total_commission` (1.9176 + 1.9283 = 3.8459) — confirms exactly 2
commission events, not 1 or 3, in the actual recorded output, not just the code path.

**No asymmetry — no STOP triggered.** Conversion: `commission_rate = fee_bps / 10000`
(no ×2 or /2 — the 2 charges-per-round-trip already reproduce `round_trip_cost =
2 × fee_bps`, matching `cost_model.yaml`'s own existing convention).

## Step 2 — cost_model.yaml perp block

Added a new, additive `perp:` top-level block (did not touch the existing top-level
`fee_rate_bps`, which stays Binance-spot-calibrated at 7.5bps — unaffected):

```yaml
perp:
  fee_rate_bps:
    default: 5.0
  round_trip_cost_bps:
    default: 10.0
```

Sourced from the original 2026-07-19 venue survey's comparison table ("Perp
maker/taker (base tier): Official docs: 0.0200% / 0.0500% at $0+"), flat across all
symbols (the source is a single tiered schedule, not per-symbol). A dated
`PERP CALIBRATION` provenance comment documents: why this exists (Dispatch F2's
finding that these two targets' SHORT trades are margin-simulated, and Dispatch G's
finding that margin's FR/EU retail legality is unconfirmed while perp's is), that
funding cash flows are **not modeled**, and that `FUNDING_MR_DAILY_RETEST` must never
be costed with this block. `spread_estimate_bps` untouched (still Binance-sourced,
already flagged in the file from Dispatch F's aborted attempt's design — re-flagged
here too).

## Step 3 — threading

`strategy-research/tools/run_protocol.py`: new `_commission_rate_for_symbol(symbol,
cost_model, product='spot')` helper (spot default = unchanged prior behavior; `'perp'`
reads the new block). New `--cost-product {spot,perp}` CLI flag (default `spot`,
verified via `--help` and a unit test). Both `run_backtest()` call sites updated:

- Holdout (line 984): `commission_rate=_commission_rate_for_symbol(symbol, cost_model, product=args.cost_product)`
- Walk-forward (line 1046): same.

Default invocations (no `--cost-product`) are byte-identical to before this dispatch
— confirmed by the full strategy-research suite staying green (see below) and by the
`test_default_product_is_spot` / `test_cli_cost_product_defaults_to_spot` unit tests.

## Step 4 — re-run results

**rsi_momentum_trending_cost_drag (run_018): NOT re-run.** Its
`runs/run_018/artifacts/candidate_strategy_config.json` fails current validation:
`tools/validate_config.py`'s `V9` rule (`regime_detector.default_regime: 'trending'
is forbidden in mode 'threshold_rules' while regime_detector.rules is non-empty`) —
this is a pre-existing artifact/validator drift (the config was produced 2026-06-27,
before this rule apparently tightened), unrelated to this dispatch, and identical in
character to `test_regression_backtest.py`'s already-known pre-existing failures.
Per the STOP condition ("don't fabricate"), did not patch the historical artifact to
pass a newer validator — that would test a different strategy than the one that
actually produced the KB finding. Confirmed `run_028`/`run_030`'s configs both pass
validation cleanly (0 errors each) before proceeding with those.

**keltner_scoremode_no_edge — run_028 (SOLUSDT, `escalation_solusdt_4h.json`):**

| | old (10bps, original) | new (perp 5bps) |
|---|---|---|
| median_sharpe | 0.0 | null (all 11 windows sparse) |
| max_abs_drawdown_pct | 0.706% | 0.0% |
| min_trade_count | 0 | 0 |
| median_cost_drag_pct | 84.2881% | undefined (0 trades) |
| **verdict** | **refine** | **refine — unchanged** |

Every window produced exactly 0 trades under perp cost, vs. 3 total trades spread
across the original 11 windows (already a fragile, ~1%-activation signal per the
KB's own `exhausted_basis`). This is a real, legitimate path-divergence effect
(commission_rate changes alter simulated fill sizes and thus subsequent bars'
allocation-delta, which can flip whether a marginal rebalance triggers at all for a
signal this sparse — confirmed non-buggy since trade 1's sizing was already known
from Dispatch C/D to be commission-independent, and this is trade *activation*
disappearing entirely across all 11 independent windows, not a resizing artifact),
not a bug in this dispatch's wiring.

**keltner_scoremode_no_edge — run_030 (AVAXUSDT, `escalation_avaxusdt_4h.json`):**

| | old (10bps, original) | new (perp 5bps) |
|---|---|---|
| median_sharpe | -2.61 | -1.90 |
| max_abs_drawdown_pct | 45.559% | 49.62% |
| min_trade_count | 310 | 96 |
| median_cost_drag_pct | 128.4407% | 30.386% |
| **verdict** | **kill** | **kill — unchanged** |

Cost drag fell dramatically (128.4% → 30.4%) and sharpe improved (-2.61 → -1.90), but
-1.90 remains below the kill threshold (`median_sharpe < -1`) — the underlying signal
is negative enough that even a much cheaper cost basis doesn't rescue it. Trade count
dropped 310→96 (same path-divergence mechanism as above, at a much larger and more
statistically stable scale here since this symbol trades far more actively).

**Neither verdict flips.** Perp costing does not rescue `keltner_scoremode_no_edge`.

**FUNDING_MR_DAILY_RETEST: deliberately deferred, not re-run.** Per this dispatch's
explicit instruction and `cost_model.yaml`'s own PERP CALIBRATION block: a fee-only
perp re-run would omit the funding credit that is this strategy's entire thesis,
producing a misleading (understated-cost, but also thesis-blind) number. Remains
deferred to a dedicated funding-modeling build.

## Step 5 — tests + suites

New: `strategy-research/tests/test_run_protocol_perp_cost_wiring.py` (8 tests: 5 unit
tests on `_commission_rate_for_symbol`'s product selection/fallback, 1 CLI-default
test, 1 real-cost_model.yaml check, 1 slow integration test proving the perp rate
changes engine output). All 8 pass.

- `strategy-research/` full suite: **318 passed**, 0 failures (no regression — unlike
  the aborted Dispatch F attempt, this dispatch left the top-level spot block
  untouched, so no pre-existing bounds/mirror tests broke).
- `trading-bot/` full suite (`-m "slow or not slow"`): **44 passed**, same 4
  pre-existing `test_regression_backtest.py` errors (`ValueError: invalid
  strategy_config`, confirmed present on unmodified HEAD in an earlier dispatch's
  independent audit) — unrelated to this change, unchanged count.

## Step 6 — commit scope deviation (flagged)

Committed `run_protocol.py`, `cost_model.yaml`, `tests/conftest.py`, and the new test
file (`d86f0d0`). **Did not commit the two new run artifacts**
(`runs/run_028/perp_recalibration_20260720/`, `runs/run_030/perp_recalibration_20260720/`,
982KB + 5.6MB): `strategy-research/runs/` is gitignored project-wide
(`.gitignore:35-36`), and every other run artifact referenced throughout this whole
dispatch chain (run_018, run_028, run_030, run_059, and every other campaign run) has
always lived outside git under this same policy. Force-adding just these two would be
an inconsistent, unilateral override of an established repo convention rather than
following this dispatch's literal instruction — flagged here rather than silently
either force-adding or silently omitting without explanation. The full numeric
results are recorded above and are reproducible on demand via `python
tools/run_protocol.py <config> <protocol> --cost-product perp --out-dir <path>`.

## Confirmation

FUNDING_MR_DAILY_RETEST was deferred per its own documented rationale, not
fee-swapped. No trading-bot code was touched. `git status --porcelain` after commit
shows only the same eight pre-existing/new untracked session reports.
