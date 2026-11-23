---
plan: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d1_extreme-surge-low-close-rise_1d
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d1_extreme-surge-low-close-rise
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess next-day return of long cases (vs coin mean daily return): 0.0201483; t of the mean, cases summed per day: 2.94574 (threshold: confirm: mean > 0 with t >= 2 and check passes; reject: mean < 0 with t <= -2; at least 30 distinct case days)
- Supporting check: cases minus low-volume low-close controls, mean excess next-day return (Welch t >= 1): 0.0190365, passed: True
- Counts: distinct case days: 157, cases: 235, control days: 1878
- Decided by: Mean excess next-day return above 0 with t >= 2 and the supporting check passes (confirm rule).
- Reading: A case is a bar whose forecast is >= 2 while the previous bar in the same window is exactly 0 (a window's first bar has no known previous forecast and is not a case); the t clusters case deviations by UTC day; the volume ratio uses the prior 20 bars inside the window, falling back to the recorded absorb value divided by the close's distance from the high on the first 20 bars; the supporting check uses Welch t on case-level excess returns of these same cases against control days recomputed from prices; the plan's 'fewer than 30 distinct case days' minimum is applied as not observable.
- Size: unusual move +2.05 % (t 3.04, the cases of one day together: 159 days) per case over 1 bars, 0.433 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +2.17 %; 238 cases
Plan: `steps_cards/../../../../../tmp/claude-0/-home-user-trading-bot/9a8c137d-677e-59d2-8d4c-7c621473a28a/scratchpad/n3/B/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d1_extreme-surge-low-close-rise_1d.md`
Record: `steps_cards/../../../../../tmp/claude-0/-home-user-trading-bot/9a8c137d-677e-59d2-8d4c-7c621473a28a/scratchpad/n3/steps/bt/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d1_extreme-surge-low-close-rise_1d`
Measure: `measure.py`
