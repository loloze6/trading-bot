---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g1_sunday-move-reverses-monday
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g1_sunday-move-reverses-monday_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin, Sunday's daily return, measured in its 20-day daily standard deviations, is reversed over the next 1 day: the larger Sunday's move, the larger Monday's move against it. The reversal is larger the lower the coin's 60-day return, so after a strong 60-day rise a large up Sunday is barely given back.
Consequence: Lean against Sunday moves into Monday harder when the coin has been falling over the past 60 days, and least when it has risen strongly.
Why:
- F4: The Sunday reversal is lopsided:
- F5: The Sunday reversal fades as the coin's 60-day return rises:
- F6: The worst 5 % of Sundays came on large moves (mean |z| 1.26 against 0.63 for the rest) with large positions (mean |position| 0.84 against 0.39). These losses drive the 0.20 deepest fall that sets the Calmar at 0.061.
