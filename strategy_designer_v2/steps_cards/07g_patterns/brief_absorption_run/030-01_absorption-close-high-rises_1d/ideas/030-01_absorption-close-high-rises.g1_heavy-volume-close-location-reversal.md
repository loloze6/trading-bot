---
brief: 030_absorption-day-close-location
source-idea: 030-01_absorption-close-high-rises
line: 7.g patterns
backtest: 030-01_absorption-close-high-rises_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: On a day when a coin's volume is far above its 20-day average, the closer its close sits to the day's high, the more the coin falls over the next 1 to 2 days, and the closer to the low, the more it rises. The effect is larger the heavier that day's volume is relative to its 20-day average.
Consequence: A close at an extreme of the range on heavy volume is a reason to bet on a short pullback against it over the next day or two, not on continuation.
Why:
- F1: On days with volume at least 2x the prior 20-day mean, the close location (from -1 at the low to +1 at the high) predicts the next day's unusual move against itself: the slope is -0.285 of the coin's usual 1-day move per unit of close location, t -4.68, on 1292 non-overlapping cases. It holds on both flat-body days (-0.323, t -2.25, n 341) and wide-body days (-0.276, t -4.12, n 951).
- F2: This one-day reversal grows with volume. The slope is -0.026 (t -1.51, n 8994) when volume is under its 20-day mean, -0.063 (t -2.25, n 4214) at 1-2x, and -0.285 (t -4.68, n 1292) at 2x or more. Across all days it is -0.066 (t -4.86, n 17379), and it stands out from the roughly 100 slopes and groups examined.
- F3: On heavy-volume days the reversal fades with the horizon and is gone by 5 days. The slope is -0.235 at 2 days (t -3.00, n 665), -0.188 at 3 days (t -1.89, n 447) and +0.189 at 5 days (t 1.82, n 275). This explains why the 5-day test of continuation found nothing (slope -0.00016, t -0.39, 369 cases).
