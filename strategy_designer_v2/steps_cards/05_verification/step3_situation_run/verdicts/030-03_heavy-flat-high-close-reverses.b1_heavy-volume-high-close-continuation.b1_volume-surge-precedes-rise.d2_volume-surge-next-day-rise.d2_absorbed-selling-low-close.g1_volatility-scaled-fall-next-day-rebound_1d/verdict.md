---
plan: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g1_volatility-scaled-fall-next-day-rebound_1d
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g1_volatility-scaled-fall-next-day-rebound
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess next-day return on case bars (close[t+1]/close[t]-1 minus coin mean daily return): 0.00687924; t of the mean, cases of one day summed: 1.29529 (threshold: mean above 0 with t >= 2 (and supporting check) confirms; below 0 with t <= -2 rejects; at least 30 case days)
- Supporting check: upper-half minus lower-half mean excess return, split at median forecast: -0.000121552, passed: False
- Counts: cases (case days): 200, case bars: 492
- Decided by: t lies between -2 and 2.
- Reading: Cases are bars in regime mean_reversion with forecast > 0 and a next bar in the same window; the t uses per-day sums of the excess returns over the case days; the median split puts forecasts above the median in the upper half and at or below it in the lower half (>= vs < if the upper half would be empty).
- Size: unusual move +0.41 % (t 0.78, the cases of one day together: 192 days) per case over 1 bars, 0.089 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.52 %; 462 cases
Plan: `steps_cards/../../../../../tmp/claude-0/-home-user-trading-bot/9a8c137d-677e-59d2-8d4c-7c621473a28a/scratchpad/n3/B/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g1_volatility-scaled-fall-next-day-rebound_1d.md`
Record: `steps_cards/../../../../../tmp/claude-0/-home-user-trading-bot/9a8c137d-677e-59d2-8d4c-7c621473a28a/scratchpad/n3/steps/bt/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g1_volatility-scaled-fall-next-day-rebound_1d`
Measure: `measure.py`
