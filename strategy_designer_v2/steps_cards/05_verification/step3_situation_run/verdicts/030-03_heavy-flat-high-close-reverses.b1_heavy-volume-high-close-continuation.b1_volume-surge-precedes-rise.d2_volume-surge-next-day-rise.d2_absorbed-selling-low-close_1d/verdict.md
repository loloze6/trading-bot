---
plan: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close_1d
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of slope of excess next-day return on forecast, heavy-volume days, same-day cases pooled: 2.28031; slope t (date-clustered OLS): 2.28031 (threshold: slope t >= 2 with top-minus-bottom > 0 confirms; slope t <= -2 rejects; else inconclusive; needs >= 100 heavy-volume days over >= 50 distinct dates)
- Supporting check: top-third minus bottom-third forecast mean excess next-day return (Welch t 2.277): 0.00589795, passed: True
- Counts: heavy-volume days: 3105, distinct dates: 1404
- Decided by: Confirm: the slope t is 2 or more and the top-minus-bottom difference is above 0.
- Reading: Heavy-volume days are the bars with regime 'trending' and a next-day close in the same window, including those with forecast 0; the slope's t pools same-day cases with standard errors clustered by date (CR1); thirds are the lowest and highest n//3 cases by forecast with ties ordered by time then coin; the coin mean is its mean 1-day return over all its windows.
- Size: unusual move +0.38 % (t 2.11, the cases of one day together: 1132 days) per case over 1 bars, 0.080 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.50 %; 2201 cases
Plan: `steps_cards/../../../../../tmp/claude-0/-home-user-trading-bot/9a8c137d-677e-59d2-8d4c-7c621473a28a/scratchpad/n3/B/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close_1d.md`
Record: `steps_cards/../../../../../tmp/claude-0/-home-user-trading-bot/9a8c137d-677e-59d2-8d4c-7c621473a28a/scratchpad/n3/steps/bt/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close_1d`
Measure: `measure.py`
