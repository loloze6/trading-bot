---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-04_thinner-weekend-larger-reversal.b1_thin-weekend-large-moves-reverse.b1_thin-weekend-rises-reverse
line: 7.g patterns
backtest: 026-04_thinner-weekend-larger-reversal.b1_thin-weekend-large-moves-reverse.b1_thin-weekend-rises-reverse_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's 24-hour return is reversed over the next 24 hours more strongly the higher its realised volatility over the past 7 days: in its most volatile weeks, the larger the 24-hour move against its usual move, the larger the opposite move over the next 24 hours.
Consequence: A trader fades a coin's large one-day moves mainly when the coin has been unusually volatile over the past week, and holds back in its calm weeks.
Why:
- F1: Across all coins, a coin's 24-hour move is partly reversed over the next 24 hours, on the non-overlapping 24-hour grid: the slope of the next 24-hour unusual move (in usual moves) on the past 24-hour move is -0.0915 (t -11.74, 16238 cases). In the extreme quintiles, the falls (z -1.24) are followed by +0.468 % (t 4.40, 3251 cases) and the rises (z +1.32) by -0.322 % (t -3.27, 3249 cases).
- F4: The 24-hour reversal is carried by the most volatile stretches. In the top quintile of past-week realised volatility, the correlation of the past 24-hour move with the next 24-hour unusual move is -0.18 (3422 cases). In the four lower quintiles it is +0.02 to -0.02.
