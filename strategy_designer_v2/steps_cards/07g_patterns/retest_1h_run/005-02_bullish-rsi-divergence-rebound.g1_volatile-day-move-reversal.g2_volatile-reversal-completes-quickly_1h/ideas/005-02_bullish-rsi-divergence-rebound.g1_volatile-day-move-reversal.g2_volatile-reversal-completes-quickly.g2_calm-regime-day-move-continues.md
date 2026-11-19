---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly
line: 7.g patterns
backtest: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly_1h
instruments: BTC, ETH, BNB
bar: 1h
period: folds A, B, C, D
---
Idea: In a coin whose 20-day volatility is low relative to its 100-day average, a large one-day move keeps going over the next 2 days. The lower that volatility ratio and the larger the day's move relative to its 60-day mean absolute daily move, the larger the continuation in the same direction.
Consequence: In calm stretches a trader should refuse to fade a sharp day and lean with it instead.
Why:
- F5: In calm stretches (ratio below 0.8) large one-day moves continue instead of reverting. The fade's mean is −0.23% at 6 hours (t −2.60, n 631), −0.30% at 12 hours (t −1.74, n 320) and −1.56% at 48 hours (t −2.63, n 78).
- F1: The fade of a large one-day move (|24h move / its 60-day mean absolute 24h move| ≥ 1.6) earns more as 20-day volatility rises against its 100-day mean, over the next 24 hours: by volatility ratio below 0.8, 0.8–1.0, 1.0–1.25, 1.25–1.5 and above 1.5, the mean signed excess return is −0.43% (t −1.27, n 156), +0.16% (t 0.63, n 243), +0.15% (t 0.58, n 306), +1.01% (t 2.58, n 149) and +2.21% (t 3.41, n 62), on non-overlapping grids.
