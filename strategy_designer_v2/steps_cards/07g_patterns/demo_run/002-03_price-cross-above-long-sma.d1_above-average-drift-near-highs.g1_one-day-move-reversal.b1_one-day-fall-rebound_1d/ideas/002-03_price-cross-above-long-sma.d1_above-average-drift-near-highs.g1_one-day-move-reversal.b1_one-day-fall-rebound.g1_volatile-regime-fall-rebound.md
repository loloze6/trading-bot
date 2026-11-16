---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.b1_one-day-fall-rebound
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.b1_one-day-fall-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's one-day fall relative to the standard deviation of its daily returns over the past 20 days, the larger its rise over the next day. The rise grows further the higher that 20-day volatility stands relative to its own level over the past 120 days.
Consequence: A trader would buy into a coin's large one-day falls mainly when its volatility is high relative to its recent past, sizing by fall times volatility rank, and would refuse to buy falls in calm periods.
Why:
- F1: The tested rebound after a fall only appears when the coin's volatility is high. Among down days, the mean of (fall in sigma × next-day excess return) in the top tercile of 20-day volatility (ranked against the coin's past 120 days) was 0.0050 (t 2.22, n 752) in windows w1–w12 and 0.0089 (t 2.89, n 910) in w13–w24. The low tercile was negative in both halves: −0.0011 (t −0.68) and −0.0020 (t −1.22).
- F2: The grading by fall size sharpens with volatility. The correlation of the scaled fall with the next-day excess return is −0.013 in the low-volatility tercile, 0.041 in the middle and 0.097 in the high (n 1762, 1314, 1662). Multiplying the fall by the volatility rank lifts the correlation from 0.042 to 0.093 over 4738 down days.
- F3: In the high-volatility tercile the rebound is positive in all six coins. The mean of (fall × next-day excess) runs from 0.0054 (ZEC, t 1.20) to 0.0105 (XRP, t 1.84), with 238 to 316 bars per coin, so no single coin carries it.
