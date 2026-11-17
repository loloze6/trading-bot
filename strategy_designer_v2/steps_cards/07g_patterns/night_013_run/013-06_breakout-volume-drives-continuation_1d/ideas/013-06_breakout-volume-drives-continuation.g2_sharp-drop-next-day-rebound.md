---
brief: 013_anchoring-to-recent-high
source-idea: 013-06_breakout-volume-drives-continuation
line: 7.g patterns
backtest: 013-06_breakout-volume-drives-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's fall on a day relative to its own 20-day daily volatility, the larger its rebound over the next 1 day.
Consequence: A trader would buy coins after unusually sharp down days for a one-day bounce rather than sell into them.
Why:
- F1: Each coin's daily return tends to reverse the next day. The pooled slope of the next day's excess return on the previous day's return has t = -8.20, and per-coin t is negative for all six coins (BTC -4.16, ETH -4.98, LTC -3.66, XMR -8.27, XRP -1.02, ZEC -2.21). Dropping days beyond 3 standard deviations still leaves t = -5.27.
- F2: The reversal comes mostly after large falls. In the bottom decile of the previous day's return scaled by 20-day volatility (mean z -1.81), the next day's excess return is +0.57 % (t = 3.87, n = 1491). Deciles 7 and 8 are only -0.31 % and -0.23 %, and the top decile is -0.02 %.
- F3: The one-day reversal fades over time. Its yearly t is -3.13, -1.76, -4.56, -2.43, -0.48 and -3.22 for 2018 to 2023, then +0.56 and +0.56 in 2024 and 2025. Over 3 days it turns into continuation: t = +3.05 on 4,759 non-overlapping cases.
