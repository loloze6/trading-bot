---
plan: 058-02.g1_choppy-agitated-deep-fall-continues_1d
idea: 058-02.g1_choppy-agitated-deep-fall-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of 5-day excess return on forecast (grid bars, forecast < 0): 0.00110511; OLS slope t: 0.767565 (threshold: confirm: slope > 0 with t >= 2 and mean excess < 0; reject: slope < 0 with t <= -2)
- Supporting check: mean 5-day excess return on the same bars below 0: -0.0198209, passed: True
- Counts: grid bars with forecast < 0: 160
- Decided by: The slope's t lies between -2 and 2 (inconclusive rule).
- Reading: The profile is read from the regime column (regime 'unknown', no veto fired) and the fall from the sign of the raw scaled 30-day return; holding is the coin's mean 5-day return over its non-overlapping grid of all windows, and the plan's minimum of 30 grid bars is applied as 'not observable'.
- Size: unusual move +0.62 % (t 0.98, the cases of one day together: 191 days) per case over 5 bars, 0.058 of the coin's usual move (10.60 %); normal drift in its direction -0.66 %, total -0.03 %; 230 cases
Plan: `steps_cards/03_test_plan/night8_fallingcalm_run/plans/058-02.g1_choppy-agitated-deep-fall-continues_1d.md`
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/058-02.g1_choppy-agitated-deep-fall-continues_1d`
Measure: `measure.py`
