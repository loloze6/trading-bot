---
line: 7.d not profitable
backtest: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling_1d
idea tested: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3423 USD
---
## Findings
- **F1:** The book is in a position on only 5.1% of bars, at a mean absolute size of 0.26 of the book, so its mean daily return is 1.2e-5 against the coin's 0.00128, with a daily standard deviation of 0.0036 against 0.040; the failed mean-return and Sharpe-versus-holding measures come mainly from this near-permanent flatness.
- **F2:** The 299 active short bars sit against the coins' rise: the next-bar coin return on them averages +0.0008 (against +0.00128 on all bars). Gain per active bar is only 0.00048, and 181 trades of 1.74 days win 33% of the time.
- **F3:** The grade does carry information, but only over the next bar. The deepest-decline quartile of new lows has a next-bar return of +0.0103 and a gain of -0.00124. The mildest quartile has -0.0034 and +0.00101, and the Spearman correlation of the 30-day decline with the next-bar return is -0.128. Over 10 bars there is no ordering (deep +0.019, q2 -0.010, q3 -0.026, mild +0.013), and the verdict's 10-bar Welch t is -0.81 on 135 cases.
- **F4:** The losses come where the fall into the low was recent and sharp. The most-down quartile by 10-day return has a next-bar return of +0.0098 and a gain of -0.0015, while the least-down quartile has -0.0029 and +0.0025. The lowest 5-day-return quartile has a next-bar return of +0.0085.
- **F5:** The short pays only while the coin is still near its 100-day average. That quartile has a next-bar return of -0.0057 and a gain of +0.0028 (t 1.67, 56 bars). Far below the average the gain is -0.0015 (t -0.92), and the mild-decline bars near the average (100 bars) gain +0.0012.
- **F6:** Only the first new-low bar pays: 152 cases with a gain of +0.0010. On the second consecutive new-low bar the next-bar return is +0.0087 and the gain is -0.0009. Runs of 5 or more bars rebound +0.059 next bar (5 cases).
- **F7:** The result rests on a few falling windows. w1 (+0.154) and w2 (+0.215) carry the summed book return, while w9 (-0.191) and w22 (-0.090) lose. Eight windows have 0 to 3 active bars, and the lowest Sharpe with one window left out is -0.18.
- **F8:** Across all bars on the non-overlapping 10-bar grid, the 10-bar return rises with closeness to the 30-day high close: 0.005 in the deepest quintile, 0.013 in the middle quintile and 0.023 at the high, with 103 cases each. Strength continues; weakness does not.

## Ideas
- `005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.d1_shallow-lows-near-trend` (from F3, F5, F6, F2): When a coin's close makes a new 30-day low, the smaller its 30-day decline into that low, the further it keeps falling over the next 2 days, only while its close is still near its 100-day average.
- `005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.d2_sharp-drops-rebound-instead` (from F3, F4, F6): When a coin's close makes a new 30-day low, the smaller its 30-day decline into that low, the further it keeps falling over the next 2 days, except when the 10-day fall into it was sharp, after which the sharper that fall, the more it rebounds.
- `005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.d3_near-highs-keep-rising` (from F8, F1, F2, F7): The closer a coin's close is to its 30-day high close, the more it rises over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
