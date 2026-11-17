---
brief: 010_rsi-midline-regime-direction
source-idea: 010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week
line: 7.g patterns
backtest: 010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's own 20-day daily volatility, the more strongly its return over the next 1 day runs opposite to its return over the past 1 day.
Consequence: A trader would let a coin's recent volatility set how hard to fade its last day's move, fading it most when volatility is highest.
Why:
- F2: This next-day reversal is concentrated in the highest 20-day-volatility tercile, with a slope of −0.0070 per standardised prior move (t −5.82, n 1,612); the middle tercile shows none (t −0.06) and the lowest tercile leans to slight continuation (+0.0015, t 2.15).
- F1: The day after a coin's daily move, its next-day return runs against that move, with a regression slope t of −3.62 in BTCUSD and −3.98 in ETHUSD (2,873 daily cases each); the lowest prior-day quintile is followed by +0.44% and the highest by −0.06% to −0.14% (Welch t 2.27 and 1.91).
