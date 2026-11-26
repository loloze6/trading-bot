---
plan: 031-02.b1.b1.b1.d2.g1_wide-high-close-downrun-continuation_1d
idea: 031-02.b1.b1.b1.d2.g1_wide-high-close-downrun-continuation
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction 3-bar unusual move per case: 0.00562427; t of the mean, cases clustered by day: 0.764229 (threshold: mean short-direction unusual move > 0 with day-clustered t >= 2 to confirm; < 0 with t <= -2 to reject; at least 30 distinct case days)
- Supporting check: OLS slope of unusual move on raw range multiple: 0.00398556, passed: True
- Counts: cases: 625, cases counted on distinct days: 275
- Decided by: t between -2 and 2, which the plan calls inconclusive.
- Reading: Situation from prices (close[t-1]<close[t-6], range over 20-bar mean range incl. the day >= 1.5 using the recorded width where present, (close-low)/(high-low) >= 0.75), active bars whose 20-bar range mean cannot be computed inside the window are left out of the agreement; cases are short bets (rise of -forecast of >= 2 from its low since the last bet), one per 3-bar grid cell of each window, t clusters deviations by UTC day, and the 30-case minimum is counted on distinct days.
- Size: unusual move +0.56 % (t 0.77, the cases of one day together: 275 days) per case over 3 bars, 0.071 of the coin's usual move (9.14 %); normal drift in its direction -0.48 %, total +0.09 %; 625 cases
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-02.b1.b1.b1.d2.g1_wide-high-close-downrun-continuation_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-02.b1.b1.b1.d2.g1_wide-high-close-downrun-continuation_1d`
Measure: `measure.py`
