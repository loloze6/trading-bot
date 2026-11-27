---
plan: 041-01.b1.b1_rise-continuation-more-coins_1d
idea: 041-01.b1.b1_rise-continuation-more-coins
fit: adapted
status: no effect
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean next-day excess return (over coin's all-window mean daily return): 0.00254818; t of weighted mean, cases of one day summed: 0.811642 (threshold: confirm: positive with t >= 2 and slope > 0; reject: negative with t <= -2)
- Supporting check: OLS slope of next-day excess return on forecast: 0.000637477, passed: True
- Counts: cases: 1273, distinct days: 758
- Decided by: The t lies between -2 and 2, which the plan calls inconclusive. No effect (common/verdicts.md): t in the idea's direction +0.812 (below 1), 1273 cases (30 needed).
- Reading: The coin's mean daily return is the mean of all its within-window daily returns, the t uses day-clustered deviations of the weighted mean (forecast-weighted, summed per UTC day), the profile is read from the recorded regime (not chop), and the plan's minimum of 100 cases and 100 days is applied as 'not observable'.
- Size: unusual move +0.12 % (t 0.44, the cases of one day together: 529 days) per case over 1 bars, 0.030 of the coin's usual move (5.25 %); normal drift in its direction +0.11 %, total +0.23 %; 830 cases
- Effect check (common/verdicts.md): no effect: t in the idea's direction +0.812 (below 1), 1273 cases (30 needed)
Plan: `steps_cards/03_test_plan/pilot_a4_named_run/plans/041-01.b1.b1_rise-continuation-more-coins_1d.md`
Record: `steps_cards/04_backtest/pilot_a4_named_run/backtests/041-01.b1.b1_rise-continuation-more-coins_1d`
Measure: `measure.py`
