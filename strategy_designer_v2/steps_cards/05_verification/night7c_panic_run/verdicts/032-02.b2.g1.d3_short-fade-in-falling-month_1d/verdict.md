---
plan: 032-02.b2.g1.d3_short-fade-in-falling-month_1d
idea: 032-02.b2.g1.d3_short-fade-in-falling-month
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: |forecast|-weighted mean next-day excess fall (short side) on regime bars: 0.00126977; t of the weighted mean, cases of one day pooled: 1.16071 (threshold: confirm: > 0 with t >= 2; reject: < 0 with t <= -2; else inconclusive; at least 100 case-days)
- Supporting check: none
- Counts: case-days: 8831, distinct days: 2218, active bars: 8916
- Decided by: The t lies between -2 and 2 (or its sign disagrees with the mean), which the plan calls inconclusive.
- Reading: The situation is the 20-day return below 0 recomputed from closes inside each window (the recorded regime where fewer than 20 prior bars exist in the window) with a short forecast; case-days are counted as the (coin, day) cases with a non-zero forecast in the trending regime and a next-day return; the day-pooled t sums each day's weighted deviations into one cluster with a D/(D-1) correction; the plan's fewer-than-100 case-days rule is applied as the minimum count giving 'not observable'.
- Size: unusual move +0.24 % (t 1.66, the cases of one day together: 1513 days) per case over 1 bars, 0.051 of the coin's usual move (4.78 %); normal drift in its direction -0.12 %, total +0.12 %; 3744 cases
Plan: `steps_cards/03_test_plan/night7c_panic_run/plans/032-02.b2.g1.d3_short-fade-in-falling-month_1d.md`
Record: `steps_cards/04_backtest/night7c_panic_run/backtests/032-02.b2.g1.d3_short-fade-in-falling-month_1d`
Measure: `measure.py`
