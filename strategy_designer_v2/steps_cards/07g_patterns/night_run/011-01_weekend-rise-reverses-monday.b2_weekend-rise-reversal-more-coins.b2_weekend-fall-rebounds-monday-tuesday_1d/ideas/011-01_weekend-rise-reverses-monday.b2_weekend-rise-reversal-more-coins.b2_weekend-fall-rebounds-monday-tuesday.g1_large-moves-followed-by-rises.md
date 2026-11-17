---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 1-day move relative to its own 60-day volatility, in either direction, the more that coin rises over the next 2 days.
Consequence: A coin's unusually large day move, up or down, is a reason to lean long for the next two days, more so the larger the move.
Why:
- F1: Across every weekday, a coin's large day moves, up or down, are followed by a rise. On a non-overlapping 2-day grid, the top fifth of |1-day return / 60-day volatility| is followed by a 2-day excess return of +0.0054 (t 3.64, n 3003), with +0.0053 after falls and +0.0055 after rises; the second-lowest fifth is followed by -0.0044 (t -3.52).
- F2: This rise after large moves belongs to each coin, not to the market's day. Comparing coins on the same date, the 2-day excess return regressed on |z| has slope 0.00266 (t 2.86, n 15013), while across whole dates the slope is only 0.00386 (t 1.25, n 1240); the slope is positive in 5 of 8 years (t 2.3 to 3.5 in 2019, 2020, 2021, 2023, 2024).
- F4: Larger day falls are followed by a larger 2-day rebound on weekdays but not on Sunday. The fall-only slopes are -0.0093 (t -4.54) on Monday, -0.0112 (t -2.78) on Wednesday and -0.0078 (t -4.04) on Thursday, against -0.00025 (t -0.09) on Sunday.
