---
brief: 010_rsi-midline-regime-direction
source-idea: 010-06_rsi-below-share-reversal
line: 7.d not profitable
backtest: 010-06_rsi-below-share-reversal_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: The larger the share of the past 30 days that a coin's 14-day RSI has spent above 50, the higher the coin's return over the next 14 days, while the coin's 60-day return is positive.
Consequence: In a rising 60-day trend, a trader would take a long whose size grows with how persistently RSI has held above its midpoint, instead of fading that strength.
Why:
- F1: The book loses because its sign is wrong rather than because of costs: its gross daily gain is -0.00102 while fees take only about 0.00003 per bar, and the same positions reversed earn a Sharpe of +0.84 against the book's -0.84 and holding's +0.64, positive in 16 of 24 windows, with a leave-one-out Sharpe range of 0.71 to 0.96.
- F2: Most of the loss comes from going short while the coin's 60-day return was positive (the RSI below-share is low then): on those 1308 days the book's mean daily gain was -0.00255 and its timing -0.00157, while long days in falling markets (1141 days) also lost, at a timing of -0.00158.
- F5: When the coin's 60-day return is positive the relation runs the other way, toward continuation: the share slope is -0.109 (t -1.42, n 79) and the forecast slope is -0.0042 (t -1.95, n 78).
