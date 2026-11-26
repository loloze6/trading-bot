---
plan: 058-01.g2.b1.d2.b1.d2.d2_modest-bounce-in-slide-fades_1d
idea: 058-01.g2.b1.d2.b1.d2.d2_modest-bounce-in-slide-fades
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-side next-day return minus the coin's drift: 0.00559812; t of the mean, cases of a day taken together: 1.92093 (threshold: confirm: mean > 0 with t >= 2 (and supporting difference > 0); reject: mean < 0 with t <= -2)
- Supporting check: deeper-half minus shallower-half mean short-side unusual move (split at median |forecast|): 0.00351657, passed: True
- Counts: cases: 1250, distinct days: 455
- Decided by: The t of the main mean lies between -2 and 2, which the plan calls inconclusive.
- Reading: Situation checked as today's return above 0 and at most 1 standard deviation of the last 30 daily returns (ddof 1, today included), the recorded depth value (four-day scaled return to yesterday) below 0 and a short forecast, on active bars where 30 returns of history exist in the window, the falling-agitated profile being left to step 3's code; cases are all bars with forecast below 0 and a next bar in the window, drift is the coin's mean next-day return over all its windows, the day-clustered t uses per-day summed deviations with a G/(G-1) correction, and the deeper half is |forecast| strictly above the median, the shallower half at or below it; the plan's 'inconclusive' for too few cases is reported as 'not observable'.
- Size: unusual move +0.56 % (t 1.65, the cases of one day together: 343 days) per case over 1 bars, 0.116 of the coin's usual move (5.33 %); normal drift in its direction -0.14 %, total +0.43 %; 834 cases
Plan: `steps_cards/03_test_plan/night8_fallingagitated_run/plans/058-01.g2.b1.d2.b1.d2.d2_modest-bounce-in-slide-fades_1d.md`
Record: `steps_cards/04_backtest/night8_fallingagitated_run/backtests/058-01.g2.b1.d2.b1.d2.d2_modest-bounce-in-slide-fades_1d`
Measure: `measure.py`
