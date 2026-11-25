---
plan: 032-02.b1.b1_choppy-downside-break-rebound_1d
idea: 032-02.b1.b1_choppy-downside-break-rebound
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day excess return over the coin's mean, cases summed per day: 0.0175166; t of the mean: 1.89775 (threshold: confirm: mean > 0 with t >= 2 on >= 30 days; reject: mean < 0 with t <= -2 on >= 30 days)
- Supporting check: slope of next-day excess return on depth below the prior 20-day low: 0.00469206, passed: True
- Counts: days with a case: 150, cases (coin-bars): 285, cases with depth: 285
- Decided by: The t of the mean excess next-day return lies between -2 and 2.
- Reading: The situation check uses the recorded depth (else the close against the prior 20 bars' lowest low) and the 60-bar close return in percent, inclusive of -10 and +10, and leaves out of its share the active bars whose 60-bar return or 20-bar low cannot be computed inside the window; the depth slope is the least-squares slope of each coin-bar's next-day excess return on its depth below the low (minus last_history_value), fitted over the coin-bar observations of the cases.
- Size: unusual move +1.34 % (t 1.79, the cases of one day together: 57 days) per case over 1 bars, 0.231 of the coin's usual move (5.31 %); normal drift in its direction +0.13 %, total +1.47 %; 94 cases
Plan: `steps_cards/03_test_plan/night7_rangefail_run/plans/032-02.b1.b1_choppy-downside-break-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_rangefail_run/backtests/032-02.b1.b1_choppy-downside-break-rebound_1d`
Measure: `measure.py`
