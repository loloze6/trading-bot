---
plan: 069-02.d2_agitated-below-high-up-day-fade_1d
idea: 069-02.d2_agitated-below-high-up-day-fade
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of next-day excess return on abs(forecast), cases forecast < 0: -0.000409069; day-clustered OLS slope t: -1.69869 (threshold: confirm: slope < 0 with t <= -2 and supporting check passes; reject: slope > 0 with t >= +2; otherwise inconclusive; at least 100 distinct case days)
- Supporting check: mean next-day excess return in short direction > 0: 0.00278813, passed: True
- Counts: distinct case days: 1517, cases: 3951
- Decided by: The slope's t lies between -2 and +2.
- Reading: Profile and the up-day rule on a window's first bar are taken from the recorded regime (the detector's components are not recorded), the up day elsewhere from the 1-bar close return, the depth from the raw component being below 0; the slope t uses a day-clustered (by UTC date) OLS standard error with the usual small-sample correction, the coin's mean is over all 1-bar returns of all its windows, and the 100-case-day minimum is treated as a minimum count (not observable when missed).
- Size: unusual move +0.55 % (t 2.93, the cases of one day together: 979 days) per case over 1 bars, 0.119 of the coin's usual move (4.73 %); normal drift in its direction -0.13 %, total +0.42 %; 2099 cases
Plan: `steps_cards/03_test_plan/night8_risingagitated_run/plans/069-02.d2_agitated-below-high-up-day-fade_1d.md`
Record: `steps_cards/04_backtest/night8_risingagitated_run/backtests/069-02.d2_agitated-below-high-up-day-fade_1d`
Measure: `measure.py`
