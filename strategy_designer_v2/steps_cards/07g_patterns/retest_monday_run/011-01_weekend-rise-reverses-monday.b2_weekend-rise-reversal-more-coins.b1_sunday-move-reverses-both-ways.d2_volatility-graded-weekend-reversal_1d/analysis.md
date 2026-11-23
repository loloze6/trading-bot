---
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d2_volatility-graded-weekend-reversal_1d
idea tested: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d2_volatility-graded-weekend-reversal
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4676 USD
---
## Findings
- **F1:** On Sunday bars, the weekend splits into two opposite effects. In a joint regression over 4325 Sunday cases, Saturday's vol-scaled move carries on into Monday–Tuesday (beta +0.216, t 5.97; into Monday alone +0.135, t 5.55). Sunday's own move reverses (beta −0.078, t −2.39; Monday alone −0.071, t −3.23). That is why the Saturday+Sunday return predicts continuation (slope +0.053, t 2.09) while the Sunday return alone predicts reversal (−0.092, t −2.82).
- **F2:** Sunday's reversal is a market-wide move in time, not a difference between coins on the same date. Measured per date, sign(Sunday move) × the next days' vol-scaled return is −0.111 for one day (t −2.51), −0.178 for two days (t −2.85) and −0.224 for three days (t −2.72), over about 340 dates. The per-date cross-coin slope has the opposite sign (+0.060, t 1.46). For the next day, only 3 of 19 coins have a continuation slope.
- **F3:** Sunday's reversal is not graded by the size of the move. The signed 2-day reversal, in units of 20-day volatility, is 0.080, 0.247, 0.245 and 0.058 from the smallest to the largest quartile of |Sunday move| (t 1.42, 3.96, 4.90, 0.99), so the largest moves reverse least.
- **F4:** The volatility-ratio grading behind the confirmed idea is not monotone. The signed 2-day reversal is 0.159, 0.044, 0.065 and 0.240 from the lowest to the highest quartile of s20/s60 (t 1.74, 0.62, 0.94, 3.52, about 650 cases each).
- **F5:** Low weekend volume does not deepen Sunday's reversal, against the brief. The signed reversal is 0.159, 0.236, 0.134 and 0.102 from the lowest to the highest quartile of Sunday volume against its 20-day mean (t 3.16, 3.97, 2.36, 1.69).
- **F6:** The reversal is fading over time. The signed Sunday-to-Tuesday reversal by year is 0.282, 0.173, 0.395 and 0.165 in 2018–2021, then 0.048, 0.084, 0.186 and 0.120 in 2022–2025. The Sunday-to-Monday reversal turns positive in 2025 (+0.047).
- **F7:** Friday's move carries on into Saturday, graded by volume and size, but much of it is common to all coins on the same date. The signed next-day return rises with Friday volume quartile (0.009, 0.023, 0.050, 0.138; top quartile t 3.55) and with |Friday move| quartile (top quartile 0.177, t 4.74). 16 of 19 coins have a positive slope, yet the per-date cross-coin slope has t 1.27 for one day and 2.64 for three days.
- **F8:** The book earns almost all its gain on Mondays and Tuesdays: mean daily return 0.00174 on Monday and 0.00075 on Tuesday, against −0.00035 on Sunday, the day it pays to enter, and about 0.0000–0.0001 on the other days.

## Ideas
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d2_volatility-graded-weekend-reversal.g1_saturday-move-continues-early-week` (from F1, F2): At Sunday's close, a coin's Saturday return continues in the same direction over the next 2 days (Monday and Tuesday), and the continuation is larger the larger Saturday's return is relative to the coin's 20-day daily volatility.
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d2_volatility-graded-weekend-reversal.g2_high-volume-friday-move-continues` (from F7): A coin's Friday return continues in the same direction over the next day (Saturday), and the continuation is larger the higher Friday's volume is relative to the coin's 20-day average volume.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
