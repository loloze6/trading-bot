---
line: 7.g patterns
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.g1_volatile-regime-fall-rebound_1d
idea tested: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.g1_volatile-regime-fall-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3661 USD
---
## Findings
- **F1:** On falling days, a pooled regression of the next-day excess return gives the close's distance from the day's high (low close) times log volume against its 20-day mean a coefficient of +0.0181 (t 4.10, n 7151), and low close alone +0.0099 (t 2.92). The fall's own depth in usual moves adds nothing once these are in (+0.0001, t 0.11). So the tested idea's rebound is carried by closes near the low on heavy volume, not by how deep the fall was.
- **F2:** Falling days in the top volume tercile that closed in the bottom third of their range gained +0.89 % excess the next day (t 4.78, n 870). The same low closes on low volume gained −0.09 % (t −0.54, n 795), and high-volume falls that closed near the high gained +0.14 % (t 0.67, n 749).
- **F3:** On all days, ranked by a graded score of low close times relative volume, next-day excess return rises steadily by quintile: −0.16 %, −0.14 %, −0.12 %, −0.01 %, then +0.37 % in the top quintile (t 3.64, n 2922). Over non-overlapping 3-day stretches the top quintile gains +0.64 % (t 2.01, n 888).
- **F4:** The top-score quintile is positive in all six coins, from +0.20 % (BTC) to +0.50 % (ETH), but only ETH reaches t ≥ 2. It is concentrated in 2020 (+1.09 %, t 3.28) and 2021 (+1.18 %, t 3.21) and near zero in 2019, 2022 and 2024, the same uneven pattern as the tested idea's deep falls (2020 t 3.00, 2021 t 3.71).
- **F5:** Inside the tested idea's positive forecasts, the close location splits the result:
- **F6:** The top-score cases the idea misses are flat: up days at −0.22 % (t −0.78, n 508). Those where the idea is long earn +0.50 % (t 4.60, n 2413). That is about 2.6 times the 0.19 % cost of a trade, against the tested idea's 1.1 times for its unusual move.
- **F7:** Other angles did not give a graded pattern that stands out against the many groups looked at:

## Ideas
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.g1_volatile-regime-fall-rebound.g1_heavy-volume-low-close-rebound` (from F1, F2, F3, F6): The heavier a coin's day volume against its average of the past 20 days, and the nearer the day's close sits to the day's low, the more the coin rises over the next day. The rise grows with both together: a close at the low on heavy volume is followed by the largest gains.
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.g1_volatile-regime-fall-rebound.g2_fall-closing-at-low-rebounds` (from F1, F5): The more a coin's one-day fall ends with its close near the day's low rather than recovered toward the high, the more the coin rises over the next day. The rebound after a fall grows with how near the low the day closed, more than with how deep the fall was.
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.g1_volatile-regime-fall-rebound.g3_low-close-three-day-rebound` (from F3, F6): The heavier a coin's day volume against its average of the past 20 days and the nearer its close sits to the day's low, the more the coin rises over the next three days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
