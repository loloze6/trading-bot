---
plan: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days_1d
idea: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the mean of forecast/10 x excess 10-bar return (net of the coin's mean 10-bar return): 0.0103519; t of the mean: 2.24138 (threshold: confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2; at least 300 non-overlapping cases)
- Supporting check: none
- Counts: non-overlapping cases: 1691
- Decided by: The mean forecast-weighted excess 10-bar return is positive with t >= 2 over at least 300 non-overlapping cases.
- Reading: Every grid bar (positions 0, 10, 20, ... of each window with close[t+10] inside the window and a forecast recorded) is a case, including those with forecast 0, and the coin's mean 10-bar return is the mean over the same non-overlapping grid returns of all its windows; the situation's side is the sign of the recorded raw 28-day return (recomputed from closes where missing).
- Size: unusual move +0.59 % per case over 10 bars, 0.037 of the coin's usual move (14.49 %); normal drift in its direction -0.02 %, total +0.57 %; 1448 cases
Plan: `steps_cards/03_test_plan/night3_learned_run/plans/022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days_1d.md`
Record: `steps_cards/04_backtest/night3_learned_run/backtests/022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days_1d`
Measure: `measure.py`
