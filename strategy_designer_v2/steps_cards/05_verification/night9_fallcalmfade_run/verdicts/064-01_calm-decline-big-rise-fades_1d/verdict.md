---
plan: 064-01_calm-decline-big-rise-fades_1d
idea: 064-01_calm-decline-big-rise-fades
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction 3-bar excess return on case bars: -0.0225219; t of the mean, cases of one day pooled: -1.4182 (threshold: mean > 0 with t >= 2 on at least 30 cases (confirm); mean < 0 with t <= -2 on at least 30 cases (reject))
- Supporting check: Pearson correlation of abs(forecast) with short-direction excess return: -0.244902, passed: False
- Counts: cases: 62, days: 46
- Decided by: The t lies between -2 and 2.
- Reading: Situation = rise in swings >= 2 (recorded raw value, else from prices) and 60-bar price change below -10 % where the window holds 60 bars, with the detector's regime mean_reversion standing for the calm profile (365-bar vol percentile not recomputable); a case is the first bar of each 3-bar grid cell (positions 0,3,6,... per window) with regime mean_reversion and forecast < 0 whose close[t+3] lies in the same window; the normal drift is the mean of the coin's non-overlapping 3-bar grid returns over all its windows; the day-pooled t sums the cases' deviations per UTC day (standard error sqrt(sum of squared day sums)/n).
- Size: unusual move -2.25 % (t -1.42, the cases of one day together: 46 days) per case over 3 bars, -0.283 of the coin's usual move (7.96 %); normal drift in its direction -0.41 %, total -2.66 %; 62 cases
Plan: `steps_cards/03_test_plan/night9_fallcalmfade_run/plans/064-01_calm-decline-big-rise-fades_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/backtests/064-01_calm-decline-big-rise-fades_1d`
Measure: `measure.py`
