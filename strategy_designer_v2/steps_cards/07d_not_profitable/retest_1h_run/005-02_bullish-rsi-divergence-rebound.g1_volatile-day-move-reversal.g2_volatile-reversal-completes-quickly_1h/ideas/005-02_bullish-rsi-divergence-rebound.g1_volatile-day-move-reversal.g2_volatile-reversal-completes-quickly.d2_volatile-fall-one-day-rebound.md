---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly
line: 7.d not profitable
backtest: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly_1h
instruments: BTC, ETH, BNB
bar: 1h
period: folds A, B, C, D
---
Idea: In a coin whose 20-day volatility is high relative to its last 100 days, a large one-day fall is followed by a rise over the next 1 day. The larger the fall relative to its 60-day mean absolute daily move, the larger that rise.
Consequence: A rebound trade after a sharp drop in a volatile stretch earns most of its move within a day, and a position not yet in profit after a day is a reason to close it.
Why:
- F3: On the non-overlapping 72-bar grid, buying after a large fall (|forecast| ≥ 10) beat the coin's mean 72-bar return by +1.31% (t 1.72, 195 cases pooled, 99 of them long), while shorting after a large rise gave +0.16% (t 0.21, 96 cases). Over 24 bars the long side's signed return was +0.55% (t 3.54, n=1158) against −0.05% (t −0.39, n=1303) for the short side.
- F6: Trades that stayed open longer lost heavily. Those held 12–48 hours averaged −1.36% before fees (n=4284) and those over 48 hours −5.69% (n=699), against about +0.5% for trades under 12 hours. A fade that does not turn within a day mostly fails.
- F5: The book churns on weak signals. Bars with |forecast| < 5 took 36% of all fees, for a gross gain near zero: +0.03 on −0.16, +0.18 and +0.08 across the side buckets. The 15,636 trades last a median of 6 hours, far shorter than the 72-hour move the idea bets on.
