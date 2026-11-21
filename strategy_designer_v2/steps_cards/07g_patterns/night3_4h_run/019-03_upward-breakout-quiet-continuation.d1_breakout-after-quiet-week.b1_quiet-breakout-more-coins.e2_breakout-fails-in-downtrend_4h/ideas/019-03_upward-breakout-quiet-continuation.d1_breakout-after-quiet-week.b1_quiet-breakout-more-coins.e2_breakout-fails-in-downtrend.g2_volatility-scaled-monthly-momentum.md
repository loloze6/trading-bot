---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins.e2_breakout-fails-in-downtrend
line: 7.g patterns
backtest: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins.e2_breakout-fails-in-downtrend_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: A coin's return over the next 24 days rises with its 30-day return divided by its 30-day volatility: the stronger its recent risk-adjusted rise, the more it gains over the following weeks.
Consequence: A trader should hold a coin long in proportion to the strength of its volatility-scaled monthly rise, and refuse longs in coins whose month has been weak.
Why:
- F6: On the 12-day grid, the coin's next 12 days rise with its volatility-scaled 30-day return (Spearman 0.058, p 0.009, about 2070 cases).
- F1: The confirmed decline after an upward breakout in a falling coin is not about the upward breakout. Downward breakouts in a falling coin are followed by nearly the same unusual 12-day move: -2.36 % (t -5.29, 1397 cases) against -2.67 % (t -5.04, 1122 cases) for upward ones. The negative 30-day return carries the effect, not the break of the two-day range.
- F3: The book is mainly a bet on the market falling. Its mean daily return is positive in 2018, 2022 and 2025, the years the coins fell (coin daily mean -0.35 %, -0.26 % and -0.03 %). It is negative in 2020, 2023 and 2024, the years they rose (book -0.10 %, -0.11 % and -0.10 %). Trades lose on average in every year except 2025: mean net from -1.2 % to -13.2 %, against +3.6 % in 2025.
