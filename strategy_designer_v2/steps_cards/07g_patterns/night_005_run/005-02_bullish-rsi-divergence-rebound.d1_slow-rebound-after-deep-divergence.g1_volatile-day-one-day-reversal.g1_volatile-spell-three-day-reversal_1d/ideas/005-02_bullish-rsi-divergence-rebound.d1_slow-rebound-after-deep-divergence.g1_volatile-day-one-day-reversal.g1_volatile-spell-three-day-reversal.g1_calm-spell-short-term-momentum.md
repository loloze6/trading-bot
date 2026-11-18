---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal.g1_volatile-spell-three-day-reversal
line: 7.g patterns
backtest: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal.g1_volatile-spell-three-day-reversal_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 20-day volatility sits below its 60-day average, its return over the next 3 days follows the direction of its 5-day return. The larger that 5-day return relative to the coin's usual 60-day daily move, and the lower the volatility ratio, the larger the continuation.
Consequence: In a calm spell, a trader leans with a strong recent run for a few days instead of fading it, and leans harder the calmer the spell; the fade is kept for volatile spells only.
Why:
- F1: The day's move behaves oppositely in the two volatility regimes. On the non-overlapping 3-day grid, the clipped day-return z times the coin-demeaned 3-day forward return has a mean of +0.0054 (t 2.05, n 710) when 20-day volatility is below its 60-day average, and −0.0147 (t −3.33, n 573) when it is above. In the calm regime the top day-return quintile (mean z 1.64) is followed by +1.22% excess (t 2.41, n 142), and the bottom quintile by −0.28%.
- F2: In the calm regime, the top quintile of the scaled 5-day return is followed by a +2.02% excess 3-day return (t 3.90, n 142), while the other four quintiles all lie between −0.72% and −0.09%. The pooled product of 5-day z and forward return has t 2.08 (n 710), against t 0.92 (n 573) in the volatile regime.
- F3: The calm-regime continuation grows the calmer the spell. By volatility-ratio tercile, the day-z product is +0.0100 (t 2.32, n 237) at a mean ratio of 0.61, +0.0084 (t 1.80, n 236) at 0.80, and −0.0021 (t −0.44, n 237) at 0.93.
- F5: The continuation is positive in both halves of the windows (w1–12: t 1.90, n 375; w13–24: t 0.97, n 335), so it is not one stretch alone.
