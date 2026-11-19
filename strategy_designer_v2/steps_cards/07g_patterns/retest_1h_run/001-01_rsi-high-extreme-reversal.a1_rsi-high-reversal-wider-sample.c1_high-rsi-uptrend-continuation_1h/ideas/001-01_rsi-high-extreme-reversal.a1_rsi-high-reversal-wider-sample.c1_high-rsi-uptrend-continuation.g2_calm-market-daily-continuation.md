---
brief: 001_rsi-extremes-predict-next-move
source-idea: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation
line: 7.g patterns
backtest: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's volatility over the last 7 days is low relative to its volatility over the last 60 days, the larger its 24-hour return measured in units of its recent volatility, the further the coin moves the same way over the next 24 hours.
Consequence: In a calm market, a trader can lean with the last day's move, in proportion to its size, for about one day, instead of fading it.
Why:
- F2: In 24-hour steps on a non-overlapping grid, a coin's past 24-hour return in volatility units predicts reversal only when its 7-day volatility is high against its 60-day volatility: the slope of the next 24-hour excess return on the past return is -0.080 (t -5.37, n 4309) in the top tercile of that ratio, +0.006 (t 0.38) in the middle tercile and +0.060 (t 2.60) in the bottom tercile, and the interaction of past return with the volatility ratio has t -5.70 (n 12926).
- F5: Using the 7-day volatility level alone gives the same split: the reversal slope is -0.087 (t -6.64) in the highest volatility tercile against +0.054 (t 2.70) in the lowest, while the unconditional slope by coin stays between t -2.25 and +1.00.
