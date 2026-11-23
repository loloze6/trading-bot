---
line: 7.d confirmed, not profitable
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d1_extreme-surge-low-close-rise_1d
idea tested: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d1_extreme-surge-low-close-rise
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4024 USD
---
## Findings
- **F1:** The deepest fall that failed Calmar was −41.7 % over 311 days, from w1 to w3, while holding the coins fell 66.4 %; in w1–w3 the strongest positions (forecast above 10, mean position 0.84) lost −1.48 in summed next-day gain with a mean next-day return of −0.19 %, although over all windows that same band earned +12.34 net of fees.
- **F2:** Holding only the stronger readings does not lift Calmar in a rebuilt book: 0.54 with every bar, 0.544 above forecast 5, 0.45 above 10 and 0.44 above 15, with the deepest fall staying at −0.38 to −0.40. A threshold on the same 1-day bet keeps the falls and gives up return.
- **F3:** The effect is larger over two days than over one: on forecast-above-10 bars, on non-overlapping grids, the excess return is +0.36 % over 1 day (t 4.11, 3895 cases) and +0.83 % over 2 days (t 4.71, 1980 cases). It fades to +0.51 % over 3 days (t 1.94, 1221) and +0.08 % over 5 days (t 0.24, 820). A 2-day holding captures more than twice the move per trade for one cost of 0.19 %.
- **F4:** The gain is graded by the close's position more than by the surge, and the two compound:
- **F5:** The weak readings cost more than they earn: bars with forecast ≤ 5 (11347 of 17524) made +0.55 gross but paid 2.51 in fees, −1.95 net. The 98 % of days in a position is mostly small, fee-eating exposure.
- **F6:** A trend filter is not a repair, because the signal works on both sides of the 50-day mean: a surge above 1.5× with a close in the lower 40 % of the range earns +0.83 % (t 3.15, 371 cases) above it and +0.87 % (t 3.28, 570 cases) below it. Non-signal bars below the 50-day mean earn −0.20 % (t −3.58, 6973 cases), and the book still held 0.24 on them.

## Ideas
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d1_extreme-surge-low-close-rise.d1_absorbed-selling-two-day-rise` (from F3, F1, F2): The heavier a coin's volume on a day relative to its own prior 20-day average, and the nearer that day's close sits to its low, the more the coin rises over the next two days. The rise grows faster than the volume surge.
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d1_extreme-surge-low-close-rise.d2_close-at-low-grades-surge` (from F4, F5, F6): On a day of heavy volume relative to the coin's prior 20-day average, the nearer the close sits to the day's low, the larger the coin's rise over the next day. The rise per unit of volume surge grows steeply as the close approaches the very low of the range.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
