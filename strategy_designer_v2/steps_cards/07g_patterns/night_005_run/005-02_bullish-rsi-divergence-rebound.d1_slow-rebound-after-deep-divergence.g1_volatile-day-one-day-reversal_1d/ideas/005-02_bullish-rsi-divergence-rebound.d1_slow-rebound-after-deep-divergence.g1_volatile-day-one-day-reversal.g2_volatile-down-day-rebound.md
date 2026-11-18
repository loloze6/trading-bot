---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal
line: 7.g patterns
backtest: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 20-day volatility is high relative to its 60-day average, a down day is followed by a rise over the next 1 day. The larger the day's fall relative to its 20-day volatility, the larger the rebound.
Consequence: After a sharp drop in a volatile spell, a trader buys the next day's rebound in proportion to the drop and refuses to sell into it.
Why:
- F3: The give-back in volatile spells is mostly a rebound after down days: in the top volatility-ratio quartile, down days have a slope of -0.00936 (t -3.21, n 480) against -0.00139 (t -0.62, n 503) for up days, and days with z below -1 are followed by a mean next-day excess return of +1.64% (t 3.12, n 123), against -0.45% to +0.23% after such days in the other quartiles.
- F1: The one-day give-back sits only in the top quarter of the 20-day/60-day volatility ratio: the slope of next-day excess return on the scaled move z is -0.00554 (t -4.34, n 983) there, against +0.00042 (t 0.34), +0.00069 (t 0.59) and -0.00074 (t -0.61) in quartiles 1 to 3 (about 980 bars each), and both coins agree in that top quartile (BTC t -2.61, n 544; ETH t -3.54, n 439).
