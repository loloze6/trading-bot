---
plan: 067-02.b2.b2.d1_choppy-month-fall-week-hold_1d
idea: 067-02.b2.b2.d1_choppy-month-fall-week-hold
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: |forecast|-weighted mean 7-bar unusual move in the short direction: 0.0155944; t of the weighted mean, cases of one day summed (day-clustered): 1.57148 (threshold: confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2; over at least 30 distinct days)
- Supporting check: mean gain before costs on bars held short with forecast 0: -0.000220651, passed: False
- Counts: distinct case days: 211, cases: 633, held-recovered bars: 3444
- Decided by: The t lies between -2 and 2 (or its sign disagrees with the mean), meeting neither confirm nor reject.
- Reading: Situation bars are those with the month_fall component recorded (choppy regime active) and raw 30-day return < 0 with a negative forecast; the drift is each coin's mean 7-bar return on the same non-overlapping grid of all its windows; the t uses per-day sums of w*(x - weighted mean) as cluster deviations, SE = sqrt(G/(G-1)*sum u_d^2)/sum w; held-recovered bars are bars with forecast exactly 0 and a negative post-rebalance allocation; and both stated minimums (30 days, 20 held bars) are treated as minimum counts giving 'not observable' when unmet.
- Size: unusual move +1.13 % (t 2.08, the cases of one day together: 624 days) per case over 7 bars, 0.071 of the coin's usual move (14.34 %); normal drift in its direction -1.13 %, total -0.01 %; 1024 cases
Plan: `steps_cards/03_test_plan/night9_chopmonth_run/plans/067-02.b2.b2.d1_choppy-month-fall-week-hold_1d.md`
Record: `steps_cards/04_backtest/night9_chopmonth_run/backtests/067-02.b2.b2.d1_choppy-month-fall-week-hold_1d`
Measure: `measure.py`
