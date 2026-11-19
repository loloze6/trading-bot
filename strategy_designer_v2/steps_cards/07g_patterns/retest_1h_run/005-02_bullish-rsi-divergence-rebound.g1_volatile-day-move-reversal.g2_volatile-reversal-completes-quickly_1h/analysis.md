---
line: 7.g patterns
backtest: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly_1h
idea tested: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4033 USD
---
## Findings
- **F1:** The fade of a large one-day move (|24h move / its 60-day mean absolute 24h move| ≥ 1.6) earns more as 20-day volatility rises against its 100-day mean, over the next 24 hours: by volatility ratio below 0.8, 0.8–1.0, 1.0–1.25, 1.25–1.5 and above 1.5, the mean signed excess return is −0.43% (t −1.27, n 156), +0.16% (t 0.63, n 243), +0.15% (t 0.58, n 306), +1.01% (t 2.58, n 149) and +2.21% (t 3.41, n 62), on non-overlapping grids.
- **F2:** Over the next 24 hours, the fade's signed excess return regressed on |day-move z| × volatility ratio has slope 0.0026 with t 6.78 (n 4592 non-overlapping cases), and on |z| alone, where the ratio is ≥ 1, slope 0.0033 with t 4.69. That makes the reversal graded in both the move size and the volatility level.
- **F3:** Where the ratio is ≥ 1.25, the 24-hour fade is strongest for the largest moves, +2.29% for |z| > 2.5 (t 4.06, n 95) against +0.28% for |z| ≤ 0.5 (t 1.11, n 244). It holds on both coins, BTC +0.89% (t 2.51, n 115) and ETH +1.92% (t 3.20, n 96), and has a positive mean in every year with cases (2018–2025).
- **F4:** The tested 72-hour horizon dilutes this. For |z| ≥ 1.6 at a ratio ≥ 1.25, the fade's mean is +0.39% at 72 hours (t 0.45, n 65) against +1.36% at 24 hours (t 4.03, n 211). The book's trades held 24–72 hours lose −3.98% (long, n 890) and −4.34% (short, n 1067) net, while trades under 6 hours gain +0.56% and +0.35%.
- **F5:** In calm stretches (ratio below 0.8) large one-day moves continue instead of reverting. The fade's mean is −0.23% at 6 hours (t −2.60, n 631), −0.30% at 12 hours (t −1.74, n 320) and −1.56% at 48 hours (t −2.63, n 78).
- **F6:** The book lost money on both coins, with mean daily returns of −0.060% (BTC) and −0.062% (ETH), while holding the coins gave +0.118% and +0.137%. Its gain from the market's own rise is −0.009 bp per bar on each coin, so it was net short a rising market and carried no timing gain large enough to offset that.
- **F7:** Hourly returns over 21:00–23:00 UTC average +4.3 bp (BTC, t 4.45) and +5.6 bp (ETH, t 4.56) per hour, against roughly 0 to 2 bp elsewhere. The effect is positive in 7 of 8 years and on every weekday (t 1.9–3.1), but it is a calendar condition with no graded strength.

## Ideas
- `005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly.g1_volatile-one-day-move-reverts` (from F1, F2, F3, F4): In a coin whose 20-day volatility is high relative to its 100-day average, a one-day move is partly given back over the next 1 day. The higher that volatility ratio and the larger the day's move relative to its 60-day mean absolute daily move, the larger the opposite move over that day.
- `005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly.g2_calm-regime-day-move-continues` (from F5, F1): In a coin whose 20-day volatility is low relative to its 100-day average, a large one-day move keeps going over the next 2 days. The lower that volatility ratio and the larger the day's move relative to its 60-day mean absolute daily move, the larger the continuation in the same direction.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
