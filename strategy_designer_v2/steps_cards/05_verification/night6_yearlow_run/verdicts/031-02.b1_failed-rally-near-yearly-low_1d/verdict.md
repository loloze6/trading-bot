---
plan: 031-02.b1_failed-rally-near-yearly-low_1d
idea: 031-02.b1_failed-rally-near-yearly-low
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: Pearson correlation of forecast with 20-bar forward excess return (non-overlapping grid, nonzero forecast): 0.0246805; correlation t (n=410): 0.498674 (threshold: confirm: t >= 2 with supporting check passing; reject: t <= -2)
- Supporting check: mean 20-bar excess return on grid bars with forecast <= -2 is below 0: -0.0277078, passed: True
- Counts: grid cases with a nonzero forecast: 410, grid cases with forecast at or below -2: 63
- Decided by: The correlation's t is between -2 and 2 (inconclusive rule).
- Reading: Cases are pooled over all coins and windows on the 0,20,40,... grid of each window; the coin's mean 20-bar return is the mean over that grid on all its bars in all windows; correlation t is r*sqrt((n-2)/(1-r^2)); the 60-day return for the situation check is recomputed from closes where the window has 60 prior bars, else read from the recorded regime; the expected side is the sign of the dist_low standardised value minus 10; the plan's minimum counts, when unmet, give 'not observable'.
- Size: unusual move +4.18 % (t 1.86, the cases of one day together: 220 days) per case over 20 bars, 0.174 of the coin's usual move (21.24 %); normal drift in its direction +0.59 %, total +4.78 %; 283 cases
Plan: `steps_cards/03_test_plan/night6_yearlow_run/plans/031-02.b1_failed-rally-near-yearly-low_1d.md`
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-02.b1_failed-rally-near-yearly-low_1d`
Measure: `measure.py`
