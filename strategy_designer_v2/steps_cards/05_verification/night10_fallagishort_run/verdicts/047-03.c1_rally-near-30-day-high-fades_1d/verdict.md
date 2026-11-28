---
plan: 047-03.c1_rally-near-30-day-high-fades_1d
idea: 047-03.c1_rally-near-30-day-high-fades
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of drift-adjusted 3-day return on abs forecast, over the cases: -0.00081485; OLS slope t: -1.18182 (threshold: slope t <= -2 confirms (with supporting check and >=30 cases on >=30 days); t >= +2 rejects)
- Supporting check: mean unusual move in the short direction > 0: 0.000274108, passed: True
- Counts: cases: 562, distinct days: 288
- Decided by: The slope's t lies between -2 and +2.
- Reading: Up day recomputed from closes and the falling-agitated profile read from the recorded regime (the detector's components are not recorded); a case is the first short bet (forecast rising in size by >= 2 points from its lowest level on the short side since the last bet) in each 3-bar grid cell of each window, and the slope's t is the ordinary OLS t pooled over all coins.
- Size: unusual move +0.03 % (t 0.05, the cases of one day together: 288 days) per case over 3 bars, -0.002 of the coin's usual move (8.38 %); normal drift in its direction -0.18 %, total -0.15 %; 562 cases
- Effect check (common/verdicts.md): unclear: t in the idea's direction +1.182 (not below 1), 562 cases (30 needed)
Plan: `steps_cards/03_test_plan/night10_fallagishort_run/plans/047-03.c1_rally-near-30-day-high-fades_1d.md`
Record: `steps_cards/04_backtest/night10_fallagishort_run/backtests/047-03.c1_rally-near-30-day-high-fades_1d`
Measure: `measure.py`
