---
brief: 010_rsi-midline-regime-direction
source-idea: 010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week
line: 7.g patterns
backtest: 010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week_1h
instruments: BTC, ETH, BNB
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's recent 7-day volatility is high, the larger its 1-day return relative to that volatility, the more its return over the next 1 day runs the other way.
Consequence: In high-volatility stretches, a trader would fade the past day's move in proportion to its size, and would refuse to chase a large 1-day move.
Why:
- F2: Over 1 day, a coin's move tends to reverse, and the effect sits in high volatility. Its volatility-scaled 24-hour return against the next 24 hours' excess return has a correlation of -0.031 (t -2.34, 5,744 non-overlapping cases). The top past-24h quintile is followed by -0.0021 and the bottom by +0.0022. In the highest tercile of 7-day volatility the correlation is -0.102 (n 1,915, t ≈ -4.5). In the lowest tercile it is +0.052.
- F5: Calendar effects are weak once you allow for the many angles checked. Daily coin returns are highest on Wednesday (+0.0037, t 2.47, n 826) and lowest on Thursday (-0.0026, t -1.61), and the book's gain before costs shows no clear hour pattern.
