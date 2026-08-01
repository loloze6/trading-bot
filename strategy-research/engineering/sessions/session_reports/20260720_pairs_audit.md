# Dispatch M — Independent audit of e3bcbb0 + the fee-isolation pair numbers

**Role:** Independent read-only auditor. Every number below re-derived from
git, code, and on-disk run artifacts — not from the implementer's own session
reports.

## Precondition manifest

- `git log --oneline -1` → `e3bcbb0 Add --commission-bps explicit override
  flag to run_protocol.py` — subject matches, MATCH.
- `git status --porcelain` → only untracked session-report `.md` files —
  MATCH.
- Proceeded.

## Step 1 — PRIMARY: run_028's zero trades at 4h — real sparsity or silent defect?

**Verdict: REAL SPARSITY, confirmed with an explicit mechanism — not a silent
engine defect.**

Checked, in order, exactly what the dispatch asked to rule out:

**(a) Is 4h candle construction itself broken?** Loaded
`legA_10bps`'s 2024-08 window `bars.csv` (190 rows) and checked timestamp
spacing and OHLC internal consistency directly:
`unique timestamp diffs = {14400.0}` (perfectly uniform 4h spacing, no gaps/dupes)
and `0/190` rows with an OHLC violation (low ≤ open/close ≤ high held for
every bar). These bars also match the current on-disk cache
(`trading-bot/local_data/SOLUSDT_4h.csv`), independently cross-checked in
Dispatch J. **4h candle building/aggregation is not defective.**

**(b) Are forecasts/regime scores uniformly zero/frozen (the defect
signature), or do they vary but simply not cross the gate (real sparsity)?**
Pulled `debug_info.regime_scores.trending` (the regime detector's raw,
continuous score, pre-threshold) across every bar in every one of
`legA_10bps`'s 11 windows:

| window | n bars | max regime score | regime ever != "unknown"? |
|---|---|---|---|
| 2024-01 | 190 | 0.1696 | no |
| 2024-02 | 178 | 0.3359 | no |
| 2024-03 | 190 | 0.2602 | no |
| 2024-04 | 184 | 0.1684 | no |
| 2024-05 | 190 | **0.3471** | no |
| 2024-06 | 184 | 0.1956 | no |
| 2024-07 | 190 | 0.3131 | no |
| 2024-08 | 190 | 0.2992 | no |
| 2024-09 | 184 | 0.1926 | no |
| 2024-10 | 190 | 0.3171 | no |
| 2024-11 | 184 | 0.3283 | no |

The score is never frozen or NaN — it varies continuously bar-to-bar (sampled
values include 0.0113, 0.0205, 0.0727, 0.1455, 0.2989... — a live, moving
signal, the opposite of a degenerate/frozen computation) — but it never once
crosses the regime detector's `min_score: 0.4` gate (`candidate_strategy_config.json`:
`regime_detector.mode: "score_product", min_score: 0.4`) across all 11
windows. Closest approach: **2024-05-19 00:00:00**, `close=174.32`,
`regime_scores.trending=0.3471`, `regime=unknown`, `forecast=0.0` — a real bar
with a real (elevated, near-miss) score that still falls 0.053 short of the
gate, so the strategy never activates and no trade results. This is the
sample bar the dispatch asked for.

**Mechanism:** the regime detector's ER/VR components use fixed **bar-count**
parameters (`EfficiencyRatioRegimeComponent(period=24, smooth_period=5)`,
`VarianceRatioComponent(k=5, window=100)`) — unchanged from when this config
was built and evidently tuned against 1h data. At 4h, the same bar counts span
4× the calendar time (24 bars = 4 days at 1h vs 16 days at 4h; a 100-bar VR
window = ~4 days at 1h vs ~16.7 days at 4h). This mechanically smooths the
efficiency/variance-ratio inputs, compressing the regime score's range well
below the 0.4 gate that was calibrated against the 1h cadence (the original
1h-run trades I inspected in the prior Dispatch-J audit showed
`regime_scores.trending` values of 0.42, 0.42, 0.34, 0.39, 0.41 — hovering
right at/above 0.4). This is a real, analytically-explicable consequence of
running an unchanged, bar-count-calibrated regime gate at a 4× coarser
cadence — not a corrupted data pipeline. It does mean the "same" strategy
config tested at 4h is a materially different (much less active) detector
than at 1h, which is a legitimate research finding in its own right, distinct
from either "genuine cost-driven sparsity" or "engine bug."

## Step 2 — Flag diff

`git show e3bcbb0` touches exactly 2 files: `strategy-research/tools/run_protocol.py`
and the new `strategy-research/tests/test_run_protocol_commission_bps_flag.py`.
`_resolve_commission_rate()`: `if commission_bps is not None: return
float(commission_bps)/10000.0; return _commission_rate_for_symbol(symbol,
cost_model, product=product)` — absent-flag path falls through unchanged to
the already-audited (Dispatch J) `_commission_rate_for_symbol`, byte-identical
to pre-existing behavior. `--commission-bps` takes precedence whenever set,
regardless of `--cost-product`'s value (verified by direct read, both branches
of the `if` are mutually exclusive and the override branch never consults
`cost_model`/`product` at all). A single `print(...)` log line fires only
when `args.commission_bps is not None`, stating both the flag value and the
resolved rate. Conversion is `/10000.0`, identical to the already-audited
perp/spot path. **CONFIRMED.**

## Step 3 — Pair integrity, re-derived

Read `manifest.json` for the first window of every leg directly:

| run | leg | timeframe | start | end | bar_count | config_sha256 |
|---|---|---|---|---|---|---|
| run_028 | legA_10bps | 14400s | 2023-11-27 | 2024-02-01 20:00 | 402 | `67a51ac2...` |
| run_028 | legB_5bps | 14400s | 2023-11-27 | 2024-02-01 20:00 | 402 | `67a51ac2...` |
| run_030 | legA_10bps | 14400s | 2023-11-27 | 2024-02-01 20:00 | 402 | `cb671e80...` |
| run_030 | legB_5bps | 14400s | 2023-11-27 | 2024-02-01 20:00 | 402 | `cb671e80...` |

Identical timeframe, window boundaries, and config hash within each pair.
**CONFIRMED** — this pair design fixes the confound Dispatch J found in the
prior (perp-vs-original) comparison.

Recomputed commission/notional directly from `run_030`'s real `trades.json`
(both legs, first 3 trades each, entry and exit independently):

| leg | trade | side | entry_commission/entry_notional | exit_commission/exit_notional |
|---|---|---|---|---|
| legA_10bps | 1 | LONG | 0.00100100 | 0.00100000 |
| legA_10bps | 2 | LONG | 0.00100100 | 0.00100000 |
| legA_10bps | 3 | SHORT | 0.00100000 | 0.00100100 |
| legB_5bps | 1 | LONG | 0.00050025 | 0.00050000 |
| legB_5bps | 2 | LONG | 0.00050025 | 0.00050000 |
| legB_5bps | 3 | SHORT | 0.00050000 | 0.00050025 |

legA resolves to **0.001** (10bps) per leg, legB to **0.0005** (5bps) per leg,
both LONG and SHORT, exactly as expected. (The 0.00100100 vs 0.00100000 split
is which price — entry vs exit — each commission is computed against, not
error.) **CONFIRMED.**

## Step 4 — Deltas table, re-derived (from protocol_summary.json / manifest.json, not the report)

**run_028** (both legs): every one of 11 windows has `trade_count=0`,
`sharpe=None`, `cost_drag_pct=None` in both legA and legB. `per_symbol_summary`
self-reports `median_sharpe: null` in both. Verdict logic
(`run_protocol.py`'s `_kill`: `if median_sharpe is None: return False`; same
guard in `_promote`) falls through to `"refine"` for both legs, reason
`"median_sharpe=null (all windows sparse), min_trades=0<20"` — identical text,
both legs. **Refine, both legs — CONFIRMED.**

**run_030** (AVAXUSDT, single symbol):

| leg | per-window sharpes | median (recomputed by hand) | reported median_sharpe | max_abs_drawdown_pct | total trades (sum of 11 windows) |
|---|---|---|---|---|---|
| legA_10bps | -2.112, -2.735, 8.508, -4.716, -0.622, -2.176, -3.108, -4.544, -3.789, -2.171, -4.651 | **-2.735** | -2.735 | 51.533 | **1178** |
| legB_5bps | -1.649, -1.9, 8.884, -4.241, 0.347, -1.32, -2.652, -4.237, -2.892, -1.272, -4.142 | **-1.900** | -1.900 | 49.62 | **1178** |

Medians independently recomputed by sorting each 11-value list and taking the
6th value by hand — both match the tool's self-reported `per_symbol_summary.median_sharpe`
exactly. `cost_drag_pct` dropped in every one of the 11 windows going from
legA to legB (e.g. window 5: 247.14%→110.31%; window 6: 258.39%→116.81%;
window 8: 11.27%→5.67%) — roughly halved, consistent with roughly halving the
fee. **1178 = 1178, exact.**

Kill-threshold logic (`run_protocol.py`, `_kill(s): return
p["median_sharpe"] < promo["kill_median_sharpe_lt"]`, then `elif
all(_kill(s) for s in symbols): verdict = "kill"`) is generic, pre-existing
code — not written or special-cased for this pair. Both -2.735 and -1.900 are
below the registered `kill_median_sharpe_lt` (-1), so both legs verdict
**kill**, reason text `"...median_sharpe=-2.735<-1"` / `"...median_sharpe=-1.900<-1"`
respectively (verified directly against `protocol_summary.json`, not the
narrative report). **Kill, both legs — CONFIRMED.**

## Step 5 — Suites + hygiene

- `strategy-research/tests/` (`pytest tests/`, no `-m` filter): **328 passed**,
  no skips, no failures.
- `git show e3bcbb0` adds exactly 9 `def test_...` functions to the new file,
  one of which (`test_commission_bps_flag_recomputes_from_real_trades`) is
  `@pytest.mark.parametrize("bps,expected_rate", [(10.0, 0.001), (5.0,
  0.0005)])`, collecting as 2 test IDs — 9 source functions → 10 collected
  tests. 328 (measured) − 10 (new) = 318, exactly matching the prior audit's
  (Dispatch J) independently-measured baseline. No pre-existing test file was
  touched by this commit (`git show e3bcbb0 --name-only` lists only the new
  test file and `run_protocol.py`) and no test was removed or skipped.
  **CONFIRMED.**
- `trading-bot/` suite (`pytest -m ""`): **44 passed, 4 errors** — identical,
  pre-existing `test_regression_backtest.py` errors, unaffected (this commit
  touches nothing under `trading-bot/`). **CONFIRMED.**
- `git show e3bcbb0 --name-only` contains zero matches for `trades.json` or
  any `runs/` path (grep exit 1). **CONFIRMED not committed.**
- `git status --porcelain` before I ran anything showed only the standing
  untracked session-report `.md` files — the implementer left the tree clean.
  (Running the audit's own pytest invocations reproduced the same
  hardcoded-path `trading-bot/results/trades.json` side effect flagged in
  Dispatch D/J — reverted via `git checkout --` before filing this report, to
  restore the precondition state.) **CONFIRMED.**

## Verdict

| Step | Result |
|---|---|
| 1 (run_028 zero-trade mechanism) | **CONFIRMED — real sparsity**, explicit mechanism shown (regime score continuously varying, never crossing 0.4 gate; 4h candles verified non-defective) |
| 2 (flag diff) | CONFIRMED |
| 3 (pair integrity + commission recompute) | CONFIRMED |
| 4 (deltas table + pass-rule + 1178=1178) | CONFIRMED |
| 5 (suites + hygiene) | CONFIRMED |

Unlike Dispatch J's audit of the prior (perp-vs-original) comparison — which
failed because the two sides silently ran at different candle intervals —
this fee-isolation pair design holds timeframe, window set, and strategy
config fixed within each pair and only varies the commission rate, and every
artifact-level check confirms that isolation held in practice. run_028's
zero-trade result at 4h is real (if severe) signal sparsity given its
regime detector's bar-count-calibrated parameters, not an engine defect, and
is consistent between both legs (0 trades at both 10bps and 5bps, so the
fee-isolation pair itself is not confounded by this — it simply demonstrates
the signal doesn't fire at 4h regardless of cost). run_030's kill verdict is
reproduced independently at both fee levels with exactly matching trade
counts (1178=1178) and hand-recomputed medians.

**AUDIT PASS** (numbers ratifiable).
