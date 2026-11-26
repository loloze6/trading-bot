---
plan: 060-01.g1.d2.d1_own-range-close-height-fade_1d
idea: 060-01.g1.d2.d1_own-range-close-height-fade
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day unusual move on short cases (short side, coin drift removed): 0.00739858; t of the mean, cases of one day taken together: 1.88903 (threshold: confirm: mean > 0 with day-clustered t >= 2 and supporting check passed; reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move, upper |forecast| half minus lower half: 0.0104005, passed: True
- Counts: case-days: 404, cases: 1099
- Decided by: The t lies between -2 and 2, which the plan calls inconclusive.
- Reading: Profile (falling agitated) taken from the recorded regime since its 365-bar/60-bar inputs cannot be rebuilt inside windows, width = high-low range over the mean high-low range of the last 20 bars (today included, regime trusted where fewer than 20 in-window bars), loc > 0.5 from prices; clustered t uses per-day summed deviations with a G/(G-1) correction; upper half is |forecast| above the median, lower half the rest; the plan's 30 case-day minimum gives 'not observable'.
- Size: unusual move +0.88 % (t 2.10, the cases of one day together: 329 days) per case over 1 bars, 0.181 of the coin's usual move (5.12 %); normal drift in its direction -0.11 %, total +0.77 %; 875 cases
Plan: `steps_cards/03_test_plan/night8_risingagitated_run/plans/060-01.g1.d2.d1_own-range-close-height-fade_1d.md`
Record: `steps_cards/04_backtest/night8_risingagitated_run/common/backtests/060-01.g1.d2.d1_own-range-close-height-fade_1d`
Measure: `measure.py`
