---
brief: 030_absorption-day-close-location
source-idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d1_extreme-surge-low-close-rise
line: 7.d confirmed, not profitable
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d1_extreme-surge-low-close-rise_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: On a day of heavy volume relative to the coin's prior 20-day average, the nearer the close sits to the day's low, the larger the coin's rise over the next day. The rise per unit of volume surge grows steeply as the close approaches the very low of the range.
Consequence: A trader sizes heavy-volume days by how near the close sits to the low rather than by the surge alone. He takes almost no exposure on heavy days that close in the upper half or on faint readings, which removes the fee drag and the losing exposure.
Why:
- F4: The gain is graded by the close's position more than by the surge, and the two compound:
- F5: The weak readings cost more than they earn: bars with forecast ≤ 5 (11347 of 17524) made +0.55 gross but paid 2.51 in fees, −1.95 net. The 98 % of days in a position is mostly small, fee-eating exposure.
- F6: A trend filter is not a repair, because the signal works on both sides of the 50-day mean: a surge above 1.5× with a close in the lower 40 % of the range earns +0.83 % (t 3.15, 371 cases) above it and +0.87 % (t 3.28, 570 cases) below it. Non-signal bars below the 50-day mean earn −0.20 % (t −3.58, 6973 cases), and the book still held 0.24 on them.
