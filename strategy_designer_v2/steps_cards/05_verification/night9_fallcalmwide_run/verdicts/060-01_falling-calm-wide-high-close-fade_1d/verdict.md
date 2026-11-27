---
plan: 060-01_falling-calm-wide-high-close-fade_1d
idea: 060-01_falling-calm-wide-high-close-fade
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day unusual move, short direction: 0.00298976; t of the mean, same-day cases summed: 1.00175 (threshold: confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2, or slope t <= -2)
- Supporting check: OLS slope of unusual move on |forecast|: 0.000257668, passed: True
- Counts: cases: 321, distinct days: 186
- Decided by: Neither the confirm rule nor a reject rule is met: inconclusive.
- Reading: Situation taken as raw width >= 2.0 and close location >= 0.75 (recorded raw values, recomputed from prices where missing) with a short forecast; the falling calm profile is added by code and not recomputed (its 365-day lookback exceeds a window); cases are all bars with forecast < 0 and a next bar in the same window; t of the mean uses deviations summed per UTC day; the slope's t is the ordinary least-squares t.
- Size: unusual move +0.29 % (t 0.94, the cases of one day together: 178 days) per case over 1 bars, 0.056 of the coin's usual move (5.33 %); normal drift in its direction -0.13 %, total +0.16 %; 308 cases
Plan: `steps_cards/03_test_plan/night9_fallcalmwide_run/plans/060-01_falling-calm-wide-high-close-fade_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmwide_run/backtests/060-01_falling-calm-wide-high-close-fade_1d`
Measure: `measure.py`
