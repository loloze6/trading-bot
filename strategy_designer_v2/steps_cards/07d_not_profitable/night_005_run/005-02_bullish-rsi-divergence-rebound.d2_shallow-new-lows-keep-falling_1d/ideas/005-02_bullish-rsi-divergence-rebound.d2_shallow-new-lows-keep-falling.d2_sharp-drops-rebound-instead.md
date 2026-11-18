---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling
line: 7.d not profitable
backtest: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's close makes a new 30-day low, the smaller its 30-day decline into that low, the further it keeps falling over the next 2 days, except when the 10-day fall into it was sharp, after which the sharper that fall, the more it rebounds.
Consequence: A new low reached by a sudden 10-day drop is a reason to stand aside or buy for a bounce, not to short.
Why:
- F3: The grade does carry information, but only over the next bar. The deepest-decline quartile of new lows has a next-bar return of +0.0103 and a gain of -0.00124. The mildest quartile has -0.0034 and +0.00101, and the Spearman correlation of the 30-day decline with the next-bar return is -0.128. Over 10 bars there is no ordering (deep +0.019, q2 -0.010, q3 -0.026, mild +0.013), and the verdict's 10-bar Welch t is -0.81 on 135 cases.
- F4: The losses come where the fall into the low was recent and sharp. The most-down quartile by 10-day return has a next-bar return of +0.0098 and a gain of -0.0015, while the least-down quartile has -0.0029 and +0.0025. The lowest 5-day-return quartile has a next-bar return of +0.0085.
- F6: Only the first new-low bar pays: 152 cases with a gain of +0.0010. On the second consecutive new-low bar the next-bar return is +0.0087 and the gain is -0.0009. Runs of 5 or more bars rebound +0.059 next bar (5 cases).
