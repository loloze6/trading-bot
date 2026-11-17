---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g1_sunday-move-reverses-monday
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g1_sunday-move-reverses-monday_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin, Sunday's daily return, measured in its 20-day daily standard deviations, is reversed over the next 1 day: the larger Sunday's move, the larger Monday's move against it. The reversal is larger the higher the coin's 20-day daily volatility.
Consequence: Lean against Sunday moves into Monday harder when the coin's recent volatility is high.
Why:
- F7: The Sunday reversal grows with the coin's 20-day volatility:
- F2: Fees cost 0.000898 per Sunday, about 70 % of the Sunday gain before fees of 0.00129, so the one-day-a-week round trip eats most of the edge.
