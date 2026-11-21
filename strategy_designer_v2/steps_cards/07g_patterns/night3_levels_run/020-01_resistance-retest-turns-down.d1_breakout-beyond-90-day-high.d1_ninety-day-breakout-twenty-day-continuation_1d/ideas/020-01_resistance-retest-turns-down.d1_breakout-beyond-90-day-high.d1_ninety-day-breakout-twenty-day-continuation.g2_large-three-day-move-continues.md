---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high.d1_ninety-day-breakout-twenty-day-continuation
line: 7.g patterns
backtest: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high.d1_ninety-day-breakout-twenty-day-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 3-day return measured against its volatility over 3 days, the more it keeps moving in the same direction over the next 3 days.
Consequence: A trader should follow a coin's unusually large 3-day move for the next few days, more so the larger the move, rather than fade it.
Why:
- F3: Over 2 to 5 days, a coin's volatility-scaled past return predicts the same direction over the same span. The slope is 0.048 at 2 days (t 3.24, 7066 cases), 0.053 at 3 days (t 2.90, 4715 cases) and 0.077 at 5 days (t 3.04, 2699 cases). The largest rises carry most of it: after a 2-day rise above 2 volatility units, the next 2 days earn +1.72 % drift-adjusted (t 2.41, 227 cases). After such a 3-day rise, the next 3 days earn +1.78 % (t 2.32, 173 cases).
