---
plan: 031-03.g1.b1.g2_swelling-volume-after-rises_1d
idea: 031-03.g1.b1.g2_swelling-volume-after-rises
fit: adapted
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 14-bar excess forward return on forecast, trending grid bars: 0.00662755; slope t, clustered by day: 1.1234 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; else inconclusive)
- Supporting check: none
- Counts: grid cases in the regime: 126, grid cases with forecast above 0: 75, days of the regime grid cases: 48
- Decided by: Minimum count not reached: only 75 grid cases with forecast above 0 (minimum 100); only 126 grid cases in the regime (minimum 200).
- Reading: Situation taken as 14-bar close change > 0 with the 14/30 volume ratio above 1 (recorded vol_swell raw value, recomputed from volume where missing), expected side long, active bars whose 14-bar change cannot be computed inside the window are left out of the agreement; the grid is positions 0,14,28,... of each window, kept when regime is 'trending' and the 14-bar forward return lies inside the window, the coin's mean 14-bar return is taken over all its windows' grid bars, and the slope's t uses standard errors clustered by calendar day (UTC).
- Size: unusual move -0.45 % (t -0.10, the cases of one day together: 84 days) per case over 14 bars, -0.041 of the coin's usual move (32.27 %); normal drift in its direction +14.41 %, total +13.96 %; 104 cases
Plan: `steps_cards/03_test_plan/night6_longreversal_run/plans/031-03.g1.b1.g2_swelling-volume-after-rises_1d.md`
Record: `steps_cards/04_backtest/night6_longreversal_run/unseen_2016_2017/backtests/031-03.g1.b1.g2_swelling-volume-after-rises_1d`
Measure: `measure.py`
