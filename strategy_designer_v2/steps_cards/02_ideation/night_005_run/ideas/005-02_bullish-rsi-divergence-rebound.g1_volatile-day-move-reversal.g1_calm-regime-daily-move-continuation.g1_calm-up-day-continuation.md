---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g1_calm-regime-daily-move-continuation
line: 7.g patterns
backtest: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g1_calm-regime-daily-move-continuation_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: In BTC or ETH, when the 20-day volatility is low relative to its last 100 days, a large up day is followed by a further rise over the next 5 days. The larger the day's gain relative to the coin's 60-day mean absolute daily move, and the lower the volatility rank, the larger that rise.
Consequence: In calm stretches, a sharp up day is a reason to buy and hold for about five days, while a sharp down day is no reason to go short.
Why:
- F1: The confirmed edge comes only from up days. In the top |forecast| quintile, the long side has a mean signed excess 5-day return of +0.0225 (t 2.28, n 88), while the short side has +0.0004 (t 0.05, n 83).
- F2: Sorted by signed forecast, only the highest quintile (the largest calm up-days) is followed by a clear excess 5-day return: +0.0156 (t 2.56, n 228). The lowest quintile (the largest calm down-days) shows +0.0031 (t 0.57, n 228), so down moves do not continue. The pattern holds in both coins: top quintile +0.0122 for BTC and +0.0191 for ETH.
- F3: The book loses because of its shorts. Days held long average +0.00072 for both BTC and ETH, while days held short average -0.00047 for BTC and -0.00088 for ETH. Overall the book's mean daily return is -0.000015, of which timing is -0.000044 and the market's own rise is +0.000029.
- F4: After the book's best 5% of days, the coin's next-5-day excess return is +0.0215 (t 3.80, n 282). After its worst 5% of days it is +0.0030 (t 0.59, n 271). This t uses every day's overlapping 5-day return, so it overstates the evidence. Still, it points the same way: the days the book wins (sharp moves it is positioned with) are followed by more of the same rise.
