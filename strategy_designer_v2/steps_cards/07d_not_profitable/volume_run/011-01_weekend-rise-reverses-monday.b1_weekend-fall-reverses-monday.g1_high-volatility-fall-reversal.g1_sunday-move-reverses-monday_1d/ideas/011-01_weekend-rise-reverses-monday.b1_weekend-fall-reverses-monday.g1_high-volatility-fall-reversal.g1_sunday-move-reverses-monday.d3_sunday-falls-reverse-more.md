---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g1_sunday-move-reverses-monday
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g1_sunday-move-reverses-monday_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin, Sunday's daily return, measured in its 20-day daily standard deviations, is reversed over the next 1 day: the larger Sunday's move, the larger Monday's move against it. A Sunday fall is reversed more strongly than a Sunday rise of the same size.
Consequence: After a large Sunday drop, buy into Monday in proportion to the drop, and lean only lightly against Sunday rallies.
Why:
- F4: The Sunday reversal is lopsided:
- F6: The worst 5 % of Sundays came on large moves (mean |z| 1.26 against 0.63 for the rest) with large positions (mean |position| 0.84 against 0.39). These losses drive the 0.20 deepest fall that sets the Calmar at 0.061.
