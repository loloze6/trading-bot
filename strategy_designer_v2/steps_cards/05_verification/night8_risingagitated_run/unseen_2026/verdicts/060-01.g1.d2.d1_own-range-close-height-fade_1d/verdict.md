---
plan: 060-01.g1.d2.d1_own-range-close-height-fade_1d
idea: 060-01.g1.d2.d1_own-range-close-height-fade
fit: adapted
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day unusual move on short cases (short side, coin drift removed): 0.000926074; t of the mean, cases of one day taken together: 0.114254 (threshold: confirm: mean > 0 with day-clustered t >= 2 and supporting check passed; reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move, upper |forecast| half minus lower half: 0.0283494, passed: True
- Counts: case-days: 25, cases: 52
- Decided by: Only 25 case-days, below the plan's minimum of 30 case-days.
- Reading: Profile (falling agitated) taken from the recorded regime since its 365-bar/60-bar inputs cannot be rebuilt inside windows, width = high-low range over the mean high-low range of the last 20 bars (today included, regime trusted where fewer than 20 in-window bars), loc > 0.5 from prices; clustered t uses per-day summed deviations with a G/(G-1) correction; upper half is |forecast| above the median, lower half the rest; the plan's 30 case-day minimum gives 'not observable'.
- Size: unusual move +0.07 % (t 0.09, the cases of one day together: 23 days) per case over 1 bars, 0.113 of the coin's usual move (3.33 %); normal drift in its direction -0.02 %, total +0.05 %; 50 cases
Plan: `steps_cards/03_test_plan/night8_risingagitated_run/plans/060-01.g1.d2.d1_own-range-close-height-fade_1d.md`
Record: `steps_cards/04_backtest/night8_risingagitated_run/unseen_2026/backtests/060-01.g1.d2.d1_own-range-close-height-fade_1d`
Measure: `measure.py`
