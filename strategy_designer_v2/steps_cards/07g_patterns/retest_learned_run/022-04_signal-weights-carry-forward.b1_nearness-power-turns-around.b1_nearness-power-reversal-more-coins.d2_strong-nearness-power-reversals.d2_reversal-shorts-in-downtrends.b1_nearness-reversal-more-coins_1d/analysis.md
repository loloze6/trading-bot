---
line: 7.g patterns
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends.b1_nearness-reversal-more-coins_1d
idea tested: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends.b1_nearness-reversal-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6756 USD
---
## Findings
- **F1:** The wider a coin's daily range relative to its 20-day volatility, the larger its drift-removed rise over the next 5 days: Spearman rho +0.083 (t about 5.4, 4177 non-overlapping cases). The top range quintile gains +1.28 % beyond drift (t 3.22), while the bottom three quintiles sit between -0.55 % and -0.75 %. Rho is positive in all 16 coins and in 6 of 8 years.
- **F2:** The range effect comes from days that close up. In the top range quintile, up days are followed by +2.29 % beyond drift over 5 days (t 3.29, 385 cases), while down days are followed by only +0.41 % (t 1.05, 454 cases). Lower range quintiles stay near -0.5 % to -0.8 % whichever way the day closed.
- **F3:** The higher a coin's daily volume relative to its 20-day average, the larger its drift-removed 5-day return: rho +0.065 (t about 4.2, 4177 cases). The lowest-volume quintile is followed by -1.57 % (t -4.00). Rho is positive in 14 of 16 coins and 7 of 8 years, and stronger after a falling week (rho +0.112 when the 5-day return is not positive, +0.035 when it is).
- **F4:** In coins whose 20-day return is negative, the larger the 5-day return scaled by 20-day volatility, the larger the drift-removed fall over the next 5 days: rho -0.074 (t -3.28, 1974 cases). The top quintile, the sharpest bounces, falls -1.82 % beyond drift (t -3.40). Rho is negative in 14 of 15 coins. In coins whose 20-day return is not negative the relation is absent (rho +0.006, t 0.28).
- **F5:** In coins whose 20-day return is negative, a low ratio of 20-day to 60-day volatility is followed by a fall. The lowest quintile falls -2.16 % beyond drift over 5 days (t -3.97, 324 cases), and the overall rho is +0.078 (t 3.12). This is less stable than F4: positive in only 5 of 8 years and 12 of 15 coins.
- **F6:** The tested reading's falls are not specific to falling coins. Strong shorts (forecast below -0.5) where the 20-day return was not negative were followed by -1.77 % beyond drift (t -2.41, 176 cases). In the active regime they were followed by -0.89 % (t -2.27, 714 cases), and active-regime cases rose beyond drift in 2023 (+0.29 %, 194 cases).
- **F7:** The book lost money in short holds and made it in long holds. Shorts closed within about 5 days lost -3.36 % net on average (705 trades). Shorts held over 20 days gained +6.19 % (259 trades, median +9.50 %). The book's mean daily return was -0.002 %, and its best 2 % of days came when the coins fell -8.3 % on average.
- **F8:** Five-day returns depend on the starting weekday. Cases starting on a Tuesday close gained +2.20 % beyond drift (t 4.38, 651 cases), and those starting on a Sunday lost -2.45 % (t -5.63, 678 cases). Tuesday minus Sunday is positive in 7 of 8 years. This is not a graded situation, so it supports no idea here.

## Ideas
- `022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends.b1_nearness-reversal-more-coins.g1_wide-up-days-continue` (from F1, F2): The wider a coin's daily high-low range is relative to its 20-day volatility on a day it closes higher, the larger its rise over the next 5 days.
- `022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends.b1_nearness-reversal-more-coins.g2_volume-surge-precedes-rise` (from F3): The higher a coin's daily volume is relative to its 20-day average volume, the larger its rise over the next 5 days, most of all after a falling 5-day stretch.
- `022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends.b1_nearness-reversal-more-coins.g3_downtrend-bounces-fade` (from F4, F7): In a coin whose 20-day return is negative, the larger its 5-day return relative to its 20-day volatility, the larger its fall over the next 5 days.
- `022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends.b1_nearness-reversal-more-coins.g4_quiet-downtrends-keep-falling` (from F5): In a coin whose 20-day return is negative, the lower its 20-day volatility is relative to its 60-day volatility, the larger its fall over the next 5 days.
- `022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends.b1_nearness-reversal-more-coins.g5_nearness-power-reversal-every-regime` (from F6): For a coin's nearness to its 90-day high, the larger the product of that signal's excess past 365-day power for 5-day returns and today's deviation of nearness from its 365-day level, when it implies a rise, the larger the coin's fall over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
