---
plan: 074-01.b1.b1.b1.b1_falling-wide-high-close-fade_1d
idea: 074-01.b1.b1.b1.b1_falling-wide-high-close-fade
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day short-direction return beyond drift on case bars: 0.00697724; t of the mean, cases grouped by day: 2.19778 (threshold: confirm: mean > 0 with t >= 2 and positive slope; reject: mean < 0 with t <= -2)
- Supporting check: slope of next-day excess return on forecast: 0.000991073, passed: True
- Counts: case days: 471, cases: 1143
- Decided by: The mean short-direction excess return is above 0 with t >= 2 and the supporting slope is positive.
- Reading: Situation computed per window from prices and the recorded raw width/loc values: up = close above prior close, width > 1, close location >= 0.75, falling = 60-bar price change below -10 % (the veto's threshold read in percent), active bars whose conditions cannot be computed inside the window (first bar, first 60 bars) are left out of the share; the horizon grid is every bar (h = 1), drift is the coin's mean 1-bar return over all its windows, t clusters cases by UTC day (deviations summed per day, D/(D-1) correction), the slope is OLS of next-day excess return on forecast, and the plan's 'fewer than 30 case days' is treated as the minimum count (not observable).
- Size: unusual move +0.72 % (t 2.19, the cases of one day together: 437 days) per case over 1 bars, 0.139 of the coin's usual move (5.31 %); normal drift in its direction -0.15 %, total +0.57 %; 1063 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.005343 on the check folds against +0.006977 on every fold
Plan: `steps_cards/03_test_plan/night9_chopdeep_run/plans/074-01.b1.b1.b1.b1_falling-wide-high-close-fade_1d.md`
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/074-01.b1.b1.b1.b1_falling-wide-high-close-fade_1d`
Measure: `measure.py`
