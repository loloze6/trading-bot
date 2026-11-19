---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through
line: 7.d not profitable
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: While a coin's 30-day return is positive, the higher its average daily volume over the last 3 days relative to its own 20-day average volume, the higher its return over the next 3 days.
Consequence: A trader can size a rising coin by its slow volume excess rather than the last day's volume, which holds the same information with far fewer position changes and fees.
Why:
- F1: Fees take a large share of the book's gain: summed over bars and coins, the position's gain before costs is 11.50 and fees are 4.70, or 41 % of it. The forecast changes 4.12 times per coin-day, and the book trades 0.92 times per day. The book's mean daily return is 0.000367, against 0.001179 for holding the coins.
- F5: The forecast's size is not graded within positive forecasts. On the 72-bar grid, its quartiles give mean excess returns of 0.0138, 0.0012, 0.0043 and 0.0147. Grid cases with any positive forecast average 0.0085 (n=1190), and cases with a zero forecast average -0.0001 (n=1647). The slope's t is 1.90.
