---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling
line: 7.g patterns
backtest: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 1-day fall relative to its own 20-day daily volatility, and the nearer its close to the day's low, the more it rises over the next 1 day; the larger its vol-scaled 1-day rise, the more it gives back over the next 1 day.
Consequence: A trader should lean against a sharp volatility-scaled daily move for one day only, buying after outsized down days and refusing to chase outsized up days.
Why:
- F1: The day after a large vol-scaled move tends to reverse it: regressing each coin's next-day excess return on the percentile rank of its 1-day return over its 20-day volatility gives a pooled slope of -0.0056, t -2.84 over 4786 days (BTC t -1.67, ETH t -2.30, Spearman -0.07 and -0.08). In raw 1-day-return quintiles, the bottom quintile is followed by next-day excess of +0.34% for BTC (t 2.01, 58% up days, n 575) and +0.32% for ETH (t 1.34, 58% up, n 575), and the top quintile by -0.17% (BTC, t -1.15) and -0.26% (ETH, t -1.39).
- F2: Where the close sits in the day's range points the same way: a close near the day's low is followed by a higher next-day return than a close near its high, pooled slope -0.0035, t -1.91 over 5793 days (BTC t -1.38, ETH t -1.34).
- F3: The reversal does not last. On a 3-day non-overlapping grid, the vol-scaled 1-day return has no slope (pooled t -0.30, n 1571), the raw 1-day return has none (t -0.80), and the 3-day return has none (t +1.65), so the effect fades after about one day.
