---
plan: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal_1d
idea: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal
fit: adapted
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS t of the slope of excess forward 3-bar return on forecast: -0.000517174; OLS slope t: -1.25109 (threshold: confirm: t >= 2 with supporting check > 0; reject: t <= -2; else inconclusive)
- Supporting check: mean sign(forecast) x excess 3-bar return over the top 20% |forecast| cases: -0.0191993, passed: False
- Counts: independent cases: 79, cases in top-20% group: 16
- Decided by: Minimum count not reached: 79 independent cases (100 needed) and 16 in the top-20% group (20 needed).
- Reading: Cases are grid bars (positions 0,3,6,... per window) with regime 'mean_reversion', non-zero forecast and a full 3-bar forward return in the window; the coin's mean 3-bar return is the mean over all grid bars of all its windows; the regression is pooled across coins; the top-20% group is the ceil(20% of cases) largest |forecast|.
- Size: unusual move -0.34 % (t -0.58, the cases of one day together: 47 days) per case over 3 bars, -0.069 of the coin's usual move (4.64 %); normal drift in its direction -0.06 %, total -0.40 %; 76 cases
Plan: `steps_cards/03_test_plan/night_005_run/plans/005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal_1d.md`
Record: `steps_cards/04_backtest/night_005_run/unseen_2026/backtests/005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal_1d`
Measure: `measure.py`
