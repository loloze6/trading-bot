---
brief: 013_anchoring-to-recent-high
source-idea: 013-03_breakout-above-high-continues.g1_near-30-day-high-continuation
line: 7.g patterns
backtest: 013-03_breakout-above-high-continues.g1_near-30-day-high-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 20-day volatility is high, the larger its 1-day return relative to that volatility, the lower its return over the next 1 day, with sharp down days followed by the strongest rebounds.
Consequence: In volatile conditions a trader would buy the day after an outsized drop and fade the day after an outsized rise, for a one-day hold.
Why:
- F4: A 1-day move scaled by 20-day volatility is followed by a next-day reversal. The pooled slope t is −4.99, negative in w1–w12 (t −3.42) and in w13–w24 (t −3.65), and negative in all six coins (XMR t −5.26, ETH −2.63, LTC −2.22). It is gone at 3 days (non-overlapping t −0.33, n 5003).
- F5: The reversal is graded and lives in high-volatility conditions. When 20-day volatility is above the coin's median, next-day excess return runs +0.0245 after moves below −2σ (n 170), +0.0098 after −2σ to −1σ, −0.0040 after 0 to +1σ and −0.0075 after more than +2σ. In low-volatility conditions the pattern is flat or inverted (−0.0043 after below −2σ, +0.0057 after above +2σ).
