---
line: 7.g patterns
backtest: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high.d1_ninety-day-breakout-twenty-day-continuation_1d
idea tested: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high.d1_ninety-day-breakout-twenty-day-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3853 USD
---
## Findings
- **F1:** When a coin's 20-day volatility is high, a large daily return is followed by a move the other way the next day. In each coin's highest 20-day-volatility tercile, the next day's drift-adjusted return, scaled by volatility, falls with today's volatility-scaled return (slope −0.090, t −6.53, 4787 non-overlapping cases). In the lowest tercile the slope is +0.042 (t 1.89, 4787 cases) and in the middle one −0.012 (t −0.71). The mean absolute daily move is 4.1 % in the high tercile against 2.3 % in the low one, so a reversal of about 0.09 of a daily move per unit of z is about 0.4 % per case. That is above the 0.19 % round trip.
- **F2:** Pooled over all volatility levels, the one-day reversal is weak and unstable. The overall slope is −0.016 (t −1.52, 14356 cases). It is −0.080 (t −3.24) on XMR and between −0.030 and +0.016 on the other five coins. By year it is −0.060 (t −2.20) in 2018 and −0.077 (t −2.62) in 2020, but +0.054 (t 1.91) in 2024. In bins, a day of −1 to −2 volatility units is followed by +0.52 % drift-adjusted (t 3.68, 1390 cases), and a day of 0 to +1 units by −0.19 % to −0.24 % (t −2.4 to −2.5).
- **F3:** Over 2 to 5 days, a coin's volatility-scaled past return predicts the same direction over the same span. The slope is 0.048 at 2 days (t 3.24, 7066 cases), 0.053 at 3 days (t 2.90, 4715 cases) and 0.077 at 5 days (t 3.04, 2699 cases). The largest rises carry most of it: after a 2-day rise above 2 volatility units, the next 2 days earn +1.72 % drift-adjusted (t 2.41, 227 cases). After such a 3-day rise, the next 3 days earn +1.78 % (t 2.32, 173 cases).
- **F4:** The tested breakout shows no continuation on the 20-day grid. Closes 0 to 5 % above the prior 90-day high are followed by −3.6 % drift-adjusted over 20 days (t −1.25, 25 cases), and closes 5 to 15 % above it by −10.2 % (t −1.40, 14 cases). Closes 0 to 3 % below the high are followed by +16.4 % (t 1.21, 35 cases). At 5 days the sign flips between neighbouring bins: +1.0 % for 8 to 15 % below the high (t 2.29, 555 cases) and −1.0 % for 15 to 25 % below (t −2.91, 639 cases). Nothing here can be told apart from chance after this many bins.
- **F5:** The book's daily mean of 0.024 % falls short of holding the coins in every rising year and beats it only in falling ones.
- **F6:** Weekday effects on next-day drift-adjusted returns are small against the number of angles looked at (about 2070 cases each). Monday is −0.26 % (t −2.57), Wednesday −0.30 % (t −2.53) and Friday +0.24 % (t 2.66). None stands out enough to count.

## Ideas
- `020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high.d1_ninety-day-breakout-twenty-day-continuation.g1_volatile-day-next-day-reversal` (from F1, F2): The larger a coin's daily return measured against its 20-day volatility, the more its next day's return goes the opposite way, and this reversal is stronger the higher the coin's 20-day volatility.
- `020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high.d1_ninety-day-breakout-twenty-day-continuation.g2_large-three-day-move-continues` (from F3): The larger a coin's 3-day return measured against its volatility over 3 days, the more it keeps moving in the same direction over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
