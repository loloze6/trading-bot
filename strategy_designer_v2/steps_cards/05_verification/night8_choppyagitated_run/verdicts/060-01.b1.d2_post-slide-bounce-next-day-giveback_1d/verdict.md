---
plan: 060-01.b1.d2_post-slide-bounce-next-day-giveback_1d
idea: 060-01.b1.d2_post-slide-bounce-next-day-giveback
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of drift-adjusted next 1-day return on short size (-forecast), active bars: -0.00027706; slope t, day-clustered SE: -0.594882 (threshold: confirm: slope < 0 with t <= -2 and mean drift-adjusted return < 0; reject: slope > 0 with t >= +2)
- Supporting check: mean drift-adjusted next-day return on active bars < 0: -0.00517908, passed: True
- Counts: active bars: 2538, distinct days: 758
- Decided by: The slope t lies between -2 and +2.
- Reading: Situation checked as rise bar (prior close-to-close return > 0, raw scaled_rise sign on a window's first bar) with regime 'trending' as the profile (detector components not recorded, its vetoes encode falling/agitated) and short side; slope by OLS with intercept, t from day-clustered (CR1) standard errors, drift is each coin's mean daily return over all its windows, and the plan's minimum counts unmet give 'not observable'.
- Size: unusual move +0.62 % (t 2.27, the cases of one day together: 537 days) per case over 1 bars, 0.126 of the coin's usual move (5.33 %); normal drift in its direction -0.13 %, total +0.48 %; 1583 cases
Plan: `steps_cards/03_test_plan/night8_choppyagitated_run/plans/060-01.b1.d2_post-slide-bounce-next-day-giveback_1d.md`
Record: `steps_cards/04_backtest/night8_choppyagitated_run/backtests/060-01.b1.d2_post-slide-bounce-next-day-giveback_1d`
Measure: `measure.py`
