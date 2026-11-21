---
plan: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling_1d
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of mean (forecast/10) x (3-bar return minus coin mean 3-bar return), forecast < 0 cases, pooled over coins: 0.00193593; t of the mean: 1.29042 (threshold: confirm if t >= 2 and the supporting check is negative; reject if t <= -2; minimum 100 independent forecast < 0 cases)
- Supporting check: mean excess 3-bar return of deeper half (forecast below median) minus shallower half: 0.00163658, passed: False
- Counts: independent forecast < 0 cases: 2881
- Decided by: t = 1.29 lies between -2 and 2.
- Reading: The coin's mean 3-bar return is taken over all grid cases of all its windows; the median split is pooled over coins, with cases at the median in the shallower half.
- Size: unusual move -0.16 % per case over 3 bars, -0.025 of the coin's usual move (7.96 %); normal drift in its direction -0.35 %, total -0.52 %; 1677 cases
Plan: `steps_cards/03_test_plan/night_013_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling_1d.md`
Record: `steps_cards/04_backtest/night_013_run/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling_1d`
Measure: `measure.py`
