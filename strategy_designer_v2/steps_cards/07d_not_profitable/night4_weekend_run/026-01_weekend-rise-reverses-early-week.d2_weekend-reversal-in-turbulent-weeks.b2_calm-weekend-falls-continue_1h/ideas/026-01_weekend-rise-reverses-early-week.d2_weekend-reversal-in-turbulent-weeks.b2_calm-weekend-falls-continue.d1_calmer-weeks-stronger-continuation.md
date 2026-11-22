---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks.b2_calm-weekend-falls-continue
line: 7.d not profitable
backtest: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks.b2_calm-weekend-falls-continue_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's price falls from Saturday 00:00 UTC to Monday 00:00 UTC while the coin's 30-day hourly volatility is low against its own last 6 months, it keeps falling over the next two days (Monday and Tuesday), the more so the calmer the coin's 30-day volatility is against its last 6 months.
Consequence: A trader would size a calm-week weekend-fall short by how calm the coin is, and refuse it as volatility nears its 6-month middle.
Why:
- F5: Across all weekend falls the continuation grows with how calm the coin's 30-day volatility is, step by step from the calmest to the most turbulent quartile of its rank: +0.78 % (t 1.51), +0.29 %, +0.10 %, then -0.79 % (t -1.64), with about 226 cases per quartile.
- F4: The continuation depends on the year: the move per signal is +1.5 % to +2.3 % in 2018, 2019 and 2021, and negative in 2020 (-0.75 %, t -1.75), 2024 (-0.46 %) and 2025 (-0.83 %, t -1.36); the book's gain per signal is largest in 2019 (+0.79 %), which explains why one window left out turns the lowest Sharpe to -0.28.
- F1: The book captures little of the move it is betting on: across the 593 Monday signal bars the coin's 48-hour move in the short direction averages +0.78 % (t 2.88), but the book's 48-hour gain per signal is only +0.12 %, because the position held averages -0.41 of the book (and -0.32 on the 11 % of bars where it holds any position).
