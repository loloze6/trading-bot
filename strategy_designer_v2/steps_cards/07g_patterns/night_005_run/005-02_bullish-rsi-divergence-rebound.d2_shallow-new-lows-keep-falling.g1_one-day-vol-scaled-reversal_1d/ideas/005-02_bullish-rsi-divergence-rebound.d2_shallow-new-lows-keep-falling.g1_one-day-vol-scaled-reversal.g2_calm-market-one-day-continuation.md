---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal
line: 7.g patterns
backtest: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 20-day daily volatility is low against its own past year, its vol-scaled 1-day return carries into the next 1 day: the larger the day's rise in units of 20-day volatility, the more it rises the next day, and the larger the fall, the more it falls.
Consequence: In calm periods a trader should refuse to fade sharp daily moves, and should follow them for one day instead.
Why:
- F1: The next-day reversal after a vol-scaled daily move holds only when volatility is high: in the top tercile of each coin's 20-day volatility, the slope of next-day excess return on the day's vol-scaled return is -0.0055 (t -5.74, n 1757). The middle tercile shows nothing (slope -0.0004, t -0.49), and the bottom tercile turns positive, i.e. continuation (slope +0.0018, t +2.94, n 1755).
- F2: The pattern is graded and fits one model: regressing next-day excess return on z, the coin's volatility rank and their product gives z +0.0045 (t 4.85) and z×vol-rank -0.0118 (t -7.41), so the reversal strengthens steadily as volatility rises and flips to continuation at low volatility.
- F5: In the low-volatility tercile the bottom z quintile is followed by -0.0030 (t -1.62) and the top quintile by +0.0034 (t +1.96), with positive slopes in both coins (BTC t 2.22, ETH t 2.01), so the low-volatility side is weaker but has the same sign throughout.
- F6: The book's mixed use of regimes costs it money: its pre-fee position gain per bar is -0.0011 in the low-volatility tercile against +0.0016 in the high tercile. Overall the pre-fee gain is 0.00023 per bar against fees of 0.00036 per bar, at a mean turnover of 0.44 of the book per bar. This explains the negative Sharpe of -0.19 despite the confirmed forecast (t 2.28).
