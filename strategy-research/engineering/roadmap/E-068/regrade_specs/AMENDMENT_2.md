# Amendment 2: the analytic p-value failed the gate; switch to the fallback

Written and committed 2026-10-03, **before any re-grade result was computed**
and before the fallback was built or calibrated. This follows the operator's
rule in amendment 1, section B: "if any cell fails, switch to the fallback."

## The gate result for `block_analytic_v1` (400 simulations per cell)

Full numbers: `engineering/roadmap/E-068/calibration_block_analytic_v1.yaml`.
Each cell shows the share of one-sided p < 0.05, horizons left to right. Pass
means every value is in [0.025, 0.075].

| Cell | Values | Result |
|---|---|---|
| daily, iid, forecast >= 12, greater | 0.030 0.025 0.013 0.007 0.005 | FAIL (too strict) |
| daily, iid, forecast >= 12, less | 0.062 0.048 0.040 0.033 0.028 | pass |
| daily, iid, forecast <= -12, greater | 0.058 0.033 0.020 0.010 0.013 | FAIL |
| daily, iid, forecast <= -12, less | 0.033 0.028 0.028 0.025 0.020 | FAIL |
| daily, garch, forecast >= 12, greater | 0.035 0.020 0.022 0.018 0.013 | FAIL |
| daily, garch, forecast >= 12, less | 0.062 0.037 0.025 0.022 0.025 | FAIL |
| daily, garch, forecast <= -12, greater | **0.090** 0.068 0.048 0.050 0.043 | FAIL (too loose at h=1) |
| daily, garch, forecast <= -12, less | 0.045 0.028 0.020 0.015 0.005 | FAIL |
| hourly, iid and garch, rank IC, both directions | 0.000 at 72, 168 and 336 | FAIL (far too strict) |

**Why it fails:**
- **Hourly:** a block of h bars over-counts the dependence when the signal's
  memory (about 20 bars) is shorter than the horizon (72-336 bars).
- **Daily:** the normal approximation on a few dozen blocks is unreliable in
  both directions.

As the operator required, the block size is **not** retuned.

## B2. The fallback: `bootstrap_null_v1`

This is the null built from shuffled prices, with the signal recomputed. All of
it is fixed here.

1. **The real statistic** uses the saved forecast and the saved closes, as before.

2. **Fake windows.** For each window, the window's own bars are cut into units.
   - A unit is the log return from the previous close, `log(high / close)` and
     `log(low / close)`.
   - Units are redrawn in circular blocks of `B` bars, with replacement.
     B = 5 for daily bars and 24 for hourly bars.
   - A price path is rebuilt from the last real close before the window. The
     real timestamps are kept.

3. **Recomputed signal.** The forecast is recomputed on (real warm-up history +
   the fake window).
   - It uses the variant's own `strategy_config.json` component and parameters.
   - Only a single component with an identity transform and weight 1 is
     accepted; anything else is refused.
   - The engine clip of +-20 is applied.
   - The code is a vectorized copy of `update()`, proven equal by a test (max
     difference measured at 2.5e-14). Calling `update()` bar by bar would need
     about 50 million calls.

4. **Warm-up history** comes from the data cache that the runs used:
   `trading-bot/local_data/kraken_<SYMBOL>_<1d|1h>.csv`, in the main checkout.
   - It is read only.
   - Only rows before the window's first bar are kept: 30 bars for daily, 500
     for hourly (the EMA start-up effect is gone after 500 bars).
   - Reading stops at the window's start, so no later row is parsed.
   - The holdout store is never touched, and no row is printed.

5. **Check before grading.** The forecast recomputed on the REAL path must equal
   the saved forecast. The maximum absolute difference is reported per window.
   If it is above 1e-6 for Donchian or 0.05 for Keltner, grading stops with an
   error. This check reads prices and forecasts only, never outcomes.

6. **p-value.** One-sided `p = (1 + #{fake >= real}) / (1 + N)` on the
   claim-oriented statistic. N = 1,000 for the re-grade, seed 20261003.

7. **Supported selectors:** those whose input can be recomputed (forecast,
   close, calendar, `all`). The regime selectors are refused under this method,
   because the regime labels cannot be recomputed on fake prices.

## B3. Gate for the fallback (same rule as amendment 1, section B)

- Same simulated prices (iid and GARCH), the same real signals, and 400
  simulations per cell.
- Warm-up comes from the simulated history.
- Each simulation uses N = 199 fake windows (p resolution 0.005).
- Both directions are read from the same simulations.
- **Pass:** every value is in [0.025, 0.075].
- If the fallback also fails, the re-grade stops and goes back to the operator.
