---
line: 7.d not profitable
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g1_short-high-break-on-volume_1d
idea tested: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g1_short-high-break-on-volume
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3196 USD
---
## Findings
- **F1:** The book's whole gain comes from its long side. Long bars summed +6.32 in gain before fees against 1.13 in fees. Short bars summed −0.36 before fees and paid another 0.79 in fees, so after fees the shorts are a net loss of about 1.14 over 8,517 bars.
- **F2:** Removing the shorts repairs the failing Calmar but not the mean. A long-only version of the same book has mean daily return 0.000296 against 0.000229, Sharpe 1.02 against 0.61, deepest fall −13.3% against −19.8%, and Calmar 0.81 against 0.39 (the rule needs 0.75).
- **F3:** The lowest forecast quintile does not lead to falling coins. It sits 1.07% below the coin's 7-day mean, yet its raw 7-day return is −0.14%, and the bars held short rose on average (+0.0068% a day). The deep-below, thin-volume side forecasts relative weakness, not an absolute fall.
- **F4:** Only the top forecast quintile carries real gains: +1.84% in 7-day excess return (+2.75% raw), with 0.155% daily gain per bar. The next quintile earns 0.026% a day and the lower three about 0 or negative.
- **F5:** Shorts lose most where the coin trends hardest. In the top 60-day-return quartile (+79% on average) shorts lose −0.029% a day, and in the bottom quartile (−36%) they lose −0.021% a day. Shorts gain only in the mildly falling quartile (+0.062%).
- **F6:** The graded relation is stronger when the coin is rising over 60 days, and so are the long gains:

## Ideas
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g1_short-high-break-on-volume.d1_near-high-volume-in-uptrends` (from F1, F2, F4, F6): The closer a coin's daily close sits to its highest close of the past 20 days, and the heavier that day's volume against its 30-day average, the higher the coin's return over the next 7 days, only while the coin's own 60-day return is positive, the gain growing with both closeness and volume inside that rising state.
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g1_short-high-break-on-volume.d2_near-high-is-long-only` (from F1, F2, F3, F5): The closer a coin's daily close sits to its highest close of the past 20 days, and the heavier that day's volume against its 30-day average, the larger the coin's rise over the next 7 days, the move being an absolute gain that grows with closeness and volume, while closes far below the high on thin volume are followed by smaller rises rather than falls.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
