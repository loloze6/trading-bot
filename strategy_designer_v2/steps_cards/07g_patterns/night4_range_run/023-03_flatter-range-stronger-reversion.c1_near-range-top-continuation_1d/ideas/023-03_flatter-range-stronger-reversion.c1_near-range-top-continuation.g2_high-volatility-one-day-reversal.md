---
brief: 023_range-reversion-when-no-trend
source-idea: 023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation
line: 7.g patterns
backtest: 023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's past 20 days have been highly volatile, the larger its one-day move relative to that volatility, the more the coin moves back the other way over the next day.
Consequence: In a volatile coin, a sharp one-day fall is a reason to buy for the following day, and a sharp one-day rise is a reason not to chase it.
Why:
- F2: After a large one-day move in a high-volatility coin, the next day tends to go the other way. In the top third of each coin's 20-day volatility, the next-day excess return has a slope of −0.134 standard deviations per unit of the one-day z, with t −7.39 over 4830 days. The same slope is +0.020 (t 1.89) in the low-volatility third, and −0.038 (t −4.61) pooled over 14500 days.
- F3: The one-day reversal is strongest after the largest falls. The bottom fifth of one-day z is followed by +0.39 % next-day excess return (t 4.04, 2900 days), which is twice the 0.19 % cost of a trade. It is negative in all eight years, with t ≤ −3 in 2018, 2020 and 2023, and negative in all six coins, ranging from −0.006 for ZEC to −0.093 for XMR (t −4.67).
