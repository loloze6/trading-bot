---
brief: 010_rsi-midline-regime-direction
source-idea: 010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week
line: 7.g patterns
backtest: 010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's daily volatility is high, the larger its one-day return measured in units of its own 20-day daily volatility, the more its return over the next 1 day runs in the opposite direction.
Consequence: In volatile stretches a trader would refuse to chase a large daily move and would lean against it for the following day, more so the larger the move.
Why:
- F1: The day after a coin's daily move, its next-day return runs against that move, with a regression slope t of −3.62 in BTCUSD and −3.98 in ETHUSD (2,873 daily cases each); the lowest prior-day quintile is followed by +0.44% and the highest by −0.06% to −0.14% (Welch t 2.27 and 1.91).
- F2: This next-day reversal is concentrated in the highest 20-day-volatility tercile, with a slope of −0.0070 per standardised prior move (t −5.82, n 1,612); the middle tercile shows none (t −0.06) and the lowest tercile leans to slight continuation (+0.0015, t 2.15).
- F3: The reversal slope is negative in every year from 2018 to 2025, and is strongest in 2020 (t −5.19, n 720) and 2021 (t −2.13).
