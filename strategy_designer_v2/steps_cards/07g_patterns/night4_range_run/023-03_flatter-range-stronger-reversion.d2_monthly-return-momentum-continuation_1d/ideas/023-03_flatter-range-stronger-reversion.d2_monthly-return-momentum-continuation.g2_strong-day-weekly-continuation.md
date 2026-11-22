---
brief: 023_range-reversion-when-no-trend
source-idea: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation
line: 7.g patterns
backtest: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's rise over the past day, relative to its usual daily move over the past 20 days, the larger its further rise over the next 5 days.
Consequence: An unusually strong up day is a reason to hold or add a long for the coming week rather than to fade it.
Why:
- F3: Over 5 days, large up days continue instead of reversing. On the 5-day grid the top quintile of the day's move against its 20-day volatility was followed by a +1.63 % excess 5-day return (t 3.24, 570 cases). Days of +1 to +2 standard deviations were followed by +1.58 % (t 2.21, 255 cases), and days above +2 by +2.47 % (t 1.96, 110 cases). The 5-day slope is positive in 5 of 8 years (2019 t 2.79, 2023 t 2.22).
- F5: Long positions carry the book's gain. Long bars earned +0.174 % per bar (6633 bars) and short bars −0.015 % (6424 bars). Both the worst and the best deciles of bar gains come from large mostly-long positions after big 30-day rises (worst: mean |allocation| 0.86, 30-day return +13.3 %; best: 0.90, +16.1 %), which is where the Calmar-failing falls sit.
