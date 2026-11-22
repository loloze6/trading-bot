---
brief: 023_range-reversion-when-no-trend
source-idea: 023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation.d1_top-of-range-continuation-only
line: 7.g patterns
backtest: 023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation.d1_top-of-range-continuation-only_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 30-day return is negative, the larger its 1-day rise against its 30-day volatility, the more it falls over the next day.
Consequence: In a falling coin, a strong up day is a reason to sell or short for the next day rather than buy it.
Why:
- F4: In coins whose 30-day trend is down (lowest tercile of 30-day log return over volatility), up days are followed by falls that grow with the size of the rise:
- F1: Across all coins, the next day's excess return falls as today's move grows: today's 1-day return divided by its 30-day volatility predicts the next day with slope -0.00184 per unit (t -4.46, 13,060 one-day cases), and the slope is negative in every coin (XMR -0.00466, t -4.93; ETH t -2.09; BTC t -1.74; LTC t -1.77).
