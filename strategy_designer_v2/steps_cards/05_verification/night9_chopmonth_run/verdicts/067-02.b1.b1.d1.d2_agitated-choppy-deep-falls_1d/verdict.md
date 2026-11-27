---
plan: 067-02.b1.b1.d1.d2_agitated-choppy-deep-falls_1d
idea: 067-02.b1.b1.d1.d2_agitated-choppy-deep-falls
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction 21-bar excess move of deep cases (forecast <= -10): 0.0584185; t of the mean, cases summed per day: 1.36502 (threshold: confirm: mean > 0 with t >= 2 and supporting check passed; reject: mean < 0 with t <= -2; at least 20 deep cases)
- Supporting check: deep mean minus shallow mean short-direction excess move (> 0 passes): 0.0317053, passed: True
- Counts: deep cases: 22, days of deep cases: 17, shallow cases: 41, active bars: 1395
- Decided by: The t of the deep cases' mean lies between -2 and 2.
- Reading: Grid bars are positions 0, 21, 42, ... of each window with a full 21-bar return inside it; the coin's drift is the mean of all its grid returns over all its windows; the day t uses per-day sums of deviations from the case mean with a K/(K-1) correction; the situation is a negative raw 30-day return with a negative forecast; fewer than 20 deep cases is reported as not observable.
- Size: unusual move +3.83 % (t 2.44, the cases of one day together: 138 days) per case over 21 bars, 0.080 of the coin's usual move (27.91 %); normal drift in its direction -3.70 %, total +0.14 %; 167 cases
Plan: `steps_cards/03_test_plan/night9_chopmonth_run/plans/067-02.b1.b1.d1.d2_agitated-choppy-deep-falls_1d.md`
Record: `steps_cards/04_backtest/night9_chopmonth_run/backtests/067-02.b1.b1.d1.d2_agitated-choppy-deep-falls_1d`
Measure: `measure.py`
