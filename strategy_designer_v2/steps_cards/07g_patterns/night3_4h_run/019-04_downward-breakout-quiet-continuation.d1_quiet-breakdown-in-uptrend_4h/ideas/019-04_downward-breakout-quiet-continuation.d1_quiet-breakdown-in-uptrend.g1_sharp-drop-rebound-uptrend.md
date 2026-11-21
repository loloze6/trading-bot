---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend
line: 7.g patterns
backtest: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: In a coin whose 30-day return is positive, the larger its 1-day fall relative to its own 30-day volatility of four-hour returns, the more it rises over the next three days.
Consequence: Buy a coin after a sharp one-day drop within a rising month, and refuse shorts of such drops, since the rebound that follows is several times a round trip's cost.
Why:
- F1: Across the whole 4h grid, the bars after the largest one-day falls, scaled by the coin's own volatility, are followed by a three-day rise. The lowest decile of the 1-day return over its 180-bar volatility gains +1.47 % unusual over 18 bars (t 3.93, 432 independent cases, strength 0.163). The second decile gains +0.73 % (t 1.60). Deciles 3 to 9 sit between -0.15 % and -0.60 %. This is the sharpest pattern of the roughly 80 groups looked at, and it is well above what that many looks would produce by chance.
- F2: The rebound is concentrated in a rising month. With a positive 180-bar return, the lowest quintile of the scaled 1-day return gains +1.89 % unusual over three days (t 4.04, 401 cases, strength 0.22). With a negative 180-bar return, the same quintile gains only +0.41 % (t 1.10, 457 cases).
- F4: The rebound is positive on all six coins but not in every period. In the lowest quintile, all six coins are positive: +0.23 % BTC (t 0.44), +0.94 % ETH, +1.56 % LTC (t 2.05), +0.81 % XMR, +1.23 % XRP, +1.84 % ZEC (t 2.20). It is positive in 16 of 24 windows (67 %). By year it is uneven: strong in 2020 (+4.0 %, t 4.91), 2021 (+4.3 %, t 2.76) and 2025 (+2.5 %, t 3.21), and negative in 2018 (-1.37 %, t -1.61).
- F7: The rebound is large enough to pay for a trade. Its three-day unusual move in a rising month, +1.89 %, is about 10 times the 0.19 % round-trip cost of this backtest. The tested short's total move of +0.14 % per case was 0.7 times that cost. Its book lost money on five of six coins' trades (mean net trade from -1.3 % on BTC to -8.6 % on ZEC; +0.04 % on XRP).
- F8: The relation is weak away from the tail. Over the whole grid, the rank correlation between the scaled 1-day return and the next three days' unusual move is only -0.03 to -0.09 on each of the six coins (714 cases each). The effect lives in the largest falls, not across the whole range.
