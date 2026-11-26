---
plan: 069-02.d1.d1_agitated-fall-up-day-fade_1d
idea: 069-02.d1.d1_agitated-fall-up-day-fade
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: least-squares slope of next-day excess return e on depth d = -forecast: -0.000204858; t of the slope, cases clustered by day: -0.409074 (threshold: t <= -2 confirms (with mean of -e > 0); t >= +2 rejects; otherwise inconclusive; at least 100 cases on at least 60 distinct days)
- Supporting check: mean of -e over the cases above 0: 0.00555294, passed: True
- Counts: cases: 1325, distinct days: 633
- Decided by: The slope's t lies between -2 and +2 (inconclusive rule).
- Reading: Cases are all bars with forecast < 0 that have a next bar in the same window; the coin's mean daily return is the mean of all its one-bar returns inside windows over all windows; the slope's t is OLS with standard errors clustered by UTC day (cases of one day taken together, with the usual G/(G-1)*(N-1)/(N-K) correction); the profile in the situation check is read from the recorded regime (mean_reversion), since the detector's components are not recorded and the 365-bar percentile cannot be rebuilt inside windows; the plan's minimum counts, when not reached, give 'not observable'.
- Size: unusual move +0.95 % (t 3.27, the cases of one day together: 394 days) per case over 1 bars, 0.204 of the coin's usual move (4.73 %); normal drift in its direction -0.13 %, total +0.82 %; 752 cases
Plan: `steps_cards/03_test_plan/night8_risingagitated_run/plans/069-02.d1.d1_agitated-fall-up-day-fade_1d.md`
Record: `steps_cards/04_backtest/night8_risingagitated_run/backtests/069-02.d1.d1_agitated-fall-up-day-fade_1d`
Measure: `measure.py`
