---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-03_postsettle-recovery-after-uptrend.g3_post-settlement-trend-continuation
line: 7.g patterns
backtest: 017-03_postsettle-recovery-after-uptrend.g3_post-settlement-trend-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Over the next 2 hours, a coin moves against its last hour's return, and the move back is larger the larger that 1-hour return is relative to the coin's own 1-day volatility, most of all when that 1-day volatility is high.
Consequence: In volatile hours, fade a sharp 1-hour spike in proportion to its size instead of chasing it.
Why:
- F2: After a large 1-hour move a coin reverses, and more so when volatility is high: the slope of the next hour's return on the volatility-normalised 1-hour return rises steadily in size across 24-hour-volatility quintiles, from +0.17 bp (t 0.9) in the lowest to -7.46 bp (t -11.8) in the highest; on a non-overlapping 2-hour grid the highest tercile gives -9.41 bp (t -11.9, 68,851 cases).
- F3: That high-volatility reversal holds coin by coin and year by year: it is negative in all six coins (t from -1.87 for ETH to -6.60 for LTC) and in all eight years, significant in seven of them (2022 t -0.83).
