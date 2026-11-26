---
plan: 074-01.b1.b1_falling-wide-up-day-high-close-fade_1d
idea: 074-01.b1.b1_falling-wide-up-day-high-close-fade
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction excess next-day return: 0.00633067; day-clustered t of the mean: 1.37331 (threshold: confirm: >0 with day-clustered t >= 2 (and larger-minus-smaller > 0); reject: <0 with t <= -2)
- Supporting check: larger-|forecast| half minus smaller half mean excess (Welch t 1.904): 0.00966223, passed: True
- Counts: distinct days with cases: 341, cases: 656, larger-forecast half cases: 328, smaller-forecast half cases: 328
- Decided by: Main t between -2 and 2 (or sign and t disagree): neither confirm nor reject.
- Reading: Falling market read as the 60-bar simple return in percent below -10 (the veto at gte -10), recomputed inside each window, and the detector's regime used for it only where 60 bars of history are missing. The range multiple is taken as high-low over its 20-bar mean including the day, or the recorded width where present. Horizon 1, so every bar is on the grid. The day-clustered t uses deviations summed per UTC day with a G/(G-1) correction. The larger half is |forecast| above the median and the smaller half the rest. The plan's 'fewer than 30 distinct days' rule is applied as the minimum count, giving 'not observable'.
- Size: unusual move +0.67 % (t 1.39, the cases of one day together: 312 days) per case over 1 bars, 0.130 of the coin's usual move (5.31 %); normal drift in its direction -0.15 %, total +0.52 %; 606 cases
Plan: `steps_cards/03_test_plan/night9_chopdeep_run/plans/074-01.b1.b1_falling-wide-up-day-high-close-fade_1d.md`
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/074-01.b1.b1_falling-wide-up-day-high-close-fade_1d`
Measure: `measure.py`
