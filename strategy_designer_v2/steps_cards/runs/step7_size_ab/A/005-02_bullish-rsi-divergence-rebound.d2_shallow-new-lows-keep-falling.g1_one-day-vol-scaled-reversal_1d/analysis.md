---
line: 7.d not profitable
backtest: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal_1d
idea tested: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3101 USD
---
## Findings
- **F1:** The book's gain before fees does not cover its fees. Gross gain is 0.000231 per day and fees are 0.000360 per day, so the net is -0.000129, which matches the book's mean daily return of -0.000134 (Sharpe -0.19) at 0.80 trades per bar.
- **F2:** The long side pays and the short side loses. Long days (n=2823) earn 0.000769 gross, of which 0.000306 is timing and 0.000464 is the coin's drift. Short days (n=2958) lose 0.000281 gross because holding short against the coin's rise costs 0.000351, and their timing adds only 0.000071.
- **F3:** Shorts lose only while the coin's 60-day return is positive. There, short days (n=835) lose 0.001051 gross with timing of -0.000650. While the 60-day return is negative, short days (n=632) earn 0.001351 gross with timing of +0.001617.
- **F4:** The 20-day trend tells the same story. Short days with a positive 20-day return (n=1419) lose 0.000585. Short days with a negative 20-day return (n=1032) earn 0.000511 with timing of +0.000801.
- **F5:** The rebound after falls is graded but the give-back after rises is not. Next-day returns rise from +0.000692 at a vol-scaled move of -0.08 to +0.004593 at -1.81 (t 2.03). After rises the next day is mixed: +0.001320 at +0.96, then only -0.001551 (t -0.91) at the largest, +1.90.
- **F6:** The long rebound is stronger inside a 60-day uptrend. Long days earn 0.001116 gross (timing +0.000584, n=720) when the 60-day return is positive, against 0.000169 (timing -0.000234, n=727) when it is negative.
- **F7:** Small moves still carry positions and fees. In the middle deciles of the vol-scaled move (z -0.08 to +0.31), positions are 0.05 to -0.12 and gross is -0.000192 to +0.000201. Fees are paid on these days as on others, about 0.00036 a day overall.

## Ideas
- `005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d1_give-back-only-in-downtrends` (from F2, F3, F4, F5): The larger a coin's 1-day fall relative to its own 20-day daily volatility, and the nearer its close to the day's low, the more it rises over the next 1 day. The larger its vol-scaled 1-day rise, the more it gives back over the next 1 day, only while its 60-day return is negative, and the more so the deeper that 60-day fall.
- `005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_dip-rebound-in-uptrends` (from F1, F2, F6, F7): The larger a coin's 1-day fall relative to its own 20-day daily volatility, and the nearer its close to the day's low, the more it rises over the next 1 day, and the more so the higher its 60-day return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
