---
brief: 030_absorption-day-close-location
source-idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d1_extreme-surge-low-close-rise
line: 7.g patterns
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d1_extreme-surge-low-close-rise_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The heavier a coin's volume on a day relative to its prior 20-day average, the more the coin rises over the next day, and more so the higher the coin's 20-day volatility.
Consequence: A trader leans long after volume surges in volatile stretches, sized by the surge, and refuses that long bet in calm ones.
Why:
- F5: Volume surge carries its own next-day rise, separate from the close location and the day's return. The log surge coefficient is +0.0018 (t 4.0) on all days and +0.0045 (t 3.4) in the most volatile fifth. The top surge fifth gains +0.39 % beyond drift (t 3.8, 3198 cases), while the other four fifths sit between −0.13 % and 0.00 %.
- F1: The next day reverses the day's return measured against its own 20-day volatility, and this grows with the coin's volatility. The slope of the next-day excess return on that scaled return goes from +0.0012 (t 2.1, 3197 cases) in the calmest fifth of 20-day volatility to −0.0090 (t −7.3, 3197 cases) in the most volatile fifth. In a regression on all days, the interaction with the high-volatility fifth is −0.0087 (t −3.4).
