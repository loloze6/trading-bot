---
line: 7.g patterns
backtest: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation_1h
idea tested: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3968 USD
---
## Findings
- **F1:** Hourly returns between 21:00 and 23:00 UTC rise far more than any other hours. Pooled raw means are 5.5e-4 at 21h (t 6.87) and 4.4e-4 at 22h (t 5.76), against at most t 3.2 for any other hour. In units of each coin's 20-day hourly volatility, the 21–22h bars average +0.032 to +0.061 against about 0 for the other hours, and all six coins are positive (Welch t 1.88 to 3.70). The late-minus-other gap is positive in 18 of 24 windows (t 3.26 across windows) and in 7 of 8 years; 2022 is the exception at −0.053 (t −2.80).
- **F2:** The size of a coin's 1-day move, scaled by its 20-day volatility, predicts its 3-day excess return in a U shape. On the non-overlapping 72-bar grid, the bottom quintile (largest 1-day falls) is followed by +0.0066 (t 2.32, n 939) and the top quintile (largest rises) by +0.0047 (t 1.64). The middle three quintiles give −0.0028 to −0.0046. The Spearman correlation of the absolute scaled 1-day move with the 3-day excess return is positive in all six coins (0.026 to 0.064, about 780 cases each).
- **F3:** The 1-day-over-20-day volume ratio is graded the same way on the 72-bar grid. Its top quintile is followed by +0.0065 3-day excess (t 2.22) and its bottom quintile by −0.0058 (t −2.30). Its Spearman correlation with the excess is positive in all six coins (0.010 to 0.095, strongest in ZEC 0.095 and XRP 0.085). The top-minus-bottom spread holds in both halves of the 10-day scaled return (+0.0094 low half, +0.0151 high half).
- **F4:** Compression does not precede larger moves, against the brief. The narrowest 5-day high-low range quintile (scaled by 20-day volatility) is followed by a mean absolute 3-day move of 0.0549, about the same as the middle quintiles (0.052 to 0.056). The widest-range quintile is followed by 0.0663, and the highest 1-day-versus-20-day volatility quintile by 0.0619 against 0.0534 for the lowest. Large moves follow large moves, not quiet periods.
- **F5:** The tested signal's edge sits only in its top quintile and is not consistent per coin. The pooled 10-day scaled-return quintiles give +0.0007, −0.0017, −0.0047, −0.0008 and +0.0070 (t 2.19 only for the top). Per coin, the top-minus-bottom Welch t ranges from −0.62 (LTC) to 1.55 (ZEC), and XMR's top quintile has a negative excess (−0.0055).
- **F6:** The book is mostly market exposure. Its mean daily return is 0.00043, of which 0.000315 (73%) is the gain from the market's own rise at a mean position of 0.27. Its Sharpe is negative in 11 of 24 windows, and it is below holding's Sharpe in 15 of the 24.

## Ideas
- `006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation.g1_late-utc-hour-drift` (from F1): A coin's price rises over the two hours from 21:00 to 23:00 UTC each day, by an amount that grows with the coin's own 20-day hourly volatility.
- `006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation.g2_large-daily-move-rebound` (from F2, F4): The larger a coin's 1-day move relative to its own 20-day volatility, in either direction, the more its price rises over the next 3 days relative to its usual 3-day return. The strongest rise follows the sharpest 1-day falls.
- `006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation.g3_relative-volume-predicts-rise` (from F3, F4): The higher a coin's volume over the last day relative to its own 20-day average volume, the more its price rises over the next 3 days relative to its usual 3-day return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
