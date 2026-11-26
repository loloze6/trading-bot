---
plan: 058-01.b2.b1_quiet-calm-fall-more-coins_1d
idea: 058-01.b2.b1_quiet-calm-fall-more-coins
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of drift-adjusted 5-day return on forecast, in-regime grid bars: 0.000210801; slope t, day-clustered: 0.458499 (threshold: confirm: slope > 0 with t >= 2 and check passes; reject: slope < 0 with t <= -2; else inconclusive)
- Supporting check: mean drift-adjusted 5-day return on grid bars with forecast < 0: -0.000374385, passed: True
- Counts: in-regime grid bars: 931, bars with forecast below 0: 822, bars with forecast 0: 109, distinct days: 271
- Decided by: The slope's |t| is below 2.
- Reading: The situation is the 30-day close-to-close return below 0 (from prices, or the recorded 'trending' regime on a window's first 30 bars) with the bar's regime 'trending' standing for the falling-calm profile, side short; in-regime means regime == 'trending'; the coin's mean 5-day return is taken on the 5-bar grid of all its windows; the slope's t pools same-day cases as day-clustered standard errors; the supporting check is the sign of the mean; distinct days are the days of the in-regime grid bars.
- Size: unusual move +0.32 % (t 0.63, the cases of one day together: 434 days) per case over 5 bars, 0.031 of the coin's usual move (11.58 %); normal drift in its direction -0.69 %, total -0.37 %; 687 cases
Plan: `steps_cards/03_test_plan/night8_fallingcalm_run/plans/058-01.b2.b1_quiet-calm-fall-more-coins_1d.md`
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/058-01.b2.b1_quiet-calm-fall-more-coins_1d`
Measure: `measure.py`
