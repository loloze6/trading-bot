---
plan: 032-01.b1.b1.e2.d2.d1.d1_chop-continuation-exit-on-break_1d
idea: 032-01.b1.b1.e2.d2.d1.d1_chop-continuation-exit-on-break
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the per-day sum of (forecast/10) x (next-day return - coin mean daily return) on chop-regime bars: 0.00516043; t of the mean over days: 1.56568 (threshold: confirm: t >= 2 over >= 100 days with top-minus-bottom third > 0; reject: t <= -2 over >= 100 days)
- Supporting check: top third minus bottom third of |forecast|, mean direction-signed excess next-day return: 0.000592942, passed: True
- Counts: days: 2546, chop-regime cases: 8058
- Decided by: The main t lies between -2 and 2.
- Reading: Situation recomputed from closes inside each window (ER = |close[t]-close[t-30]| / sum of 30 absolute daily changes, 7- and 30-day returns), with active bars whose 30-day lookback lies before the window's first recorded bar left out of the agreement share; chop-regime bars are those whose recorded regime is 'chop' with a next-day close in the same window; terciles of |forecast| are cut by rank (ties in time order) over all chop-regime cases pooled, and a day is the UTC date of the bar's timestamp.
- Size: unusual move +0.14 % (t 1.26, the cases of one day together: 1764 days) per case over 1 bars, 0.030 of the coin's usual move (4.78 %); normal drift in its direction -0.01 %, total +0.14 %; 3640 cases
Plan: `steps_cards/03_test_plan/night7c_chopreversal_run/plans/032-01.b1.b1.e2.d2.d1.d1_chop-continuation-exit-on-break_1d.md`
Record: `steps_cards/04_backtest/night7c_chopreversal_run/backtests/032-01.b1.b1.e2.d2.d1.d1_chop-continuation-exit-on-break_1d`
Measure: `measure.py`
