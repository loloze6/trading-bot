---
plan: 060-01.b1.d1.b1_fresh-slide-bounce-fades-overnight_1d
idea: 060-01.b1.d1.b1_fresh-slide-bounce-fades-overnight
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of next-day excess return on -forecast (short bars): -0.000362952; OLS slope t, day-clustered: -0.648601 (threshold: confirm: slope < 0 with day-clustered t <= -2 and check passes; reject: slope > 0 with t >= 2)
- Supporting check: mean next-day excess return, short-signed, > 0: 0.00522089, passed: True
- Counts: active bars: 1598, distinct days: 535
- Decided by: Inconclusive: the slope's t lies between -2 and 2.
- Reading: Situation taken as the raw 5-day lag-1 scaled return < 0 and today's raw 1-day scaled return > 0 (recomputed from prices if not recorded) with a negative forecast, the profile not rechecked since its components are not recorded and need more history than a window; the excess return removes the coin's mean 1-bar return over all its windows; t is an OLS slope t with standard errors clustered by UTC day; active bars are bars with forecast < 0 and a next-day return in the same window; the plan's minimum counts, when not reached, give 'not observable'.
- Size: unusual move +0.65 % (t 2.04, the cases of one day together: 421 days) per case over 1 bars, 0.134 of the coin's usual move (5.33 %); normal drift in its direction -0.13 %, total +0.52 %; 1203 cases
Plan: `steps_cards/03_test_plan/night8_choppyagitated_run/plans/060-01.b1.d1.b1_fresh-slide-bounce-fades-overnight_1d.md`
Record: `steps_cards/04_backtest/night8_choppyagitated_run/backtests/060-01.b1.d1.b1_fresh-slide-bounce-fades-overnight_1d`
Measure: `measure.py`
