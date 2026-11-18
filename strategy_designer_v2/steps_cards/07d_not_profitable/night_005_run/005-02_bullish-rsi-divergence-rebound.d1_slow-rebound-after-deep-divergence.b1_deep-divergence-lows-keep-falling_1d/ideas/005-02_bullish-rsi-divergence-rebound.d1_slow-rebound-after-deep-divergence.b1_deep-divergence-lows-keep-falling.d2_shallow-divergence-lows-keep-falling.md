---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.b1_deep-divergence-lows-keep-falling
line: 7.d not profitable
backtest: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.b1_deep-divergence-lows-keep-falling_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's close makes a new 30-day low while its 14-day RSI is above its reading at the previous low in that window, the price keeps falling over the next 10 days, and the shallower the coin's 30-day decline into that low, the larger the further fall.
Consequence: A divergence low reached after only a mild 30-day slide is a reason to keep a short for days, while one reached after a steep slide is not.
Why:
- F4: The tested grading runs backwards: at divergence lows, the deeper the 30-day decline, the larger the next rise. The 30-day return correlates −0.37 with the 5-day forward return and −0.41 with the 10-day forward return. The deepest third (30-day return −33%, n 14) rose +2.1% over 5 days and +4.4% over 10 days. The mildest third (−8.6%, n 14) fell −3.6% over 5 days and −3.7% over 10 days.
- F2: The short is gone almost as soon as it opens. Short runs last 1.24 bars on average, with a median of 1 and a maximum of 3, because the new-low condition holds only on the bar of the low. The result is 121 trades averaging 1.2 days, winning 31% of the time, with a mean net result of −0.74%. Fees took a further 0.146 of book value on top of a gross loss of −0.255.
- F3: The divergence carries no information. Over 32 spaced events the excess 20-bar return was −0.58% (t −0.16). Recomputed divergence lows (40) against non-divergence new lows (66) differ by Welch t between −1.26 and +0.03 at every horizon from 1 to 20 days.
