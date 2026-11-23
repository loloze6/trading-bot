---
brief: 030_absorption-day-close-location
source-idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g2_heavy-volume-low-close-reversal
line: 7.g patterns
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g2_heavy-volume-low-close-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's one-day fall against its own 20-day volatility, and the lower that day's close sits within its range on heavy volume against its prior 20-day average, the more the coin rises over the next day.
Consequence: A trader sizes the one-day rebound long by how many volatility units the coin fell and how close to its low it closed on heavy volume, and refuses the long after mild or high-closing falls.
Why:
- F5: Measured in units of the coin's prior 20-day volatility, falls of 1 to 1.5 are followed by +0.62 % (t 3.52, 861 cases) and falls of 2 to 3 by +0.61 % (t 2.34). Small rises of 0 to 1 are followed by about −0.2 % (t −2.3 to −2.5).
- F6: In a joint regression of the next-day excess return, close location × volume ratio keeps t 6.30 and the size of the fall in volatility units keeps t 2.50. The range ratio is negative (t −2.87) when up and down days are pooled.
- F7: Among days falling more than 1.5 volatility units, heavy-volume days that closed in the bottom 30 % of their range gave +1.60 % next day (t 4.70, 331 cases). The other three groups were within ±0.7 % (|t| ≤ 1.34).
