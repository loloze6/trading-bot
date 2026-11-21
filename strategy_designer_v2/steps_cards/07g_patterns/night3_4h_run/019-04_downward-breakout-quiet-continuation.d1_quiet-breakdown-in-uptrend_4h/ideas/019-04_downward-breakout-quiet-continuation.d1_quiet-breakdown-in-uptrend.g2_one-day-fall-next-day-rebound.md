---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend
line: 7.g patterns
backtest: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: The larger a coin's 1-day fall relative to its own 30-day volatility of four-hour returns, the more it rises over the next day.
Consequence: A sharp one-day drop is a reason to take a short-term long and to refuse a short opened on it.
Why:
- F3: The same rebound shows at a one-day horizon. On the 6-bar grid, the lowest quintile of the scaled 1-day return gains +0.49 % unusual over the next 6 bars (t 5.04, 3046 cases, strength 0.10). Quintiles 2 to 5 gain between +0.00 % and -0.18 %.
- F1: Across the whole 4h grid, the bars after the largest one-day falls, scaled by the coin's own volatility, are followed by a three-day rise. The lowest decile of the 1-day return over its 180-bar volatility gains +1.47 % unusual over 18 bars (t 3.93, 432 independent cases, strength 0.163). The second decile gains +0.73 % (t 1.60). Deciles 3 to 9 sit between -0.15 % and -0.60 %. This is the sharpest pattern of the roughly 80 groups looked at, and it is well above what that many looks would produce by chance.
- F8: The relation is weak away from the tail. Over the whole grid, the rank correlation between the scaled 1-day return and the next three days' unusual move is only -0.03 to -0.09 on each of the six coins (714 cases each). The effect lives in the largest falls, not across the whole range.
