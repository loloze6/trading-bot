---
brief: 010_rsi-midline-regime-direction
source-idea: 010-01_rsi-above-midpoint-continues-up
line: 7.g patterns
backtest: 010-01_rsi-above-midpoint-continues-up_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's one-day return relative to its own recent 60-day daily volatility, the larger its move in the same direction over the next 7 days.
Consequence: A trader would lean with the most recent day's outsized move for the following week rather than wait for a multi-week RSI regime to form.
Why:
- F1: The coin's last one-day return predicts the next 7 days in the same direction. The pooled OLS slope of the 7-day forward return minus the coin's mean, on the per-coin standardised 1-day return, is 0.0107 per standard deviation (t = 2.79, n = 767 non-overlapping cases, BTC and ETH). By quintile, the lowest 1-day return quintile is followed by −2.01% (t = −2.29) and the top two quintiles by +1.16% and +1.17%. The same return scaled by its own 60-day volatility keeps the sign (slope 0.0082, t = 2.02, n = 671).
- F2: The tested RSI-above-midline share gives a graded but weaker version of this momentum. Its quintiles run from −0.66% to +1.15% excess 7-day return, with pooled t = 1.73 (n = 815). The 14-day return gives t = 1.60 (n = 719), the 3-day return t = 0.72, and the 60-day return t = −0.13 (n = 383). The information sits in the most recent moves, not in long trends.
