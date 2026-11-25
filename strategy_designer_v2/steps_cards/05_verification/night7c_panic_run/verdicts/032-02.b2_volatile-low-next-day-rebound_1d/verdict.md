---
plan: 032-02.b2_volatile-low-next-day-rebound_1d
idea: 032-02.b2_volatile-low-next-day-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day excess return of mean_reversion bars with forecast > 0: 0.0236171; day-clustered t of the mean: 2.12997 (threshold: confirm: mean > 0 with t >= 2 and Spearman > 0; reject: mean < 0 with t <= -2; at least 30 distinct case days)
- Supporting check: Spearman(forecast, next-day excess return) > 0: 0.250357, passed: True
- Counts: distinct case days: 93, cases: 143
- Decided by: The mean next-day excess return is positive with t >= 2 and the Spearman correlation is above 0.
- Reading: The 365-to-30 range ratio (and the 30-bar return or prior-low distance where the window lacks the history) cannot be rebuilt inside a window, so the recorded mean_reversion regime stands for those conditions; the t is a day-clustered t (deviations summed per day, D/(D-1) correction); the plan's fewer-than-30-case-days rule is applied as the minimum count, giving 'not observable'.
- Size: unusual move +5.84 % (t 2.65, the cases of one day together: 30 days) per case over 1 bars, 1.230 of the coin's usual move (4.73 %); normal drift in its direction +0.12 %, total +5.96 %; 45 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: too few cases on the check folds (52 cases, 52 days)
Plan: `steps_cards/03_test_plan/night7c_panic_run/plans/032-02.b2_volatile-low-next-day-rebound_1d.md`
Record: `steps_cards/04_backtest/night7c_panic_run/backtests/032-02.b2_volatile-low-next-day-rebound_1d`
Measure: `measure.py`
