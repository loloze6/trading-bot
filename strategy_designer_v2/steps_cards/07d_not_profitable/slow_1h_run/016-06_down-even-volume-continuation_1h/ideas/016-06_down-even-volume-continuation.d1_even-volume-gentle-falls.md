---
brief: 016_grind-versus-jump-moves
source-idea: 016-06_down-even-volume-continuation
line: 7.d not profitable
backtest: 016-06_down-even-volume-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has fallen over the past 3 days, the more evenly its hourly volume was spread across those hours, the more the coin keeps falling over the next 3 days, only while that 3-day fall is small next to the coin's usual 3-day swing in its hourly volatility.
Consequence: A trader should press the short only on gentle, evenly traded declines and stand aside from steep 3-day falls, where even volume is followed by a rebound rather than continuation.
Why:
- F3: Among fallen coins, only the shallow falls continue; deep falls do not. On the non-overlapping 72-bar grid, the shallowest raw-fall quintile had a 72-bar excess return of -0.0115 (t -3.81, n 534) and the deepest +0.0060 (t 1.30, n 534). By volatility-scaled fall, the shallowest quintile was -0.0091 (t -2.51) and the deepest +0.0002 (t 0.04).
- F4: Even volume predicts continuation only inside shallow falls. Shallow falls with even volume had an excess of -0.0107 (t -3.65, n 690), while deep falls with even volume had +0.0099 (t 1.79, n 378). This opposite sign in deep falls cancels the pooled evenness slope (t 0.94 over 2762 cases). Among shallow falls, the most even volume tercile had -0.0081 (t -1.99) against -0.0012 (t -0.38) for the most bursty.
- F1: The book loses because it is short in a rising market and pays more in fees than it gains: its allocation averaged -0.073 while the coins rose 0.00119 per day. Its pre-fee gain was -9.7e-7 per bar, against fees of 9.8e-6 per bar. The market's own rise cost it -4.4e-6 per bar, which its timing (+3.5e-6 per bar) did not make up, so the book earned -0.000244 per day.
