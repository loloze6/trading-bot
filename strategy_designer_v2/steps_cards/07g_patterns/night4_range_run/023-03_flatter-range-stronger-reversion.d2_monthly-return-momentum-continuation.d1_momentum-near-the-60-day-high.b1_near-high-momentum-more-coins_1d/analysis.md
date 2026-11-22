---
line: 7.g patterns
backtest: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.b1_near-high-momentum-more-coins_1d
idea tested: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.b1_near-high-momentum-more-coins
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4778 USD
---
## Findings
- **F1:** The tested monthly momentum works mainly in calm coins. Split by each coin's own 20-day volatility into terciles, the slope of the 5-day demeaned move (in units of the usual move) on the 30-day return is 0.32 (t 2.86) in the calmest third, 0.25 (t 2.91) in the middle third and 0.08 (t 1.39) in the most volatile third, about 1,790 grid cases each. Split by volatility pooled across coins, the same falloff shows: 0.50 (t 4.01), 0.19 (t 2.07), 0.04 (t 1.04).
- **F2:** The 30-day return divided by the coin's 20-day daily volatility (times the square root of 30) predicts the next 5 days better than the raw 30-day return: t 4.22 against 3.45 on the same 5,363 non-overlapping cases. The vol-scaled t also stays higher inside each own-volatility tercile: 3.30, 3.00 and 1.42 against 2.86, 2.91 and 1.39.
- **F3:** The book's gain comes from the long side alone. Long bars earn +0.168 % per bar over 20,837 bars and short bars lose 0.021 % over 11,013. Long trades average +10.9 % net with a median of −1.0 %; short trades average −0.70 %.
- **F4:** The gain is carried by long holdings. Trades held over 15 days average +27.8 % net, while trades held 4 days or less average −2.37 %, with 2,080 trades in each duration quartile. The gain is uneven across years: the momentum t is negative in 2018 (down to −3.00) and 2022 (down to −2.55) and positive in 2020 (3.39 and 2.81 in the two calmer terciles).
- **F5:** The steepest monthly losers do not keep falling, but the difference does not clear chance after this many angles. The lowest 30-day-return quintile has a 5-day excess of −0.39 % (t −1.09) against −1.28 % (t −4.08) for the second quintile. The bottom fifth of the 60-day range has z +0.009 (t 0.17) against −0.068 (t −3.09) for the next fifth; the quintile gap is t ≈ 1.9.
- **F6:** The weekday pattern seen per case (Tuesday z +0.18, t 5.0; Sunday −0.14, t −3.9) disappears once coins are averaged per date. Next-day excess by weekday then has a largest |t| of 1.91 over 7 weekdays (about 414 dates each), and no weekday keeps its sign across years.

## Ideas
- `023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.b1_near-high-momentum-more-coins.g1_volatility-scaled-monthly-momentum` (from F2, F1): The larger a coin's 30-day return measured against its own 20-day daily volatility, the larger its rise over the next 5 days.
- `023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.b1_near-high-momentum-more-coins.g2_momentum-stronger-in-calm-coins` (from F1, F3): The larger a coin's 30-day return, the larger its rise over the next 5 days, the more so the lower the coin's 20-day volatility stands against its own past.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
