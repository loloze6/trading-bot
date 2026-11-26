---
plan: 060-02.d1.d1_volume-shrinkage-extends-running-falls_1d
idea: 060-02.d1.d1_volume-shrinkage-extends-running-falls
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: clustered-by-day t of the slope of drift-adjusted next 5-bar return on forecast, trending grid bars: 0.00195196; day-clustered OLS slope t: 2.46139 (threshold: confirm: slope > 0 with t >= 2 and supporting mean > 0; reject: slope < 0 with t <= -2; else inconclusive)
- Supporting check: mean short-side unusual move on grid cases with forecast < 0: 0.00844215, passed: True
- Counts: in-regime grid cases: 906, grid cases with forecast < 0: 520, days: 304
- Decided by: Confirm rule: the slope is positive with t >= 2 and the supporting short-side mean is above 0.
- Reading: Grid = rows 0,5,10,... of each window; normal drift = the coin's mean non-overlapping 5-bar return over all its windows; in-regime = regime 'trending'; slope t uses day-clustered (CR1) standard errors; the situation check takes profile = regime 'trending', 20-day fall from prices (regime where not computable) and shrinkage = raw dryup < 0; fewer than the plan's minimum cases is reported as 'not observable'.
- Size: unusual move +0.93 % (t 1.67, the cases of one day together: 344 days) per case over 5 bars, 0.087 of the coin's usual move (10.60 %); normal drift in its direction -0.59 %, total +0.34 %; 454 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0006133 on the check folds against +0.001952 on every fold
Plan: `steps_cards/03_test_plan/night8_fallingcalm_run/plans/060-02.d1.d1_volume-shrinkage-extends-running-falls_1d.md`
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/060-02.d1.d1_volume-shrinkage-extends-running-falls_1d`
Measure: `measure.py`
