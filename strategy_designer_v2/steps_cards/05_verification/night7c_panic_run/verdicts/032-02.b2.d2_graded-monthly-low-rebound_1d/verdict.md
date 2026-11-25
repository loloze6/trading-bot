---
plan: 032-02.b2.d2_graded-monthly-low-rebound_1d
idea: 032-02.b2.d2_graded-monthly-low-rebound
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-1-day return on forecast > 0 bars minus coin mean daily return: 0.00824242; t of the mean, same-day cases pooled: 1.46389 (threshold: confirm: mean > 0 with t >= 2 over >= 30 distinct days; reject: t <= -2 over >= 30 distinct days)
- Supporting check: mean excess return above median forecast minus below median: 0.0129497, passed: True
- Counts: distinct days with cases: 197, cases: 420
- Decided by: t is between -2 and 2 (or not computable), meeting neither the confirm nor the reject rule.
- Reading: The situation is checked on active bars where it can be evaluated (break from the recorded raw depth > 0, or from prices if missing; 30-bar return from closes inside the window), bars without 30 prior bars in their window being left out of the share; the same-day pooled t sums each day's deviations from the mean (clustered standard error with a D/(D-1) correction); cases equal to the median forecast are in neither group.
- Size: unusual move +0.54 % (t 0.84, the cases of one day together: 168 days) per case over 1 bars, 0.125 of the coin's usual move (4.73 %); normal drift in its direction +0.13 %, total +0.67 %; 324 cases
Plan: `steps_cards/03_test_plan/night7c_panic_run/plans/032-02.b2.d2_graded-monthly-low-rebound_1d.md`
Record: `steps_cards/04_backtest/night7c_panic_run/backtests/032-02.b2.d2_graded-monthly-low-rebound_1d`
Measure: `measure.py`
