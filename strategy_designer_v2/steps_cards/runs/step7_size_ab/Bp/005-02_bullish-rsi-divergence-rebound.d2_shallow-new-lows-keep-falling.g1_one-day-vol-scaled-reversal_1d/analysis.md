---
line: 7.d not profitable
backtest: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal_1d
idea tested: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3490 USD
---
## Findings
- **F1:** The book loses because its trades cost more than its forecast earns. Before fees the position earns 2.31 bps a day, the fees take 3.59 bps a day, and the book ends at -1.31 bps a day on 0.44 of the book turned over each bar. This matches the stated size: the total move per case is 0.9 times the 0.17 % cost of a buy and a sell.
- **F2:** The short side carries the loss. Short bars earn -2.81 bps a day before fees (n 2958), and -3.51 bps of that is the position's share of the coins' own rise. Long bars earn +7.69 bps a day before fees (n 2823).
- **F3:** The short side loses most when the coin's 50-day return is positive. There, short bars earn -7.40 bps a day before fees (n 995) and long bars +12.24 bps (n 849). When the 50-day return is negative, short bars earn +6.09 bps (n 710).
- **F4:** The one-day rebound is concentrated in the largest falls and is larger when the coin's 50-day return is positive. After falls beyond 1.5 usual moves, the next-day excess is +0.71 % with t 1.86 (83 cases) when the 50-day return is positive, and +0.29 % with t 0.57 (127 cases) when it is negative.
- **F5:** The give-back after rises appears mainly when the coin's 50-day return is negative. After rises beyond 1.5 usual moves, the next-day excess is -0.78 % with t -1.47 (85 cases) when the 50-day return is negative, and only -0.10 % with t -0.35 (165 cases) when it is positive.
- **F6:** Small daily moves carry no edge but still pay fees.
- **F7:** Holding the rebound longer does not help. After falls beyond one usual move, the excess return is +0.32 % over 1 day, +0.15 % over 2 days, +0.07 % over 3 days and -0.16 % over 5 days.
- **F8:** The idea's part about where the close sits in the day's range does not grade the rebound as stated. On down days, closes in the lowest quarter of the range are followed by +0.11 % (896 cases), and closes in the second quarter by +0.23 % (997 cases).

## Ideas
- `005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d1_trend-conditioned-one-day-reversal` (from F2, F3, F4, F5, F7): The larger a coin's 1-day fall relative to its own 20-day daily volatility, the more it rises over the next 1 day, and the higher its 50-day return the larger that rise. The larger its vol-scaled 1-day rise, the more it gives back over the next 1 day, only while its 50-day return is negative, and the more negative that return the larger the give-back.
- `005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_rebound-after-outsized-falls` (from F1, F4, F6, F7): The larger a coin's 1-day fall measured in its own 20-day daily volatility, the more it rises over the next 1 day, and this rise grows faster than the size of the fall itself, so the largest falls carry most of the rebound.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
