---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal
line: 7.g patterns
backtest: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 20-day volatility is high relative to its 60-day average, its return over the next 3 days runs against the day just closed. The larger that day's return relative to its 20-day volatility, and the higher the volatility ratio, the larger the move back.
Consequence: In a volatile spell, a trader leans against a large daily move for about three days instead of one, and leans harder as the volatility ratio climbs.
Why:
- F1: The one-day give-back sits only in the top quarter of the 20-day/60-day volatility ratio: the slope of next-day excess return on the scaled move z is -0.00554 (t -4.34, n 983) there, against +0.00042 (t 0.34), +0.00069 (t 0.59) and -0.00074 (t -0.61) in quartiles 1 to 3 (about 980 bars each), and both coins agree in that top quartile (BTC t -2.61, n 544; ETH t -3.54, n 439).
- F2: In the top volatility-ratio quartile the give-back lasts beyond one day: on non-overlapping 3-day samples, the slope of the 3-day excess return on the day's z is -0.0133 (t -3.91, n 324), more than twice the one-day slope; on all high-volatility bars it is -0.0068 (t -2.57, n 573).
