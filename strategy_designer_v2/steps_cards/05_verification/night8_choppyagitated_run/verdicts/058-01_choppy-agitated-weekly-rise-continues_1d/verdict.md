---
plan: 058-01_choppy-agitated-weekly-rise-continues_1d
idea: 058-01_choppy-agitated-weekly-rise-continues
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 7-bar forward return of grid cases with forecast > 0 (vs coin's mean 7-bar return): -0.00120909; t of the mean, cases of one day taken together: -0.123148 (threshold: confirm: mean > 0 with t >= 2 and Spearman > 0; reject: mean < 0 with t <= -2)
- Supporting check: Spearman correlation between forecast and excess 7-bar return: 0.0333597, passed: True
- Counts: grid cases: 93, distinct days: 64
- Decided by: t is between -2 and 2.
- Reading: grid bars at positions 0,7,14,... of each window with a full 7-bar forward return inside the window; the coin's mean 7-bar return is the mean over that grid of all its windows; the day-clustered t uses per-day sums of deviations with a D/(D-1) correction; minimum counts are reported as 'not observable'.
- Size: unusual move +0.72 % (t 0.84, the cases of one day together: 165 days) per case over 7 bars, 0.051 of the coin's usual move (12.44 %); normal drift in its direction +0.97 %, total +1.69 %; 201 cases
Plan: `steps_cards/03_test_plan/night8_choppyagitated_run/plans/058-01_choppy-agitated-weekly-rise-continues_1d.md`
Record: `steps_cards/04_backtest/night8_choppyagitated_run/backtests/058-01_choppy-agitated-weekly-rise-continues_1d`
Measure: `measure.py`
