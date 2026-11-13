---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-03_deep-month-loss-rebound
line: 7.d not profitable
backtest: N2-03_deep-month-loss-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin trades below its 100-day average and its 20-day decline keeps deepening, the decline continues and a long position held there loses. The rebound is concentrated in short bounces that resolve within a few days.
Consequence: Cap how long a rebound long is held while the coin remains below its long average, and exit if the fall extends instead of riding it.
Why:
- F2: Long holds make the loss. Trades held over 15 days (743) average -6.38% gross, while trades closed within 1.5 days (707) earn +2.30% and those of 1.5–3.5 days (693) earn +1.66%. The long holds lost most in 2018 (-24.0%, 145 trades) and 2022 (-14.7%, 137 trades).
- F3: The book is a long bet on falling coins. 75% of bars sit below the 100-day average, where the mean allocation is 0.52, against 0.08 above it. In 2018 the coins fell (mean daily return -0.35%) while the allocation averaged 0.60, and the book's summed daily return was -6.40, its only losing year.
- F7: The largest entry forecasts lose. Trades entered at forecasts of 15–21 average -1.42% gross (1337 trades), while those entered at 8–15 earn +0.85% (792 trades).
