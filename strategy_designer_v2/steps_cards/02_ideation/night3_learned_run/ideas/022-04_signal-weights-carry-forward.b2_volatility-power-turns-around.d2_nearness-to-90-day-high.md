---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around
line: 7.d not profitable
backtest: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The closer a coin's daily close sits to its highest close of the past 90 days, the higher its return over the next 5 days.
Consequence: A coin trading near its 90-day high is a reason to be long for the next week, and one far below it a reason to refuse a long.
Why:
- F2: The idea is real but far too small to pay: per case over 5 days the unusual move is +0.12 % (strength 0.004, against about 0.05 for confirmed ideas so far), and the total move is +0.07 %. A round trip costs 0.19 %, so the moves are 0.6 and 0.4 times the cost.
- F6: Nearness to the 90-day high separates the 5-day timing gain by more than the cost of a trade:
