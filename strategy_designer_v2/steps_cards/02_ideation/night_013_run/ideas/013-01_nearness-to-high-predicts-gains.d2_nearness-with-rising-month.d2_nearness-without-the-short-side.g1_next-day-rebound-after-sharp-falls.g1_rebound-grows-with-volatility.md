---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.g1_next-day-rebound-after-sharp-falls
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.g1_next-day-rebound-after-sharp-falls_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's one-day fall relative to its own 20-day volatility of daily returns, the higher its return over the next 1 day, and the rebound per unit of fall grows the higher the coin's 20-day volatility stands against its own past 120 days.
Consequence: A trader can size one-day rebound buys after sharp falls up when the coin's volatility is high against its own past, and refuse them when its volatility is low.
Why:
- F1: The rebound after down days lives in high volatility: on down days split by the coin's 20-day volatility rank within its own past 120 days, the slope of next-day excess return on the scaled fall is 0.0073 (t 3.45, n 1459) in the high tercile, 0.0007 (t 0.37) in the middle and −0.0011 (t −0.59) in the low; the fall × volatility-rank interaction has t 3.57, and fall alone has t −1.84.
- F2: The book's timing gain follows the same split: the mean daily position × excess return is 0.00153 (sum 4.52) in the high-volatility tercile, 0.00044 in the middle and −0.00063 (sum −1.87) in the low, so low-volatility days give back about 40% of what high-volatility days earn.
- F3: For falls beyond one usual move (z < −1), next-day excess return is 0.0121 (t 3.54, n 373) in high volatility against −0.0028 (t −1.19, n 374) in low; high-minus-low Welch t is positive in 5 of 6 coins (BTC 2.44, ZEC 2.23, ETH 1.71, XRP 1.71, LTC 1.17), and XMR is the exception at −0.48.
- F6: The rebound is not steady over time: for z < −1 it is 0.0150 (t 3.49) in 2020 and 0.0146 (t 3.43) in 2021, but between −0.0013 and 0.0043 (all |t| < 1.1) in 2022–2025, which fits the book's weak Calmar of 0.43.
