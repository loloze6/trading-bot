---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.d1_weekend-moves-reverse-both-ways.g1_high-volatility-daily-move-reversal
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.d1_weekend-moves-reverse-both-ways.g1_high-volatility-daily-move-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's rise over the next 1 day after a down day grows with the size of that day's fall measured in its 20-day volatility, and it is concentrated in the largest falls, where it is several times larger than after small falls.
Consequence: Act only on large volatility-scaled falls, where the rebound clears the trading costs that small moves cannot pay.
Why:
- F2: Up days do not reverse in a way that pays. After the largest third of vol-scaled up days the next-day return minus the coin's mean was only -0.000260, and the net gain was -0.002066 per bar over 1194 cases. After large down days the next day beat the coin mean by 0.008049, with a net gain of 0.005421 over 1075 cases.
- F3: Fees take about half the gross. Active bars earned 0.001260 gross against 0.000605 in fees. Small and mid moves net almost nothing: down-small 0.000005, down-mid 0.000341, up-small -0.000418, up-mid 0.000083.
