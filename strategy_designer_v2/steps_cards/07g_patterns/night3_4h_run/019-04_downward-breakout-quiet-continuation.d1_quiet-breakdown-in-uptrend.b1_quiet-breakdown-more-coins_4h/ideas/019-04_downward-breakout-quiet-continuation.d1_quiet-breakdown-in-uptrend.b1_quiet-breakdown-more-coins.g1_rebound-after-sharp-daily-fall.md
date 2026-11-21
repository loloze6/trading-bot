---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b1_quiet-breakdown-more-coins
line: 7.g patterns
backtest: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b1_quiet-breakdown-more-coins_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: After a coin's 1-day return is a large fall compared with its 30-day volatility, the coin rises more than usual over the next 3 days. The rise is larger the larger that fall, and larger still the more its 5-day volatility exceeds its 30-day volatility.
Consequence: A trader should buy, or at least refuse to short, a coin right after a sharp one-day drop in a volatility spike, where the 3-day rebound is several times the cost of a trade.
Why:
- F1: A sharp one-day fall is followed by a rebound. On the non-overlapping 3-day grid, the bars in the lowest decile of the past 1-day return (scaled by the 30-day volatility) are followed by a 3-day move of +2.04 % above the coin's drift. That is t 6.7 over 911 cases, positive in 18 of 19 coins, about 9 times the 0.22 % cost of a trade. The next decile shows only +0.25 % (t 0.97), and the middle deciles are negative (-0.13 to -0.92 %).
- F2: The rebound after a sharp one-day fall is much larger when recent volatility has expanded. In the lowest 1-day quintile, the bars with the top quintile of 5-day over 30-day volatility are followed by +3.17 % above drift (t 7.0, 460 cases, 18 of 19 coins). The other bars in that quintile show +0.46 % (t 1.9, 1362 cases). Across all bars, the top volatility-ratio quintile alone gives +1.09 % (t 4.5, 17 of 19 coins).
- F3: The rebound after a sharp one-day fall holds in every era and in both trends. By era it is +0.94 % (t 2.0) up to 2020, +1.80 % (t 3.7) over <date> and +0.90 % (t 3.3) from 2023, all above drift. It is larger when the coin's 30-day return is positive: +2.10 % (t 6.1, 811 cases) against +0.38 % (t 1.5, 1011 cases).
- F6: A downward break after a wide 2-day stretch is followed by a rebound. The widest decile of such breaks shows +2.51 % against drift (t 5.1, 491 cases, 17 of 19 coins). Within the widest quartile, the rebound is largest after the deepest 2-day falls: +1.34 % (t 3.6, 781 cases). This is largely the same situation as F1.
