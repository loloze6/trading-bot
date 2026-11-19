---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-uptrend-momentum-near-highs
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_short-horizon-uptrend-momentum-near-highs_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin closes above its 8-day moving average, the larger its 20-hour rise and the nearer its close to its 20-hour high, the lower its return over the next day.
Consequence: Do not chase a fresh hourly push to a new short-term high inside an uptrend for a one-day move. Expect it to give back part of the move first.
Why:
- F4: At other horizons the effect does not show. The slope t is 0.92 at 168 bars (1,218 cases) and 0.64 at 720 bars (271 cases). At 24 bars it reverses to −3.25 (8,740 cases), where positive-forecast grid bars trail zero-forecast ones by Welch t −2.51.
- F5: The book's daily gross gain per coin-day (+0.000083) is smaller than its gain from the market's own rise (+0.000214), so its timing part is negative (−0.000131). Its fees (0.001825 per coin-day, with 3.8 trades a day of 4-hour median length) make it lose −0.0017 a day. The book thus trades the 1-day reversal of F4, not the two-week drift.
