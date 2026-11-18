---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling
line: 7.d not profitable
backtest: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's close makes a new 30-day low, the smaller its 30-day decline into that low, the further it keeps falling over the next 2 days, only while its close is still near its 100-day average.
Consequence: A shallow new low taken while the coin still sits near its 100-day average is a reason to short for a day or two, and a new low far below that average is a reason to refuse the short.
Why:
- F3: The grade does carry information, but only over the next bar. The deepest-decline quartile of new lows has a next-bar return of +0.0103 and a gain of -0.00124. The mildest quartile has -0.0034 and +0.00101, and the Spearman correlation of the 30-day decline with the next-bar return is -0.128. Over 10 bars there is no ordering (deep +0.019, q2 -0.010, q3 -0.026, mild +0.013), and the verdict's 10-bar Welch t is -0.81 on 135 cases.
- F5: The short pays only while the coin is still near its 100-day average. That quartile has a next-bar return of -0.0057 and a gain of +0.0028 (t 1.67, 56 bars). Far below the average the gain is -0.0015 (t -0.92), and the mild-decline bars near the average (100 bars) gain +0.0012.
- F6: Only the first new-low bar pays: 152 cases with a gain of +0.0010. On the second consecutive new-low bar the next-bar return is +0.0087 and the gain is -0.0009. Runs of 5 or more bars rebound +0.059 next bar (5 cases).
- F2: The 299 active short bars sit against the coins' rise: the next-bar coin return on them averages +0.0008 (against +0.00128 on all bars). Gain per active bar is only 0.00048, and 181 trades of 1.74 days win 33% of the time.
