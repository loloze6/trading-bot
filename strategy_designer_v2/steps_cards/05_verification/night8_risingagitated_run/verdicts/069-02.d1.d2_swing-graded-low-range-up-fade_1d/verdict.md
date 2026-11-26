---
plan: 069-02.d1.d2_swing-graded-low-range-up-fade_1d
idea: 069-02.d1.d2_swing-graded-low-range-up-fade
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of next-day short-direction excess return on abs(forecast): -0.000324165; OLS slope t: -0.606406 (threshold: confirm: slope > 0 with t >= 2 and mean excess > 0; reject: slope < 0 with t <= -2)
- Supporting check: mean short-direction next-day excess return > 0: 0.0071623, passed: True
- Counts: cases: 378
- Decided by: The slope's t lies between -2 and 2.
- Reading: Bars whose 60-day, 20-day or 1-day evolution cannot be recomputed inside their window (no warm-up recorded) are left out of the situation check, the falling profile is read as a 60-bar price evolution in percent below -10 (the config veto), and every bar is a case grid cell since the horizon is 1 bar; the plan's 'fewer than 100 cases' is applied as a minimum count.
- Size: unusual move +0.99 % (t 2.08, the cases of one day together: 198 days) per case over 1 bars, 0.206 of the coin's usual move (4.73 %); normal drift in its direction -0.13 %, total +0.86 %; 306 cases
Plan: `steps_cards/03_test_plan/night8_risingagitated_run/plans/069-02.d1.d2_swing-graded-low-range-up-fade_1d.md`
Record: `steps_cards/04_backtest/night8_risingagitated_run/backtests/069-02.d1.d2_swing-graded-low-range-up-fade_1d`
Measure: `measure.py`
