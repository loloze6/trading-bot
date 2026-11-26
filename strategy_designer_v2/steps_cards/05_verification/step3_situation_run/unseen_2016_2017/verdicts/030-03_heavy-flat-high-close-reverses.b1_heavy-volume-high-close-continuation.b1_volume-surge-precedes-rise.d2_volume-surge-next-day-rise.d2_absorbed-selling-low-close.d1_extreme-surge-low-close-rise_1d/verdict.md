---
plan: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d1_extreme-surge-low-close-rise_1d
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d1_extreme-surge-low-close-rise
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess next-day return of long cases (vs coin mean daily return): 0.00624889; t of the mean, cases summed per day: 0.419592 (threshold: confirm: mean > 0 with t >= 2 and check passes; reject: mean < 0 with t <= -2; at least 30 distinct case days)
- Supporting check: cases minus low-volume low-close controls, mean excess next-day return (Welch t >= 1): 0.0114615, passed: False
- Counts: distinct case days: 31, cases: 38, control days: 297
- Decided by: The t of the mean excess next-day return lies between -2 and 2 (inconclusive rule).
- Reading: A case is a bar whose forecast is >= 2 while the previous bar in the same window is exactly 0 (a window's first bar has no known previous forecast and is not a case); the t clusters case deviations by UTC day; the volume ratio uses the prior 20 bars inside the window, falling back to the recorded absorb value divided by the close's distance from the high on the first 20 bars; the supporting check uses Welch t on case-level excess returns of these same cases against control days recomputed from prices; the plan's 'fewer than 30 distinct case days' minimum is applied as not observable.
- Size: unusual move +0.62 % (t 0.43, the cases of one day together: 31 days) per case over 1 bars, 0.125 of the coin's usual move (7.55 %); normal drift in its direction +0.94 %, total +1.56 %; 38 cases
Plan: `steps_cards/03_test_plan/step3_situation_run/plans/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d1_extreme-surge-low-close-rise_1d.md`
Record: `steps_cards/04_backtest/step3_situation_run/unseen_2016_2017/backtests/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d1_extreme-surge-low-close-rise_1d`
Measure: `measure.py`
