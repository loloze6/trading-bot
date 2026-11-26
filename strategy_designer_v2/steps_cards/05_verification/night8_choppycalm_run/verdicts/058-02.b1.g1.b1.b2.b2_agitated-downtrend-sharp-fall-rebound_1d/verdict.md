---
plan: 058-02.b1.g1.b1.b2.b2_agitated-downtrend-sharp-fall-rebound_1d
idea: 058-02.b1.g1.b1.b2.b2_agitated-downtrend-sharp-fall-rebound
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of next-day excess return on forecast, positive-forecast bars: 0.000643518; t of the slope, day-clustered: 1.78075 (threshold: confirm if slope t >= 2 (with supporting check), reject if slope t <= -2)
- Supporting check: forecast-weighted mean next-day excess return > 0: 0.007653, passed: True
- Counts: bars with a positive forecast: 2872, distinct days: 832
- Decided by: The slope's t is strictly between -2 and 2.
- Reading: The falling agitated profile is read from the recorded regime ('unknown' = both chop vetoes passed, since the detector's components are not recorded) and the fall from the raw scaled return being negative (recomputed from closes where missing); the slope is an OLS of excess next-day return on the forecast with a day-clustered standard error; the plan's minimum counts are applied as 'not observable'.
- Size: unusual move +0.60 % (t 2.15, the cases of one day together: 610 days) per case over 1 bars, 0.129 of the coin's usual move (5.33 %); normal drift in its direction +0.14 %, total +0.74 %; 1893 cases
Plan: `steps_cards/03_test_plan/night8_choppycalm_run/plans/058-02.b1.g1.b1.b2.b2_agitated-downtrend-sharp-fall-rebound_1d.md`
Record: `steps_cards/04_backtest/night8_choppycalm_run/backtests/058-02.b1.g1.b1.b2.b2_agitated-downtrend-sharp-fall-rebound_1d`
Measure: `measure.py`
