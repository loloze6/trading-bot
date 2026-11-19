---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly
line: 7.g patterns
backtest: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly_1h
instruments: BTC, ETH, BNB
bar: 1h
period: folds A, B, C, D
---
Idea: In a coin whose 20-day volatility is high relative to its 100-day average, a one-day move is partly given back over the next 1 day. The higher that volatility ratio and the larger the day's move relative to its 60-day mean absolute daily move, the larger the opposite move over that day.
Consequence: A fade of a sharp move in a volatile stretch should be sized up with both move size and volatility ratio, and taken off after about a day rather than held for three.
Why:
- F1: The fade of a large one-day move (|24h move / its 60-day mean absolute 24h move| ≥ 1.6) earns more as 20-day volatility rises against its 100-day mean, over the next 24 hours: by volatility ratio below 0.8, 0.8–1.0, 1.0–1.25, 1.25–1.5 and above 1.5, the mean signed excess return is −0.43% (t −1.27, n 156), +0.16% (t 0.63, n 243), +0.15% (t 0.58, n 306), +1.01% (t 2.58, n 149) and +2.21% (t 3.41, n 62), on non-overlapping grids.
- F2: Over the next 24 hours, the fade's signed excess return regressed on |day-move z| × volatility ratio has slope 0.0026 with t 6.78 (n 4592 non-overlapping cases), and on |z| alone, where the ratio is ≥ 1, slope 0.0033 with t 4.69. That makes the reversal graded in both the move size and the volatility level.
- F3: Where the ratio is ≥ 1.25, the 24-hour fade is strongest for the largest moves, +2.29% for |z| > 2.5 (t 4.06, n 95) against +0.28% for |z| ≤ 0.5 (t 1.11, n 244). It holds on both coins, BTC +0.89% (t 2.51, n 115) and ETH +1.92% (t 3.20, n 96), and has a positive mean in every year with cases (2018–2025).
- F4: The tested 72-hour horizon dilutes this. For |z| ≥ 1.6 at a ratio ≥ 1.25, the fade's mean is +0.39% at 72 hours (t 0.45, n 65) against +1.36% at 24 hours (t 4.03, n 211). The book's trades held 24–72 hours lose −3.98% (long, n 890) and −4.34% (short, n 1067) net, while trades under 6 hours gain +0.56% and +0.35%.
