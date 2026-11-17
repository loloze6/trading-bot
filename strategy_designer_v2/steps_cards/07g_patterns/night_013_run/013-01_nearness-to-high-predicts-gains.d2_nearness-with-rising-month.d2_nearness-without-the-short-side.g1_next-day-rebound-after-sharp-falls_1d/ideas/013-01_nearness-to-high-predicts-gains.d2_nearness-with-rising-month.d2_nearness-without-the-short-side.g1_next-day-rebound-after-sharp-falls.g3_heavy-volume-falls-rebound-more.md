---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.g1_next-day-rebound-after-sharp-falls
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.g1_next-day-rebound-after-sharp-falls_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's one-day fall relative to its 20-day volatility, the higher its return over the next 1 day, and the rebound per unit of fall grows with that day's volume relative to the coin's own 20-day volume.
Consequence: A trader can favour rebound buys after sharp falls on heavy volume, and refuse them after sharp falls on thin volume.
Why:
- F5: Heavy volume strengthens the rebound: for z < −1, next-day excess return is 0.0102 (t 4.02, n 614) in the high volume-surprise tercile against 0.0018 (t 0.91) in the low; the fall × volume-z interaction is only t 2.05, so this is weak given how many angles were checked.
- F3: For falls beyond one usual move (z < −1), next-day excess return is 0.0121 (t 3.54, n 373) in high volatility against −0.0028 (t −1.19, n 374) in low; high-minus-low Welch t is positive in 5 of 6 coins (BTC 2.44, ZEC 2.23, ETH 1.71, XRP 1.71, LTC 1.17), and XMR is the exception at −0.48.
