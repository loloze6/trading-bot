---
plan: 031-02.b1.b1.b1.d1_small-body-wide-uprun-day_1d
idea: 031-02.b1.b1.b1.d1_small-body-wide-uprun-day
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 3-bar unusual move of long bets (return minus coin's normal 3-bar drift), before costs: 0.0222924; t of the mean, cases of one day taken together: 1.53033 (threshold: confirm: mean > 0 with t >= 2 over at least 30 cases and supporting check passes; reject: mean < 0 with t <= -2 over at least 30 cases)
- Supporting check: mean unusual move above minus below the median case forecast > 0: 0.0327391, passed: True
- Counts: cases: 151, distinct days: 111
- Decided by: The t of the mean unusual move is between -2 and 2.
- Reading: The situation is rebuilt per window from the recorded raw flatness and run_up where present and otherwise from prices, with 'wide' as the day's range over the mean range of the last 20 bars including it, active bars whose 20-bar range history is incomplete being left out of the agreement; a case is the first bet (forecast rise of >= 2 points from its lowest level on its side since the last bet) in each cell of the per-window 3-bar grid, its unusual move is its 3-bar return minus the coin's mean 3-bar return on the pooled grid of all its windows, the t is clustered by UTC day, the median split drops cases equal to the median, and the minimum is 30 cases.
- Size: unusual move +2.23 % (t 1.54, the cases of one day together: 111 days) per case over 3 bars, 0.192 of the coin's usual move (13.83 %); normal drift in its direction +2.82 %, total +5.05 %; 151 cases
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-02.b1.b1.b1.d1_small-body-wide-uprun-day_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/unseen_2016_2017/backtests/031-02.b1.b1.b1.d1_small-body-wide-uprun-day_1d`
Measure: `measure.py`
