---
plan: 058-02.b2_calm-range-position-continues_1d
idea: 058-02.b2_calm-range-position-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of the 5-bar excess return on the forecast: 0.000288097; t of slope, cases clustered by day: 0.726371 (threshold: slope > 0 with t >= 2 confirms; slope < 0 with t <= -2 rejects; otherwise inconclusive)
- Supporting check: none
- Counts: grid cases inside the profile: 567, distinct days: 282
- Decided by: The t of the slope lies between -2 and +2.
- Reading: Profile bars are those with regime 'unknown'; the drift is the coin's mean 5-bar return over all grid cells of all its windows; 'taken together by day' is a day-clustered (CR1) standard error of the OLS slope; the plan's minimum counts, when not reached, give 'not observable'.
- Size: unusual move +0.42 % (t 1.25, the cases of one day together: 588 days) per case over 5 bars, 0.044 of the coin's usual move (10.60 %); normal drift in its direction +0.03 %, total +0.45 %; 800 cases
Plan: `steps_cards/03_test_plan/night8_choppycalm_run/plans/058-02.b2_calm-range-position-continues_1d.md`
Record: `steps_cards/04_backtest/night8_choppycalm_run/backtests/058-02.b2_calm-range-position-continues_1d`
Measure: `measure.py`
