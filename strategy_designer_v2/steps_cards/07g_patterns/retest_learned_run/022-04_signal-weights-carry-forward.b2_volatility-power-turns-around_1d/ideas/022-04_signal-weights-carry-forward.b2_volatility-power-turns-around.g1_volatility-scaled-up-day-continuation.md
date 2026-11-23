---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around
line: 7.g patterns
backtest: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 1-day rise measured against its own 20-day volatility, the higher its return over the next 5 days, relative to its usual 5-day drift.
Consequence: A coin that closes a day with an unusually large rise for its recent volatility is a reason to hold it long for the following 5 days, and a small or negative such move is a reason to refuse that long.
Why:
- F2: A coin's 1-day return divided by its 20-day volatility, read at the close, predicts the next 5 days. The top quintile is followed by a 5-day excess return of +1.56 % (t 2.86, 510 non-overlapping cases), about 0.15 of the coin's usual 5-day move (10.60 %) and about 8 times the 0.19 % cost of a trade; the other four quintiles lie between -0.73 % and +0.02 %.
- F3: The F2 effect is graded and fairly broad. Among positive readings only, the Spearman correlation of the standardised 1-day rise with the next 5-day excess return is +0.065 (1231 cases, t about 2.3). The top quintile's mean is positive in 5 of 6 coins (BTC +1.52 %, ETH +0.96 %, XMR +0.53 %, XRP +3.00 %, ZEC +3.60 %; LTC -0.31 %) and in 7 of 8 years (2022 -1.13 %).
- F4: The raw 1-day return without volatility scaling shows no clean grading. Its quintile means are +0.69 %, -1.47 %, -0.10 %, -0.45 %, +0.99 %, and its per-coin rank correlations run from -0.067 to +0.018. Only scaling by the coin's recent volatility orders the effect into one tail.
