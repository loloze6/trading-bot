---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g2_sunday-fall-rebounds-early-week
line: 7.b inconclusive
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g2_sunday-fall-rebounds-early-week_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's Sunday return (its Saturday-close to Sunday-close return, measured against its own recent daily volatility) is reversed over the next 3 days: the price moves against the Sunday move, and the larger the Sunday move in usual daily moves, the larger the move back.
Consequence: A trader fading Sunday moves should fade both Sunday rises and Sunday falls, sized by the Sunday move, and hold into midweek rather than only through Monday.
Why:
- F1: Across all Sunday bars, the Sunday return in usual daily moves predicts the opposite move: the slope of the excess 2-day return on it is -0.0058 (t -4.39, 4382 cases) and of the 3-day return -0.0092 (t -5.83, 4320 cases), while on all other days pooled it is +0.00003 (t 0.05) at 2 days, and the Sunday-versus-other-days difference in slope is -0.0058 (t -3.99).
- F2: Most of the reversal comes from which way Sunday moved, not from how far Sunday fell. Sunday-fall octiles are followed by excess 2-day returns of +0.56%, +0.93% and +0.85%, and Sunday-rise octiles by -1.33%, -1.33%, -1.20% and -0.67%. Within falls alone the slope on the fall's size is not significant (-0.0024, t -0.80, 2172 cases).
- F4: The two-sided Sunday reversal holds broadly. 17 of 19 coins (89%) have a negative 2-day slope, and 7 of 8 years are negative, with t -3.45 in 2020, -3.23 in 2025 and -2.14 in 2024; only 2022 is positive (+0.0056, t 1.67).
- F5: On the fall side alone, the 2-day slope changes sign from year to year (2018 t -2.08, 2021 t +2.79, 2022 t -1.08) and from coin to coin (TRX t +2.08, BTC t -1.17), and no more data is available, because the test already used every coin and fold listed.
