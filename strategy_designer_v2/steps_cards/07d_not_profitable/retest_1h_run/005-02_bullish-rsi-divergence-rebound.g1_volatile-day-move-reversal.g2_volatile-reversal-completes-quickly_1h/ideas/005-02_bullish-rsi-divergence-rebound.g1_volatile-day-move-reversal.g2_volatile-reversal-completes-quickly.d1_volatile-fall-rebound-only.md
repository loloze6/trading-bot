---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly
line: 7.d not profitable
backtest: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly_1h
instruments: BTC, ETH, BNB
bar: 1h
period: folds A, B, C, D
---
Idea: In a coin whose 20-day volatility is high relative to its last 100 days, the give-back after a large one-day fall happens within the next 3 days, only for falls and not for rises. The larger the day's fall relative to its 60-day mean absolute daily move, the larger the rise over those 3 days.
Consequence: A trader should buy sharp one-day drops in a volatile stretch and hold for days, but should refuse to short sharp one-day rises, which give nothing back.
Why:
- F2: The book's gain comes only from its long side, the fade of large one-day falls. Long bars earned +1.58 gross against −0.70 for short bars, and at |forecast| 10–20 longs earned +1.23 while shorts lost −0.50.
- F3: On the non-overlapping 72-bar grid, buying after a large fall (|forecast| ≥ 10) beat the coin's mean 72-bar return by +1.31% (t 1.72, 195 cases pooled, 99 of them long), while shorting after a large rise gave +0.16% (t 0.21, 96 cases). Over 24 bars the long side's signed return was +0.55% (t 3.54, n=1158) against −0.05% (t −0.39, n=1303) for the short side.
- F4: The rebound after a fall is graded. On the 72-bar grid, long cases with |forecast| ≥ 10 beat the mean by +1.31%, against +0.24% (t 0.55, n=288) for smaller ones; on the short side neither group differs from zero (−0.01% and +0.16%).
- F1: Fees, not the forecast's direction, sink the book: over BTC and ETH the positions earned 0.88 before costs but paid 4.45 in fees, about 0.00075–0.00079 per day per coin against 0.00010–0.00020 gross, leaving a mean daily return of about −0.0006 (Sharpe −0.72).
