---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-03_postsettle-recovery-after-uptrend.g2_daily-move-reversal
line: 7.g patterns
backtest: 017-03_postsettle-recovery-after-uptrend.g2_daily-move-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 7-day volatility is low relative to its own history, its return over the next 1 day follows its past 1-day return. The larger the past day's move in units of its 7-day volatility, the larger the continuation.
Consequence: In calm markets, do not fade a strong day; lean with it in proportion to its size.
Why:
- F3: Inside the high-volatility tercile, the next-day move is monotone in the past day's vol-scaled move. The most-down quintile (z −1.37) is followed by +1.17% (t 4.61) and the most-up quintile (z +1.32) by −0.74% (t −3.39). In the low-volatility tercile the sign flips: the most-down quintile is followed by −0.30% (t −2.40), rising monotonically to +0.15% for the most-up.
- F1: The tested day-reversal works only when the coin is volatile. On non-overlapping 24-hour cases split into terciles of each coin's 7-day volatility, the sign-based reversal earns +0.0051 per case (t 5.53, n 5413) in the top tercile. It earns −0.00097 (t −2.13) and −0.00106 (t −1.78) in the lower two. The z-weighted reversal t in the top tercile is positive for all six coins (1.85 to 2.88) and in every year (0.62 to 4.67).
