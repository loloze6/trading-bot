---
plan: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal_1d
idea: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS t of the slope of excess forward 3-bar return on forecast: 0.000786044; OLS slope t: 3.7963 (threshold: confirm: t >= 2 with supporting check > 0; reject: t <= -2; else inconclusive)
- Supporting check: mean sign(forecast) x excess 3-bar return over the top 20% |forecast| cases: 0.0132365, passed: True
- Counts: independent cases: 913, cases in top-20% group: 183
- Decided by: The slope's t is 2 or more and the top-20% mean of sign(forecast) x excess return is above 0.
- Reading: Cases are grid bars (positions 0,3,6,... per window) with regime 'mean_reversion', non-zero forecast and a full 3-bar forward return in the window; the coin's mean 3-bar return is the mean over all grid bars of all its windows; the regression is pooled across coins; the top-20% group is the ceil(20% of cases) largest |forecast|.
Plan: `steps_cards/03_test_plan/night_005_run/plans/005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal_1d.md`
Record: `steps_cards/04_backtest/night_005_run/backtests/005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal_1d`
Measure: `measure.py`
