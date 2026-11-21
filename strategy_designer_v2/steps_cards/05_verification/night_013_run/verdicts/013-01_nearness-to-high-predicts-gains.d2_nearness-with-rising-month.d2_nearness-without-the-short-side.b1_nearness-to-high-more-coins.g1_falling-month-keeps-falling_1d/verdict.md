---
plan: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins.g1_falling-month-keeps-falling_1d
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins.g1_falling-month-keeps-falling
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of excess 7-bar return on forecast, falling-month regime grid bars: 0.000453557; OLS t of slope: 0.860507 (threshold: confirm: slope > 0 with t >= 2 (and timing gain > 0); reject: slope < 0 with t <= -2; at least 100 grid cases)
- Supporting check: mean of (forecast/10) x excess 7-bar return: 0.0149663, passed: True
- Counts: grid cases in the regime: 2655
- Decided by: The slope's t lies between -2 and 2 (inconclusive rule).
- Reading: The falling month is the 30-day close-to-close return recomputed inside each window (the recorded regime is used on the first 30 rows where it cannot be recomputed), the depth below the high is the recorded depth raw value (< 0), the expected side is short, the coin's mean 7-bar return is taken over all its grid bars in all windows, and the minimum of 100 grid cases is applied as 'not observable'.
- Size: unusual move +1.25 % per case over 7 bars, 0.084 of the coin's usual move (13.79 %); normal drift in its direction -1.12 %, total +0.13 %; 1950 cases
Plan: `steps_cards/03_test_plan/night_013_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins.g1_falling-month-keeps-falling_1d.md`
Record: `steps_cards/04_backtest/night_013_run/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins.g1_falling-month-keeps-falling_1d`
Measure: `measure.py`
