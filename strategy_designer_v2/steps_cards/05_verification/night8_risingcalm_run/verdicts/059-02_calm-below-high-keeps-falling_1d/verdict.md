---
plan: 059-02_calm-below-high-keeps-falling_1d
idea: 059-02_calm-below-high-keeps-falling
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 5-bar excess return on forecast, in-profile grid bars: 0.000937956; OLS slope t: 2.85561 (threshold: confirm: slope > 0 with t >= 2 (and supporting check positive); reject: slope < 0 with t <= -2)
- Supporting check: mean unusual 5-bar move of short-side cases, short direction: 0.000405641, passed: True
- Counts: grid cases in profile with a non-zero forecast: 1550, grid cases in profile: 1829, supporting cases (short-side forecast rises of at least 2 points): 1530
- Decided by: Confirmed on every fold, but the main measure points the other way on the check folds (A, D), the years step 7 does not explore: main measure -0.0003639 on the check folds against +0.000938 on every fold.
- Reading: In-profile means regime 'unknown' (the calm regime with the strategy), the regression uses all in-profile grid bars including forecast 0, the coin's drift is its mean non-overlapping 5-bar grid return over all windows, and supporting cases are short-side bets (forecast.md 7) taken once per grid cell at their first bar; a short count below the minimum is reported as not observable per the workflow.
- Size: unusual move +0.04 % (t 0.12, the cases of one day together: 813 days) per case over 5 bars, 0.004 of the coin's usual move (10.60 %); normal drift in its direction -0.64 %, total -0.60 %; 1530 cases
- Direction check on folds A, D (the years step 7 does not explore): disagrees: main measure -0.0003639 on the check folds against +0.000938 on every fold
Plan: `steps_cards/03_test_plan/night8_risingcalm_run/plans/059-02_calm-below-high-keeps-falling_1d.md`
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/059-02_calm-below-high-keeps-falling_1d`
Measure: `measure.py`
