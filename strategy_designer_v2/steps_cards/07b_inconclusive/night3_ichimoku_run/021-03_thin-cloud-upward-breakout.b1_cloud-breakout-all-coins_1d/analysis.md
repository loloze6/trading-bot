---
line: 7.b inconclusive
backtest: 021-03_thin-cloud-upward-breakout.b1_cloud-breakout-all-coins_1d
idea tested: 021-03_thin-cloud-upward-breakout.b1_cloud-breakout-all-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4471 USD
---
## Findings
- **F1:** The tested result points the way the idea predicts but falls short of the bar. On 285 cases (142 thin, 143 thick), thin-cloud crosses beat thick ones by +7.1 % over 26 days (+5.8 % against −1.3 %, Welch t 1.59), with a Mann-Whitney p of 0.045 and a Spearman correlation between thinness and the unusual move of only 0.11. All 19 coins and all four folds were already used, so no more daily data is available.
- **F2:** The effect is not graded across thinness. It comes from the thickest fifth of clouds doing badly: that quintile's unusual 26-day move is −7.2 % with 28 % of cases up. The other four quintiles sit at +0.8 %, +6.4 %, +7.2 % and +4.0 %, so the thinnest fifth does not beat the middle.
- **F3:** The effect is drowned in large, skewed moves. The standard deviation of the 26-day unusual move is 0.42 for thin cases and 0.33 for thick ones. Both medians are negative (−1.6 % and −5.9 %). The all-case mean is +2.2 % with t 1.0, against a coin's usual 26-day move of about 30 %.
- **F4:** One year carries most of the difference. In 2024 thin cases gained +23.2 % (44 cases) against thick cases' −11.8 % (19 cases). Elsewhere the gap is small or reversed: in 2023 thin +0.5 % against thick +6.9 % (21 and 38 cases), in 2025 thin −11.4 % against thick −11.1 %, and in 2020 thin +27.1 % against thick +27.4 %.
- **F5:** The thin-versus-thick gap appears only after a strong rise into the cross. In the top third of the 26-day return before the signal, thin crosses gained +7.1 % (22 cases) while thick crosses lost −10.8 % (45 cases). In the lower two thirds, thick crosses did better than thin ones (+14.6 % against +7.0 %, and +11.7 % against +5.4 %).
- **F6:** The gap grows with the horizon but never becomes clear. Measured from 5, 10, 26 and 52 days, the thin-minus-thick Welch t is 0.21, 1.32, 1.59 and 1.72, and the Spearman correlation is −0.03, 0.07, 0.11 and 0.17. A longer horizon alone does not settle the idea.
- **F7:** Size is not the obstacle. Per case the unusual move is +2.32 % (strength 0.081) and the total move +7.91 %, which is 10.4 and 35.4 times the 0.22 % cost of a trade. The book had a Sharpe of 0.98 and failed only on Calmar (0.60).

## Ideas
- `021-03_thin-cloud-upward-breakout.b1_cloud-breakout-all-coins.b1_thin-cloud-after-strong-run` (from F1, F2, F5): After a daily close that crosses up from below a coin's Ichimoku cloud to above it, only while the coin has risen strongly over the past 26 days, the coin rises over the next 26 days, and the thinner the cloud at the cross (its width relative to price), the larger the rise.
- `021-03_thin-cloud-upward-breakout.b1_cloud-breakout-all-coins.b2_exhausted-thick-cloud-breakout` (from F2, F5, F3): After a daily close that crosses up from below a coin's Ichimoku cloud to above it through a thick cloud, the coin falls over the next 26 days, and the larger its 26-day return into the cross, the larger the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
