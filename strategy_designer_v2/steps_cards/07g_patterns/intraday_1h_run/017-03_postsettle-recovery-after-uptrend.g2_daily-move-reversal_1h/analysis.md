---
line: 7.g patterns
backtest: 017-03_postsettle-recovery-after-uptrend.g2_daily-move-reversal_1h
idea tested: 017-03_postsettle-recovery-after-uptrend.g2_daily-move-reversal
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3701 USD
---
## Findings
- **F1:** The tested day-reversal works only when the coin is volatile. On non-overlapping 24-hour cases split into terciles of each coin's 7-day volatility, the sign-based reversal earns +0.0051 per case (t 5.53, n 5413) in the top tercile. It earns −0.00097 (t −2.13) and −0.00106 (t −1.78) in the lower two. The z-weighted reversal t in the top tercile is positive for all six coins (1.85 to 2.88) and in every year (0.62 to 4.67).
- **F2:** The trigger is volatility that is high relative to the coin's own longer volatility. Split into terciles of 7-day over 30-day volatility, the top tercile gives a reversal of +0.0062 per case (t 6.01, n 4308). The other two give −0.0005 (t −0.78) and −0.0008 (t −0.99).
- **F3:** Inside the high-volatility tercile, the next-day move is monotone in the past day's vol-scaled move. The most-down quintile (z −1.37) is followed by +1.17% (t 4.61) and the most-up quintile (z +1.32) by −0.74% (t −3.39). In the low-volatility tercile the sign flips: the most-down quintile is followed by −0.30% (t −2.40), rising monotonically to +0.15% for the most-up.
- **F4:** The book loses for two reasons.
- **F5:** Hourly bars reverse, and the reversal grows with the size of the last hour's move in units of its 7-day hourly standard deviation. Across quintiles of |1h move| the reversal product rises from 0.0000006 (t 0.18) to 0.00098 (t 6.66), with about 78,490 cases each. It is positive in 41 of 48 coin-years.
- **F6:** Clock-time and weekday effects stand out even after 24 hours and 7 days were tested, but they are ungraded:

## Ideas
- `017-03_postsettle-recovery-after-uptrend.g2_daily-move-reversal.g1_reversal-after-volatility-expansion` (from F1, F2, F3, F4): When a coin's 7-day volatility is high relative to its own 30-day volatility, its return over the next 1 day runs against its past 1-day return. The larger the past day's move in units of its 7-day volatility, and the higher that volatility ratio, the larger the move back.
- `017-03_postsettle-recovery-after-uptrend.g2_daily-move-reversal.g2_calm-market-daily-continuation` (from F3, F1): When a coin's 7-day volatility is low relative to its own history, its return over the next 1 day follows its past 1-day return. The larger the past day's move in units of its 7-day volatility, the larger the continuation.
- `017-03_postsettle-recovery-after-uptrend.g2_daily-move-reversal.g3_outsized-hourly-move-reversal` (from F5): A coin's return over the next 1 hour runs against its past 1-hour return, and the larger that move in units of the coin's 7-day hourly volatility, the larger the move back.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
