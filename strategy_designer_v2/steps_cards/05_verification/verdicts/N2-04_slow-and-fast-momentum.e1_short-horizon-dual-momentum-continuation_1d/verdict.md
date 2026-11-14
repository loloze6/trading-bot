---
plan: N2-04_slow-and-fast-momentum.e1_short-horizon-dual-momentum-continuation_1d
idea: N2-04_slow-and-fast-momentum.e1_short-horizon-dual-momentum-continuation
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean forward 5-bar excess over holding the coin, active bars: 0.00822748; t of the mean: 2.222 (threshold: confirm: mean > 0 with t >= 2 (and supporting check > 0); reject: mean < 0 with t <= -2)
- Supporting check: mean 5-bar excess / 5 minus mean 20-bar excess / 20: 0.00069485, passed: True
- Counts: active non-overlapping 5-bar cases: 1130, active non-overlapping 20-bar cases: 269
- Decided by: The mean 5-bar excess is positive with t >= 2 and the supporting check is above 0.
- Reading: Situation recomputed from closes (20- and 60-bar returns > 0) where the window holds 60 prior bars, otherwise taken from the detector's regime == 'trending' (the detector's own components are not recorded); active = forecast > 0 on each window's grid at positions 0, h, 2h, ... with a full h-bar forward return inside the window; holding-the-coin mean = the coin's mean h-bar return over all its grid bars in all windows; the plan's 'fewer than 100 cases' is reported as 'not observable' per the workflow.
Plan: `steps_cards/03_test_plan/plans/N2-04_slow-and-fast-momentum.e1_short-horizon-dual-momentum-continuation_1d.md`
Record: `steps_cards/04_backtest/backtests/N2-04_slow-and-fast-momentum.e1_short-horizon-dual-momentum-continuation_1d`
Measure: `measure.py`
