---
plan: 059-01_choppy-calm-weekly-rise-continues_1d
idea: 059-01_choppy-calm-weekly-rise-continues
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 7-bar excess return on forecast: 0.00214747; OLS slope t: 1.95477 (threshold: slope t >= 2 confirms (with mean excess > 0); slope t <= -2 rejects)
- Supporting check: mean excess 7-bar return above 0 (day-clustered t, reject if t <= -2): 0.00417588, passed: True
- Counts: cases with forecast > 0 on the grid: 220, days: 127
- Decided by: Inconclusive: at least 40 cases, but neither the confirm nor the reject rule is met.
- Reading: The choppy calm profile is read from the recorded regime ('unknown' = no veto, since the 365-bar volatility percentile cannot be rebuilt from the windows) and the rise from the raw component value (or the 7-bar close return where it is missing); the normal drift is each coin's mean 7-bar return on the non-overlapping grid of all its windows; the slope's t is the ordinary OLS t over all cases pooled; the mean's day-clustered t uses a G/(G-1) correction; fewer than 40 cases is reported as not observable as the workflow requires.
- Size: unusual move -0.36 % (t -0.62, the cases of one day together: 337 days) per case over 7 bars, -0.034 of the coin's usual move (12.44 %); normal drift in its direction +0.96 %, total +0.60 %; 438 cases
Plan: `steps_cards/03_test_plan/night8_choppyagitated_run/plans/059-01_choppy-calm-weekly-rise-continues_1d.md`
Record: `steps_cards/04_backtest/night8_choppyagitated_run/backtests/059-01_choppy-calm-weekly-rise-continues_1d`
Measure: `measure.py`
