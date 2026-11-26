---
plan: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal_1d
idea: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS t of the slope of excess forward 3-bar return on forecast: -4.43159e-05; OLS slope t: -0.0743707 (threshold: confirm: t >= 2 with supporting check > 0; reject: t <= -2; else inconclusive)
- Supporting check: mean sign(forecast) x excess 3-bar return over the top 20% |forecast| cases: -0.0068109, passed: False
- Counts: independent cases: 255, cases in top-20% group: 51
- Decided by: The slope's t is between -2 and 2.
- Reading: Cases are grid bars (positions 0,3,6,... per window) with regime 'mean_reversion', non-zero forecast and a full 3-bar forward return in the window; the coin's mean 3-bar return is the mean over all grid bars of all its windows; the regression is pooled across coins; the top-20% group is the ceil(20% of cases) largest |forecast|.
- Size: unusual move +0.41 % (t 0.55, the cases of one day together: 203 days) per case over 3 bars, 0.020 of the coin's usual move (10.22 %); normal drift in its direction -0.21 %, total +0.20 %; 246 cases
Plan: `steps_cards/03_test_plan/night_005_run/plans/005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal_1d.md`
Record: `steps_cards/04_backtest/night_005_run/unseen_2016_2017/backtests/005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal_1d`
Measure: `measure.py`
