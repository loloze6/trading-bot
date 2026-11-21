---
plan: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-rebounds-next-day_1h
idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-rebounds-next-day
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess 24-bar return on forecast (regime bars, pooled): 0.000148871; OLS slope t: 2.68289 (threshold: confirm: t >= 2 and mean excess on forecast>0 bars > 0; reject: t <= -2)
- Supporting check: mean excess 24-bar return on forecast > 0 bars: 0.000539743, passed: True
- Counts: regime bars with a full 24-bar forward return: 17280, regime bars with forecast > 0: 8580
- Decided by: The slope's t is 2 or more and the mean excess return on forecast > 0 bars is above 0.
- Reading: Situation bars are those whose close (timestamp + 1h) is at 20:00 UTC with a negative 24-bar return (recorded raw value, else recomputed from closes), expected side long; regime bars are those with regime == 'mean_reversion'; forward returns use row offsets inside each window; the coin's mean 24-bar return uses the non-overlapping grid 0, 24, 48, ... of each window pooled over all windows; t is the OLS slope over its standard error; the plan's minimum counts lead to 'not observable'.
- Size: unusual move +0.09 % per case over 24 bars, 0.019 of the coin's usual move (4.87 %); normal drift in its direction +0.14 %, total +0.23 %; 7307 cases
Plan: `steps_cards/03_test_plan/d_line_1h_run/plans/016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-rebounds-next-day_1h.md`
Record: `steps_cards/04_backtest/d_line_1h_run/backtests/016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-rebounds-next-day_1h`
Measure: `measure.py`
