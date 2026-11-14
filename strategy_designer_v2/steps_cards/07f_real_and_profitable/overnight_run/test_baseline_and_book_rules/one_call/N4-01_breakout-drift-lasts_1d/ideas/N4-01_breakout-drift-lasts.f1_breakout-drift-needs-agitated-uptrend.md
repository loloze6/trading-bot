---
brief: 002_moving-average-cross-trend-persistence
source-idea: N4-01_breakout-drift-lasts
line: 7.f real and profitable
backtest: N4-01_breakout-drift-lasts_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In one coin, a close at a new 20-day closing high, at a time when the coin's prior 20 days have risen and its 20-day daily volatility is in the middle or upper third of its own range, is followed by a rise over the next ten days larger than the coin's average ten-day move.
Consequence: A trader would take new-high longs only when the coin is already rising with lively volatility, and refuse them in calm or falling markets where the drift has not paid.
Why:
- F3: The book earns only in rising and agitated markets: days with a positive prior 20-day coin move and mid or high volatility carry 43% (mean 0.0041, t 1.73, n 449) and 56% (mean 0.0058, t 2.04, n 412) of the book's sum, while rising calm days (-0.0002, n 499) and all falling-market states (means -0.0003 to 0.0008, |t| < 0.6) earn nothing.
- F4: The effect turns with the year: event excess returns are positive in 2020 (0.046, t 2.62, n 80), 2021 (0.078, t 2.36, n 60) and 2024 (0.057, t 2.29, n 63), and negative in 2018 (-0.050, t -1.64, n 28), 2022 (-0.028, t -1.95, n 55) and 2023 (-0.017, t -1.74, n 66); the book's Sharpe was -1.64 in 2018 and -0.78 in 2022.
- F5: Much of the book is market exposure: regressed on the coins' mean daily return, it has beta 0.79 and a daily alpha of 0.00077 with t 1.61 over 2898 days; across the 24 windows, window means of book and holding move together.
