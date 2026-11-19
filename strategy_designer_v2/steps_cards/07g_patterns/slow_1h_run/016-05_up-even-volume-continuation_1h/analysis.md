---
line: 7.g patterns
backtest: 016-05_up-even-volume-continuation_1h
idea tested: 016-05_up-even-volume-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3689 USD
---
## Findings
- **F1:** Across all 24 hours of the day, the coins' next-hour return is clearly highest from the 20:00 and 21:00 UTC bars, with means of +0.000545 (t 6.75) and +0.000436 (t 5.66) against hourly means mostly within ±0.0003. On those two hours pooled, all six coins are positive (t 2.98 to 4.44). Seven of eight years are positive (t 1.90 to 5.66); 2022 is the exception at −0.000218 (t −1.44).
- **F2:** On up moves, the 3-day path efficiency predicts the next 3 days. Efficiency is the net 72-hour log move over the sum of absolute hourly moves. On the non-overlapping 72-bar grid, the top third minus the bottom third of excess forward return is +0.0092 − (−0.0032), Welch t 3.06, n 2865. All six coins are positive on the up side (t 0.88 to 2.18). Inside size terciles of the rise the sign holds but each tercile is weak alone (t 1.13, 0.73, 1.21). In a regression with size and volatility, the past × efficiency term is zero (t −0.01). Much of this effect is therefore the size of the rise.
- **F3:** The volume evenness that the book trades on adds almost nothing on the same grid. Up moves give top minus bottom excess 0.0027 − (−0.0008), t 0.87, and down moves give t −0.21. The book loses: Sharpe −0.32 and mean daily return −0.00018. Three of six coins lose money (XMR −0.00122/day, LTC −0.00059, ZEC −0.00013) while every coin's holding gains 0.0007 to 0.0016/day.
- **F4:** The size of the 3-day move matters in both directions, and the coin does better after large moves of either sign.
- **F5:** Friday bars have the highest next-hour return of the week (+0.000264, t 5.83 across 7 weekdays) and Thursday the lowest (−0.000146, t −3.22). Friday's edge is positive in seven of eight years (2022 −0.000059) and fades over time: t 3.09, 5.61, 2.47 in 2018–2020, then 0.65 in 2025.

## Ideas
- `016-05_up-even-volume-continuation.g1_evening-utc-hour-drift` (from F1): Each day, the coin rises over the two hours after 20:00 UTC by more than in its other hours. The rise is larger the higher its realised hourly volatility over the past 7 days.
- `016-05_up-even-volume-continuation.g2_up-move-path-efficiency-continuation` (from F2, F3): When a coin has risen over the past 3 days, the more directly its price climbed, the more it keeps rising over the next 3 days. Directness is the 3-day net move as a share of the sum of its absolute hourly moves.
- `016-05_up-even-volume-continuation.g3_big-swing-then-rise` (from F4, F2): The larger the coin's absolute return over the past 3 days, in either direction, the more the coin rises over the next 3 days.
- `016-05_up-even-volume-continuation.g4_friday-hourly-up-drift` (from F5): From Friday's hourly bars the coin rises over the next hour by more than on other weekdays. The rise is larger the higher its realised hourly volatility over the past 7 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
