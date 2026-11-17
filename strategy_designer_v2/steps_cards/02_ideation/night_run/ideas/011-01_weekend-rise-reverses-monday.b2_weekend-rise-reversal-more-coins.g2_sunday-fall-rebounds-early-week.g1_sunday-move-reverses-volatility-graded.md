---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g2_sunday-fall-rebounds-early-week
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g2_sunday-fall-rebounds-early-week_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's Sunday return, measured in units of its own 20-day daily volatility, is followed by a move the opposite way over the next 2 days. The reversal is larger the larger the Sunday move, and larger still when the coin's recent volatility is high.
Consequence: A trader can fade both Sunday rises and Sunday falls at Sunday's close, sizing up when the coin is in a high-volatility period, rather than only buying falls.
Why:
- F1: Across all coins, Sunday's return scaled by its 20-day volatility predicts the next 2 days' excess return with a negative slope of -0.0062 (t -4.80, n 4600, one case per week so none overlap). This is the strongest of the seven weekdays: Monday's moves give t -1.55 and Thursday's give +0.86. The same Sunday-scaled return still gives t -2.00 over 5 days.
- F2: The Sunday reversal grows with the coin's volatility level. The slope is -0.0015 (t -0.84, n 1535) in the lowest third of the coin's own volatility, -0.0062 (t -2.98, n 1542) in the middle third and -0.0115 (t -4.10, n 1502) in the highest third.
- F4: The Sunday slope is negative in 7 of 8 years, with 2022 the exception at +0.0047 (t 1.48). It is significant in 2020 (t -3.17), 2024 (t -2.76) and 2025 (t -3.87). It is negative in 17 of 19 coins, most strongly LINK (t -3.00), SUI (-2.45), NEAR (-2.16) and XMR (-2.03).
- F5: The reversal comes from the sign of Sunday's move, not its size within one side. The slope is only +0.0024 (t 0.91, n 2268) among Sunday rises and +0.0009 (t 0.31, n 2302) among Sunday falls. This fits the tested falls-only idea being inconclusive (t 1.12) and the book earning 8.968e-05 a day, Sharpe 0.36.
