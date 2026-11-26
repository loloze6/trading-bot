---
plan: 058-02.b1.b1_quiet-volume-fall-keeps-falling_1d
idea: 058-02.b1.b1_quiet-volume-fall-keeps-falling
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of drift-adjusted 5-bar forward return on forecast, fall-regime grid bars: -5.87208e-06; day-clustered OLS slope t: -0.0125038 (threshold: confirm: slope > 0 with day-clustered t >= 2 (and supporting check passes); reject: slope < 0 with t <= -2)
- Supporting check: mean drift-adjusted 5-bar return in the short direction, forecast <= -2: 0.00473676, passed: True
- Counts: grid bars in the fall regime: 3104, grid bars in the fall regime with a forecast of -2 or lower: 1840, distinct days of those bars: 403
- Decided by: The slope's t lies between -2 and 2 (inconclusive rule).
- Reading: The 30-day fall is close[t]/close[t-30]-1 < 0 within the window, using the recorded regime where the window has fewer than 30 prior bars; the regime sample uses the recorded regime 'trending'; the drift is the coin's mean 5-bar return on the non-overlapping grid of all its windows; the slope's t is cluster-robust (CR1) by UTC day; the plan's 'fewer cases' rule is reported as 'not observable' per the workflow.
- Size: unusual move +0.59 % (t 1.61, the cases of one day together: 723 days) per case over 5 bars, 0.047 of the coin's usual move (11.58 %); normal drift in its direction -0.70 %, total -0.12 %; 1228 cases
Plan: `steps_cards/03_test_plan/night8_fallingcalm_run/plans/058-02.b1.b1_quiet-volume-fall-keeps-falling_1d.md`
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/058-02.b1.b1_quiet-volume-fall-keeps-falling_1d`
Measure: `measure.py`
