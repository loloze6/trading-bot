---
plan: 031-03.g1.b1.g2_swelling-volume-after-rises_1d
idea: 031-03.g1.b1.g2_swelling-volume-after-rises
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 14-bar excess forward return on forecast, trending grid bars: 0.00337961; slope t, clustered by day: 2.0746 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; else inconclusive)
- Supporting check: none
- Counts: grid cases in the regime: 1207, grid cases with forecast above 0: 655, days of the regime grid cases: 167
- Decided by: Confirm rule: the slope is positive with t >= 2.
- Reading: Situation taken as 14-bar close change > 0 with the 14/30 volume ratio above 1 (recorded vol_swell raw value, recomputed from volume where missing), expected side long, active bars whose 14-bar change cannot be computed inside the window are left out of the agreement; the grid is positions 0,14,28,... of each window, kept when regime is 'trending' and the 14-bar forward return lies inside the window, the coin's mean 14-bar return is taken over all its windows' grid bars, and the slope's t uses standard errors clustered by calendar day (UTC).
- Size: unusual move +2.46 % (t 2.45, the cases of one day together: 665 days) per case over 14 bars, 0.099 of the coin's usual move (20.98 %); normal drift in its direction +2.51 %, total +4.97 %; 1091 cases
Plan: `steps_cards/03_test_plan/night6_longreversal_run/plans/031-03.g1.b1.g2_swelling-volume-after-rises_1d.md`
Record: `steps_cards/04_backtest/night6_longreversal_run/backtests/031-03.g1.b1.g2_swelling-volume-after-rises_1d`
Measure: `measure.py`
