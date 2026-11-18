---
plan: N2-04_slow-and-fast-momentum.e1_short-horizon-dual-momentum-continuation_1d
idea: N2-04_slow-and-fast-momentum.e1_short-horizon-dual-momentum-continuation
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean forward 5-bar excess over holding the coin, active bars: 0.0150489; t of the mean: 1.36874 (threshold: confirm: mean > 0 with t >= 2 (and supporting check > 0); reject: mean < 0 with t <= -2)
- Supporting check: mean 5-bar excess / 5 minus mean 20-bar excess / 20: 0.00253683, passed: True
- Counts: active non-overlapping 5-bar cases: 310, active non-overlapping 20-bar cases: 74
- Decided by: The t of the mean 5-bar excess lies between -2 and 2, which the plan calls inconclusive.
- Reading: Situation recomputed from closes (20- and 60-bar returns > 0) where the window holds 60 prior bars, otherwise taken from the detector's regime == 'trending' (the detector's own components are not recorded); active = forecast > 0 on each window's grid at positions 0, h, 2h, ... with a full h-bar forward return inside the window; holding-the-coin mean = the coin's mean h-bar return over all its grid bars in all windows; the plan's 'fewer than 100 cases' is reported as 'not observable' per the workflow.
Plan: `steps_cards/03_test_plan/validation_run/plans/N2-04_slow-and-fast-momentum.e1_short-horizon-dual-momentum-continuation_1d.md`
Record: `steps_cards/04_backtest/unseen_run/unseen_2016_2017/backtests/N2-04_slow-and-fast-momentum.e1_short-horizon-dual-momentum-continuation_1d`
Measure: `measure.py`
