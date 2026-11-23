---
brief: 030_absorption-day-close-location
source-idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d1_extreme-surge-low-close-rise
line: 7.d confirmed, not profitable
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d1_extreme-surge-low-close-rise_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The heavier a coin's volume on a day relative to its own prior 20-day average, and the nearer that day's close sits to its low, the more the coin rises over the next two days. The rise grows faster than the volume surge.
Consequence: A trader holds each heavy-volume, low-close day for two days instead of one, so each trade captures more than twice the move for a single cost of 0.19 %.
Why:
- F3: The effect is larger over two days than over one: on forecast-above-10 bars, on non-overlapping grids, the excess return is +0.36 % over 1 day (t 4.11, 3895 cases) and +0.83 % over 2 days (t 4.71, 1980 cases). It fades to +0.51 % over 3 days (t 1.94, 1221) and +0.08 % over 5 days (t 0.24, 820). A 2-day holding captures more than twice the move per trade for one cost of 0.19 %.
- F1: The deepest fall that failed Calmar was −41.7 % over 311 days, from w1 to w3, while holding the coins fell 66.4 %; in w1–w3 the strongest positions (forecast above 10, mean position 0.84) lost −1.48 in summed next-day gain with a mean next-day return of −0.19 %, although over all windows that same band earned +12.34 net of fees.
- F2: Holding only the stronger readings does not lift Calmar in a rebuilt book: 0.54 with every bar, 0.544 above forecast 5, 0.45 above 10 and 0.44 above 15, with the deepest fall staying at −0.38 to −0.40. A threshold on the same 1-day bet keeps the falls and gives up return.
