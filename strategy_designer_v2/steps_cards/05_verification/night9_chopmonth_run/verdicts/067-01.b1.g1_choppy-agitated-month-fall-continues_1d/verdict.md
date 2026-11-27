---
plan: 067-01.b1.g1_choppy-agitated-month-fall-continues_1d
idea: 067-01.b1.g1_choppy-agitated-month-fall-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 7-bar forward return minus coin drift on fall30 post_pipeline_value: 0.00165791; ordinary OLS slope t: 1.09368 (threshold: confirm: slope > 0 with t >= 2 and mean short unusual move > 0; reject: slope < 0 with t <= -2)
- Supporting check: mean short unusual move (minus excess return): 0.0053883, passed: True
- Counts: independent grid cases with a forecast below 0: 215
- Decided by: The slope's t lies between -2 and 2 (inconclusive rule).
- Reading: The choppy agitated profile is read from the recorded regime ('unknown', the only regime the detector does not veto to chop) and the fall from the raw 30-bar return (recomputed from closes where missing); cases are grid bars (positions 0,7,14,... of each window, forward return inside the window) with forecast < 0, regressed on fall30's post_pipeline_value, with each coin's drift as the mean 7-bar return on the same grid over all its windows; the plan's 30-case minimum gives 'not observable' when unmet.
- Size: unusual move +1.22 % (t 1.66, the cases of one day together: 265 days) per case over 7 bars, 0.076 of the coin's usual move (12.84 %); normal drift in its direction -0.94 %, total +0.28 %; 359 cases
Plan: `steps_cards/03_test_plan/night9_chopmonth_run/plans/067-01.b1.g1_choppy-agitated-month-fall-continues_1d.md`
Record: `steps_cards/04_backtest/night9_chopmonth_run/backtests/067-01.b1.g1_choppy-agitated-month-fall-continues_1d`
Measure: `measure.py`
