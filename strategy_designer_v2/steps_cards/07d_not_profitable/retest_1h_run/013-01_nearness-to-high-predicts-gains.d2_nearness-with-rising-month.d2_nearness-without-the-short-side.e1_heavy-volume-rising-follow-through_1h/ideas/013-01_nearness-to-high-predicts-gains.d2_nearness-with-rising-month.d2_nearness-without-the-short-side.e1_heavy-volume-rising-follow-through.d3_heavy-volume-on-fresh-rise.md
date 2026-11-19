---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through
line: 7.d not profitable
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: While a coin's 30-day return is positive, the higher its daily volume relative to its own 20-day average volume, the higher its return over the next 3 days, only while its 3-day return is positive, and the more so the larger that 3-day return.
Consequence: A trader should hold heavy-volume longs in a rising coin when the last three days have also risen, and stand aside when the coin has been flat, where the position loses after fees.
Why:
- F6: While in position, bars whose past 3-day return is in the top quartile (above +5.6 %) net 6.13. Bars whose 3-day return is in the second quartile (-3.1 % to +0.9 %) net -0.48, with the coin falling 0.27 bp per hour.
- F1: Fees take a large share of the book's gain: summed over bars and coins, the position's gain before costs is 11.50 and fees are 4.70, or 41 % of it. The forecast changes 4.12 times per coin-day, and the book trades 0.92 times per day. The book's mean daily return is 0.000367, against 0.001179 for holding the coins.
