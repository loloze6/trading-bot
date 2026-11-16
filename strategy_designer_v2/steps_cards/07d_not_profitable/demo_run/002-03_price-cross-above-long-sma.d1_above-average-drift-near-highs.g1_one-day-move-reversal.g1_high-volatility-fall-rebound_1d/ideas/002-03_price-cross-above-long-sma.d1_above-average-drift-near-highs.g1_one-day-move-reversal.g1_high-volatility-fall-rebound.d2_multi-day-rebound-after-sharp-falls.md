---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.g1_high-volatility-fall-rebound
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.g1_high-volatility-fall-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 20-day volatility is high compared with its own past levels, the larger its one-day fall relative to its usual daily move over the past 20 days, the larger its rise over the next three days.
Consequence: A trader would hold the rebound from a sharp fall for several days instead of one, collecting more of the move per trade.
Why:
- F1: The book's gain comes almost entirely from its largest forecasts. The top forecast tercile (mean forecast 13.6, n 613) earned 0.00699 per active bar, while the lower two terciles earned 0.00004 (n 1226) and 0.00041 (n 613). With the book active on only 14.0 % of bars at a mean allocation of 0.247, its mean daily return is only 0.000209, against 0.00118 for holding.
- F2: Most signal bars are small falls that do not rebound. Of 1408 signal bars with a measured fall, 1153 had a vol-scaled fall between -1 and 0, with a next-day excess of 0.00196 (t 1.17) and a gain of 0.00042. Falls between -1.5 and -1 gave 0.01655 (t 3.07, n 163), and falls below -3 gave 0.201 (t 7.74, n 8).
- F5: The rebound does not end after one day. Over all 1698 signal bars, the excess over the coin's mean was 0.00515 over 1 day (t 3.47), 0.00742 over 3 days (t 3.18, n 1674) and 0.00876 over 5 days (t 2.84, n 1661). A one-day hold captures well under the full move.
