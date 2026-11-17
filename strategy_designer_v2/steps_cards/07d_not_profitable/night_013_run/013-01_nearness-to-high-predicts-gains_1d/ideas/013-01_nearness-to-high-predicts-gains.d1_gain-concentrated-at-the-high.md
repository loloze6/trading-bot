---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains
line: 7.d not profitable
backtest: 013-01_nearness-to-high-predicts-gains_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The closer a coin's daily close sits to its highest close of the past 52 weeks, the higher its return over the next 7 days. The rise is concentrated in the last stretch just below the high, so the gain grows faster the nearer the close is to that high. It is larger the stronger the coin's 30-day return.
Consequence: Commit capital mainly to coins pressed against their 52-week high after a strong month, rather than spreading small longs and shorts across the whole range.
Why:
- F1: The book earned too little because it held little: its mean daily return was 0.000114 against holding's 0.00123, with a daily sd of 0.0042 against holding's 0.040, and its average position was only 0.017 of the book (median 0, max 0.54). The book was short on 35.6 % of bars and long on 35.9 %, so its average net exposure stayed near zero.
- F2: Nearly all of the gain came from the top distance decile, closes within about 3 % of the 364-day high: there the next-day excess return was +0.0033 and the position's daily gain was 0.00102. In deciles 0 to 8 the daily gain ranged only from -0.00015 to +0.00026, and the next-day excess showed no ordering by distance.
- F4: Near the high (top 20 % of distance), the following day depended on the coin's 30-day return:
- F5: Over the plan's own 30-day horizon the forecast's slope was not significant (t = 0.95, n = 526). The 30-day excess by forecast quintile was not monotonic: -0.027, -0.031, +0.080, -0.013, -0.008 from the lowest to the highest quintile.
