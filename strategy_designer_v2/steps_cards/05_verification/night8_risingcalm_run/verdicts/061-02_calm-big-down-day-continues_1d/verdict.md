---
plan: 061-02_calm-big-down-day-continues_1d
idea: 061-02_calm-big-down-day-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess gain of (forecast/10) x 5-bar excess return on grid cases: 0.00804412; t of the mean, same-day cases summed: 1.58673 (threshold: confirm: mean > 0 with t >= 2 and supporting check passed; reject: mean < 0 with t <= -2)
- Supporting check: upper minus lower |forecast| half, mean short-direction 5-bar excess return (Welch t >= 1): -0.246764, passed: False
- Counts: cases: 930, cases on distinct days: 340
- Decided by: The t of the mean excess gain lies between -2 and 2, which the plan calls inconclusive.
- Reading: The upper half is |forecast| strictly above the median and the lower half at or below it, the coin's mean 5-bar return is taken on the same non-overlapping grid of all its windows, the day-clustered t uses a G/(G-1) correction, and the supporting check's value is its Welch t (upper minus lower).
- Size: unusual move +0.33 % (t 0.90, the cases of one day together: 836 days) per case over 5 bars, 0.035 of the coin's usual move (10.60 %); normal drift in its direction -0.64 %, total -0.31 %; 1769 cases
Plan: `steps_cards/03_test_plan/night8_risingcalm_run/plans/061-02_calm-big-down-day-continues_1d.md`
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/061-02_calm-big-down-day-continues_1d`
Measure: `measure.py`
