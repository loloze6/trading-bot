---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal
line: 7.g patterns
backtest: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 20-day volatility is low relative to its 60-day average, its return over the next 3 days follows the direction of the day just closed. The larger that day's return relative to its 20-day volatility, the larger the move that follows.
Consequence: In calm spells, a trader follows a large daily move for three days and refuses to fade it.
Why:
- F4: In the calmest quarter of the volatility ratio the sign turns: the day's z predicts continuation over the next 3 days (slope +0.0105, t 3.08, n 319, non-overlapping), and on low-volatility bars the slope is +0.0042 (t 2.14, n 998), positive for both coins (ETH t 2.12, BTC t 1.09).
- F5: The book's gain is all timing and no market: timing is 0.000687 per bar against a market part of -0.000017, while the book is flat on 43% of bars and earns a mean daily 0.000384 against the coins' 0.001275. Holding the coins beats it because it gives up their rise, not because the reversal is absent.
