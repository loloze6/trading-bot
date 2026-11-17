---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 1-day rise relative to its own 60-day volatility, the more that coin keeps rising over the next 2 days.
Consequence: A strong day rise in a coin is a reason to hold or add long for two days rather than fade it.
Why:
- F1: Across every weekday, a coin's large day moves, up or down, are followed by a rise. On a non-overlapping 2-day grid, the top fifth of |1-day return / 60-day volatility| is followed by a 2-day excess return of +0.0054 (t 3.64, n 3003), with +0.0053 after falls and +0.0055 after rises; the second-lowest fifth is followed by -0.0044 (t -3.52).
- F3: Larger day rises are followed by a larger 2-day excess return on Monday, Wednesday and Friday. The rise-only slopes are 0.0075 (t 4.33), 0.0079 (t 3.94) and 0.0060 (t 3.93), with about 2,150 cases per weekday at one per coin per week.
