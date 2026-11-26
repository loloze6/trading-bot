---
plan: 060-02_falling-agitated-rally-fades-next-day_1d
idea: 060-02_falling-agitated-rally-fades-next-day
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of signal-direction next-day excess return on |forecast|: 0.000134197; slope t, clustered by day: 0.399705 (threshold: confirm: slope t >= 2 (with mean excess > 0, t >= 2); reject: slope t <= -2 or mean t <= -2)
- Supporting check: mean signal-direction next-day excess return (t clustered by day = 2.349): 0.00517908, passed: True
- Counts: cases: 2538, distinct days: 758
- Decided by: Neither rule met: the slope's t and the mean's t lie between the confirm and reject thresholds (or the slope passes without the mean).
- Reading: Profile bars are those with regime 'unknown' (not vetoed to chop), the situation is a positive raw scaled return (price return when unrecorded); next-day return is close[t+1]/close[t]-1 inside the window on every case bar, the coin's mean is over all its 1-day returns in all windows, t's use CR1 cluster-robust errors by UTC day, and the plan's 'fewer than 100 cases or 50 days' is reported as 'not observable'.
- Size: unusual move +0.56 % (t 2.09, the cases of one day together: 565 days) per case over 1 bars, 0.113 of the coin's usual move (5.33 %); normal drift in its direction -0.14 %, total +0.42 %; 1669 cases
Plan: `steps_cards/03_test_plan/night8_choppyagitated_run/plans/060-02_falling-agitated-rally-fades-next-day_1d.md`
Record: `steps_cards/04_backtest/night8_choppyagitated_run/backtests/060-02_falling-agitated-rally-fades-next-day_1d`
Measure: `measure.py`
