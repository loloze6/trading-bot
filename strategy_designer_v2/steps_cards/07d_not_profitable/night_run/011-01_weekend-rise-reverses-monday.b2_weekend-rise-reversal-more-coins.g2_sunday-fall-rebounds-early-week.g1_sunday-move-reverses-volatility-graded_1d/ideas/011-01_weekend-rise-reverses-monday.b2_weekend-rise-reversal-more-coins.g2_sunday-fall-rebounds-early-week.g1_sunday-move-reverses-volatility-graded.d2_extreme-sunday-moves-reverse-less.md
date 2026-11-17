---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g2_sunday-fall-rebounds-early-week.g1_sunday-move-reverses-volatility-graded
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g2_sunday-fall-rebounds-early-week.g1_sunday-move-reverses-volatility-graded_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's Sunday return, measured in units of its own 20-day daily volatility, is followed by a move the opposite way over the next 2 days. The reversal grows with the Sunday move up to moderate sizes, and the most extreme Sunday moves (several times the coin's daily volatility) reverse less and partly continue on Monday.
Consequence: Fading moderate Sunday moves hardest and the most extreme ones lightly would cut the book's deepest Monday losses.
Why:
- F5: The largest Sunday moves reverse less, and they cause the deepest losses, which is what drives the Calmar failure. By |Sunday z|-quartile, the Monday reversal goes 0.0024, 0.0049, 0.0068, then drops to 0.0036 in the top quartile. The worst 5% of Mondays sum to -16.5 against a total of +7.1, and they follow Sunday moves of |z| 1.37 against 0.66 on average.
- F2: The reversal lasts two days, but the book is held for one. The signed reversal is 0.00326 on Monday (t 4.13) and a further 0.00366 on Tuesday alone (t 5.14), then 0.00101 (t 1.22) on Wednesday and -0.00118 on Thursday. Keeping the same position through Tuesday would add 0.00094 per case (t 2.79) with no extra fee.
