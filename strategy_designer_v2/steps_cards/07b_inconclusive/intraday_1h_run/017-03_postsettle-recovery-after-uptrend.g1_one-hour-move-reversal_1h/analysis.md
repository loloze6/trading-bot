---
line: 7.b inconclusive
backtest: 017-03_postsettle-recovery-after-uptrend.g1_one-hour-move-reversal_1h
idea tested: 017-03_postsettle-recovery-after-uptrend.g1_one-hour-move-reversal
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3041 USD
---
## Findings
- **F1:** The fade is real and clearly graded by the size of the last-hour move. The pooled excess gain is 8.15e-05 per bar (t 10.23, 416,645 bars). It rises with the size of the forecast, from 0.1e-05 (t 0.74) at |forecast| ≤ 2 to 18.1e-05 (t 5.91) at |forecast| above 15. The raw fade, the next-hour return against the sign of the last hour, grows from −2.7e-05 (t −0.78) in the smallest |z| quintile to 33.1e-05 (t 7.58) in the largest.
- **F2:** The 30-day-volatility check points the predicted way but is weak, which is why the result is unclear. High-volatility bars earn 10.0e-05 (t 8.10) against 6.9e-05 (t 5.08) for low-volatility bars, a Welch t of 1.69 with 156,480 bars in each group. High beats low in all six coins, but only by 0.6e-05 (ZEC) to 6.5e-05 (LTC).
- **F3:** Most of the volatility effect sits in the top volatility quintile. That quintile earns 13.4e-05 (t 7.16), while quintiles 1 to 4 sit between 6.2e-05 and 8.7e-05 with no order among them, so a split at the median dilutes it.
- **F4:** The volatility effect is mixed across move sizes and seems to be mostly a matter of scale. In the 4th |z| quintile high volatility earns 23.1e-05 against 8.5e-05 for low, but in the top |z| quintile high earns 17.3e-05 against 21.0e-05 for low (Welch t −0.49). The slope of the next-hour return over volatility on z is almost the same in both groups: −0.0163 (t −6.68) high against −0.0138 (t −4.98) low.
- **F5:** The reversal keeps building after the first hour. On non-overlapping samples the sign-fade averages 1.77e-04 at 1 hour (t 10.77, n 416,501), 3.65e-04 at 2 hours (t 11.30, n 208,134), 3.77e-04 at 4 hours (t 5.97, n 103,944) and 4.46e-04 at 8 hours (t 3.58, n 51,843). Most of it arrives within 2 hours.
- **F6:** The book loses because of turnover, not because the signal is wrong. The implied fee is 6.56e-04 per bar against a gross excess of 0.81e-04, a net of −5.75e-04 per bar. Mean turnover is 0.61 of the book per bar, giving a Sharpe of −16.35.

## Ideas
- `017-03_postsettle-recovery-after-uptrend.g1_one-hour-move-reversal.b1_one-hour-reversal-more-coins` (from F1, F2): A coin's return over the next 1 hour runs against its own last-hour return, and the larger that move relative to the coin's recent hourly volatility, the larger the reversal. The reversal is strongest when the coin's 30-day volatility is high.
- `017-03_postsettle-recovery-after-uptrend.g1_one-hour-move-reversal.b2_two-hour-reversal-after-sharp-hour` (from F1, F5, F6): A coin's return over the next 2 hours runs against its own last-hour return, and the larger that move is relative to the coin's recent hourly volatility, the larger the reversal.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
