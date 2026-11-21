---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward
line: 7.b inconclusive
backtest: 022-04_signal-weights-carry-forward_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: For a coin's 30-day volatility, the higher that signal's predictive power for the coin's 5-day returns over the past 365 days, the lower the same signal's predictive power for that coin's 5-day returns over the following 90 days.
Consequence: A volatility relation that predicted a coin's returns over the past year is a reason to expect the opposite over the next quarter, not a weight to keep.
Why:
- F1: The tested measure points the opposite way to the idea, not too weakly the right way. The mean of (forecast/10) x 5-day excess return is -0.00228 with t -1.97 on 3,250 non-overlapping cases. Per case the unusual move is -0.48 %, a strength of -0.048, which is the usual 0.05 of a real idea but with the sign reversed. More data on the same idea would not rescue it.
- F2: The reversal comes from two of the four signals.
- F3: The nearness component's correlation with the next 5-day excess return is negative in 6 of 8 years, reaching -0.153 in 2021. The volatility component's is negative in 5 of 8, reaching -0.189 in 2019. In these two signals, past power tends to turn around over the following period rather than carry forward.
- F4: The reversal is broad but uneven, so this data cannot pin it to one place.
