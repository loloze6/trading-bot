---
plan: 047-03_falling-agitated-scaled-rise-giveback_1d
idea: 047-03_falling-agitated-scaled-rise-giveback
fit: exact
status: no effect
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of next-day excess return on abs(forecast), short bars: -0.000313915; slope t (day-clustered): -0.744697 (threshold: confirm if slope t <= -2 (with mean excess < 0); reject if slope t >= +2)
- Supporting check: mean next-day excess return on short bars: -0.00320783, passed: True
- Counts: short bars: 1118, distinct days: 492
- Decided by: The slope's t is between -2 and +2. No effect (common/verdicts.md): t in the idea's direction +0.745 (below 1), 492 cases (30 needed).
- Reading: Profile bars are those with regime 'unknown' (the detector's only non-vetoed regime, i.e. falling and agitated), up days are a positive raw scaled return (price change when unrecorded), every short bar with a next close in its window is used (1-bar horizon grid), and the slope's t uses cluster-robust (CR1) standard errors clustered by UTC day.
- Size: unusual move +0.37 % (t 1.36, the cases of one day together: 364 days) per case over 1 bars, 0.074 of the coin's usual move (4.92 %); normal drift in its direction -0.06 %, total +0.31 %; 749 cases
- Effect check (common/verdicts.md): no effect: t in the idea's direction +0.745 (below 1), 492 cases (30 needed)
Plan: `steps_cards/03_test_plan/night10_fallagishort_run/plans/047-03_falling-agitated-scaled-rise-giveback_1d.md`
Record: `steps_cards/04_backtest/night10_fallagishort_run/backtests/047-03_falling-agitated-scaled-rise-giveback_1d`
Measure: `measure.py`
