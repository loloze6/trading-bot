---
plan: 060-01.g1.d2.d1_own-range-close-height-fade_1d
idea: 060-01.g1.d2.d1_own-range-close-height-fade
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day unusual move on short cases (short side, coin drift removed): 0.00903956; t of the mean, cases of one day taken together: 2.23138 (threshold: confirm: mean > 0 with day-clustered t >= 2 and supporting check passed; reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move, upper |forecast| half minus lower half: 0.0045279, passed: True
- Counts: case-days: 236, cases: 378
- Decided by: The mean unusual move is positive with t >= 2 and the upper-minus-lower half difference is above 0.
- Reading: Profile (falling agitated) taken from the recorded regime since its 365-bar/60-bar inputs cannot be rebuilt inside windows, width = high-low range over the mean high-low range of the last 20 bars (today included, regime trusted where fewer than 20 in-window bars), loc > 0.5 from prices; clustered t uses per-day summed deviations with a G/(G-1) correction; upper half is |forecast| above the median, lower half the rest; the plan's 30 case-day minimum gives 'not observable'.
- Size: unusual move +1.19 % (t 3.01, the cases of one day together: 195 days) per case over 1 bars, 0.261 of the coin's usual move (4.73 %); normal drift in its direction -0.13 %, total +1.06 %; 303 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.005429 on the check folds against +0.00904 on every fold
Plan: `steps_cards/03_test_plan/night8_risingagitated_run/plans/060-01.g1.d2.d1_own-range-close-height-fade_1d.md`
Record: `steps_cards/04_backtest/night8_risingagitated_run/backtests/060-01.g1.d2.d1_own-range-close-height-fade_1d`
Measure: `measure.py`
