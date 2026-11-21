---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-01_learned-combined-signal-score.b1_rebound-after-large-daily-falls
line: 7.g patterns
backtest: 022-01_learned-combined-signal-score.b1_rebound-after-large-daily-falls_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 1-day fall compared with its 30-day volatility, the higher its return over the next 1 day, and the more so the higher its 30-day volatility stands against its own 180-day volatility.
Consequence: A trader would buy a coin after a large daily fall mainly when its recent volatility has risen above its longer-run level, and refuse falls in calm periods whose rebound does not cover a trade.
Why:
- F1: The rebound after a daily fall depends on how high volatility is at the time. On next-day excess returns after falls (7,151 bars with a negative 30-day-scaled return), the fall × (30-day volatility / 180-day volatility) interaction has a slope of +208 bps with t 4.4, while the fall's own slope turns negative (-163 bps, t -3.5). After falls larger than one usual move, split into quartiles of that volatility ratio, the next day's excess return is -12, +50, +13 and +160 bps (t 4.12, n 265 in the top quartile).
- F2: The gain sits where volatility is high. Falls in the top quartile of the volatility ratio have a strength of 0.34 of a usual daily move, against -0.03 to 0.09 in the other quartiles. Split by the volatility's rank over the past 180 days instead, the next-day excess is +112 bps (t 3.19, n 168) in high volatility and -1 bps (t -0.05, n 326) in low volatility. The cost of a round trip is 19 bps, so +160 bps is about 8 times it.
- F3: The high-volatility rebound does not hold in every year or coin. It is positive in 2018, 2020, 2023 and 2025 (+70 to +207 bps; t 3.59 only in 2023) but negative or flat in 2019 (-99 bps, n 8) and 2024 (+13 bps). It is strongest on ZEC (+190 bps, t 2.64) and ETH (+247 bps, t 1.76), while XMR's rebound comes from normal-volatility falls (+118 bps, t 2.79).
- F4: The rebound fades with the horizon. On non-overlapping grids, the excess return per usual move of fall is +41 bps over 1 day (t 4.7, n 7,151), +48 over 2 days (t 2.8), +58 over 3 days (t 2.2) and +19 over 5 days (t 0.5). Most of the reversal is in the first day.
- F7: The book holds its bets longer than one day and loses on the average trade. It made 5,950 trades of mean length 2.1 days (median 1), with a mean net result of -0.45 % per trade and 49.5 % winners. Its 2 % worst days follow a prior-day coin fall of -600 bps and coincide with a further -855 bps fall. Its 2 % best days also follow a prior fall (-732 bps), with a +922 bps rebound. The book's outcome is decided by whether a large fall continues or reverses.
