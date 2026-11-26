---
plan: 069-02_below-high-up-day-fade_1d
idea: 069-02_below-high-up-day-fade
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of (forecast/10) x next-day excess return on up days: 0.00276565; t of the mean, cases of one day taken together: 2.72784 (threshold: confirm: mean > 0 with t >= 2 and check passes; reject: mean < 0 with t <= -2)
- Supporting check: deepest third minus shallowest third mean excess next-day return < 0: -0.00615436, passed: True
- Counts: up-day cases: 8849, distinct days: 2274
- Decided by: The mean gain is positive with t >= 2 and the deepest third's mean excess next-day return minus the shallowest third's is below 0.
- Reading: Up-day cases are the bars whose regime is mean_reversion with a next-day close in the same window, the coin's mean daily return is over all its windows' next-day returns, the t clusters cases by UTC day (deviations summed per day, with a D/(D-1) correction), the thirds are n//3 cases each from sorting the forecast (lowest = deepest), the situation check leaves out each window's first bar, and the plan's 'too few cases' rule is reported as not observable as the workflow requires.
- Size: unusual move +0.33 % (t 2.80, the cases of one day together: 1618 days) per case over 1 bars, 0.072 of the coin's usual move (4.78 %); normal drift in its direction -0.12 %, total +0.21 %; 4585 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0008131 on the check folds against +0.002766 on every fold
Plan: `steps_cards/03_test_plan/night8_risingagitated_run/plans/069-02_below-high-up-day-fade_1d.md`
Record: `steps_cards/04_backtest/night8_risingagitated_run/backtests/069-02_below-high-up-day-fade_1d`
Measure: `measure.py`
