---
line: 7.e profitable but not proven
backtest: 031-01.g1.g1.g2.d1_volatile-rising-weekends-continue_1d
idea tested: 031-01.g1.g1.g2.d1_volatile-rising-weekends-continue
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4005 USD
---
## Findings
- **F1:** The book's gain is timing rather than the market's own rise: its mean daily return is 0.0285 % (t 3.01 over 2,898 days), and only 0.0057 % a day, about 20 %, comes from the position times the coin's mean daily return. Summed per bar, the market part is 0.99 of 5.66.
- **F2:** Almost all of the gain is earned on positions held from Friday's close and from Saturday's close, 3.05 and 2.62 of the 5.66 summed bar gain. Every other weekday adds between -0.11 and +0.14.
- **F3:** The high-volatility condition does not carry the effect. On Fridays with a 14-day rise, the 2-day unusual move is +1.19 % (t 3.80, 319 cases) when volatility is above its usual level and +0.95 % (t 3.91, 297 cases) when it is not.
- **F4:** Among Fridays with a 14-day rise, the unusual move is +0.92 %, +0.90 %, +0.94 % and +1.52 % across the four quartiles of the volatility ratio. This flat grading explains why the plan's median split failed (-0.05 %).
- **F5:** The 14-day return is graded. Across all Fridays, a standardised 14-day return (its return over the 60-day daily volatility times √14) predicts the 2-day unusual move in units of the coin's usual move with slope 0.108 (t 5.72, 1,224 Fridays, Spearman 0.12). Its quintiles rise from -0.64 % (t -1.00, 77 days) to +1.76 % (t 3.20, 94 days).
- **F6:** The 14-day lookback is the best of those tried for the Friday 2-day move: slope t 5.72, against 4.99 for 28 days, 3.95 for 7 days and 1.09 for 3 days.
- **F7:** The same graded continuation shows from the Wednesday close (slope t 3.84), the Thursday close (t 6.87) and the Friday close (t 5.72), but not from Monday (t -1.66), Tuesday (-0.18), Saturday (1.60) or Sunday (0.53). These are overlapping samples, indicative only.
- **F8:** Only the long side holds. Fridays with a 14-day fall give +0.32 % in the short direction (t 0.82, 147 days), against +1.07 % (t 3.37, 156 days) for Fridays with a 14-day rise.
- **F9:** The gain is uneven across years and coins but spread wide. The book's mean daily return is near zero in 2018 (0.0006 %), 2021 (0.0016 %) and 2022 (0.0052 %), and 0.034–0.066 % in the other years. All six coins gain, with XRP the largest at 1.64 of 5.66. The top 10 of 781 trades give 32 % of the summed net trade return.

## Ideas
- `031-01.g1.g1.g2.d1.e1_late-week-momentum-into-weekend` (from F1, F2, F3, F4, F5, F6, F7): The larger a coin's 14-day return, measured against its own usual daily volatility, at a Thursday or Friday close (UTC), the larger its rise over the next 2 days into the weekend, whatever the level of its recent volatility.
- `031-01.g1.g1.g2.d1.e2_friday-rise-weekend-continuation` (from F3, F4, F5, F8): The larger a coin's 14-day rise, measured against its usual daily volatility, at Friday's close (UTC), the larger its gain over Saturday and Sunday beyond its normal drift.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
