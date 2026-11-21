---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high.d1_ninety-day-breakout-twenty-day-continuation
line: 7.g patterns
backtest: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high.d1_ninety-day-breakout-twenty-day-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's daily return measured against its 20-day volatility, the more its next day's return goes the opposite way, and this reversal is stronger the higher the coin's 20-day volatility.
Consequence: A trader should fade a coin's large daily move for one day when the coin is volatile, harder the larger the move, and refuse to chase it overnight.
Why:
- F1: When a coin's 20-day volatility is high, a large daily return is followed by a move the other way the next day. In each coin's highest 20-day-volatility tercile, the next day's drift-adjusted return, scaled by volatility, falls with today's volatility-scaled return (slope −0.090, t −6.53, 4787 non-overlapping cases). In the lowest tercile the slope is +0.042 (t 1.89, 4787 cases) and in the middle one −0.012 (t −0.71). The mean absolute daily move is 4.1 % in the high tercile against 2.3 % in the low one, so a reversal of about 0.09 of a daily move per unit of z is about 0.4 % per case. That is above the 0.19 % round trip.
- F2: Pooled over all volatility levels, the one-day reversal is weak and unstable. The overall slope is −0.016 (t −1.52, 14356 cases). It is −0.080 (t −3.24) on XMR and between −0.030 and +0.016 on the other five coins. By year it is −0.060 (t −2.20) in 2018 and −0.077 (t −2.62) in 2020, but +0.054 (t 1.91) in 2024. In bins, a day of −1 to −2 volatility units is followed by +0.52 % drift-adjusted (t 3.68, 1390 cases), and a day of 0 to +1 units by −0.19 % to −0.24 % (t −2.4 to −2.5).
