---
plan: 074-01.b1.d1_run-break-fade-widening-swing_1d
idea: 074-01.b1.d1_run-break-fade-widening-swing
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-signed next-day return minus coin mean daily return, over forecast<0 bars: 0.00551527; t of the mean, cases grouped by day: 2.88363 (threshold: confirm: mean > 0 with t >= 2 (day-clustered) and check > 0; reject: mean < 0 with t <= -2)
- Supporting check: top-half minus bottom-half |forecast| mean short-signed unusual move: 0.00791215, passed: True
- Counts: cases across the coins: 1692, days with cases: 739
- Decided by: Mean above 0 with t >= 2 and top-minus-bottom |forecast| half difference above 0.
- Reading: Situation from run_depth raw value > 0 (prices where unrecorded) and 60-bar in-window price return < -10 % (detector's regime where 60 bars are not available); cases with no next bar in the window are left out; top half = the n//2 cases with largest |forecast| (stable sort), bottom half = the rest; the 100-case minimum is applied as 'not observable'.
- Size: unusual move +0.55 % (t 2.87, the cases of one day together: 738 days) per case over 1 bars, 0.118 of the coin's usual move (4.78 %); normal drift in its direction -0.12 %, total +0.43 %; 1685 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.001024 on the check folds against +0.005515 on every fold
Plan: `steps_cards/03_test_plan/night9_fallcalmfade_run/plans/074-01.b1.d1_run-break-fade-widening-swing_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/backtests/074-01.b1.d1_run-break-fade-widening-swing_1d`
Measure: `measure.py`
