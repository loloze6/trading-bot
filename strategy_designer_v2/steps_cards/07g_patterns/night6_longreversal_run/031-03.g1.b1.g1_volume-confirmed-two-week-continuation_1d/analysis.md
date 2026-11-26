---
line: 7.g patterns
backtest: 031-03.g1.b1.g1_volume-confirmed-two-week-continuation_1d
idea tested: 031-03.g1.b1.g1_volume-confirmed-two-week-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4562 USD
---
## Findings
- **F1:** A coin's own volume swell alone, whatever the direction of its price, sorts its next 14 days in a steady gradient: by coin-quintile of the 14-day over 30-day mean-volume ratio, the 14-bar move above the coin's normal drift runs -5.41 % (t -2.92 with same-day cases summed, 73 days), -1.02 %, +0.57 %, +1.52 % and +6.24 % (t 2.19, 70 days), with Spearman rho 0.19 over 1280 non-overlapping cases (p 7e-12).
- **F2:** Going long when the ratio is above the coin's median and short when it is below earns +3.26 % per case over 14 days above the normal drift (t 3.35 with same-day cases summed, 131 days, 1280 cases). That is about 0.17 of the coin's usual 14-day move of 18.9 % and 15 times the 0.22 % cost of a trade; the same split gives +1.03 % over 7 days (t 1.73).
- **F3:** This volume pattern holds in all 18 coins with cases (from +0.3 % for BTC to +9.2 % for AVAX), in 7 of 8 years (2019 is -0.9 %; 2018 to 2025 otherwise +0.4 % to +6.9 %), in 18 of 24 windows, and in both recorded regimes (+3.0 % mean_reversion, +3.5 % trending).
- **F4:** Most of the pattern is market-wide timing rather than one coin against the others: the Spearman rho of the log volume ratio with the move above drift falls from 0.190 to 0.034 once each day's mean across coins is removed (1259 cases), and 45 % of the ratio's variance is shared across coins on the same day.
- **F5:** The tested direction rule only works on its swell side: following the 14-day return gives +2.63 % in the top volume-ratio tercile (t 2.38, 427 cases), but the fade side earns nothing (-0.05 % in the bottom tercile, t -0.07). There a dry-up predicts a fall whatever the earlier return (F1), which is why the tested idea's t is only 1.35.
- **F6:** The brief's two-to-three-month reversal does not show in these bars: the 60-day return has Spearman rho +0.008 with the next 14 days' move above drift (768 cases, p 0.83), and its largest-move tercile leans with the move, not against it (+0.34 %, t 0.25).
- **F7:** Days of the week differ (the mean daily return over coins is +0.46 % on Saturdays, t 3.00 over 414 days, and Wednesday, Friday and Saturday beat the other days in 7 of 8 years). This is a calendar condition, not a graded situation, and the next-day bounce after a large down day is not reliable (t 0.98 over 678 days).

## Ideas
- `031-03.g1.b1.g1.g1_volume-swell-predicts-direction` (from F1, F2, F3, F4, F5): The more a coin's mean daily volume over the last 14 days has risen above its 30-day mean, the more its price rises over the next 14 days, and the further that volume has fallen below its 30-day mean, the more its price falls over the next 14 days, whichever way its 14-day return points.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
