---
line: 7.b inconclusive
backtest: 021-03_thin-cloud-upward-breakout.d2_calm-breakout-lasts-longer_1d
idea tested: 021-03_thin-cloud-upward-breakout.d2_calm-breakout-lasts-longer
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3792 USD
---
## Findings
- **F1:** The rise after an upward cloud cross comes from a few large cases, not from a typical one. Over 151 cross bars with 40 days left, the mean drift-adjusted 40-day return is +8.7 % (t 1.81), but the median is −2.1 % and only 48 % end above the drift. The 5 largest cases make up 141 % of the summed standardised return, and without them the mean is −0.066 of a usual move. This is why step 5's weighted mean only just reaches t 2.04.
- **F2:** The grading the idea states, calmer crosses rising more, does appear in the plain 20-day volatility, but the test's forecast does not carry it. The Spearman correlation of the 20-day volatility at the cross with the 40-day drift-adjusted return is −0.27 (p 0.005, 151 cases), while that of the forecast is only +0.04 to +0.13 (p 0.63). The forecast compares today's volatility with its own 365-day mean, which is why step 5's calm-minus-violent split came out at −0.169, on the wrong side.
- **F3:** Within each coin, the gradient runs the predicted way but is too weak to show clearly. Ranked within each coin, the calm, middle and violent thirds of crosses end at +0.39, +0.24 and −0.14 of a usual 40-day move, with 56 %, 50 % and 29 % of cases above the drift. Calm minus violent is +0.21, but its Welch t is only 0.82 (53 against 53 cases). The pattern is also not shared by every coin: it holds in BTC, ETH, LTC and XRP, while XMR and ZEC run the other way.
- **F4:** The effect is strongest at a shorter horizon than the plan's 40 days. The mean drift-adjusted return after the cross is +1.9 % over 10 days (t 1.51, 190 cases), +5.8 % over 20 days (t 2.32, 181 cases), +8.7 % over 40 days (t 1.81, 151 cases) and +7.6 % over 60 days (t 0.82, 103 cases). Its t peaks at 20 days.
- **F5:** The effect is uneven across years, which explains the book's weak Calmar (0.62 against 0.75). All 6 cases in 2018 fell (mean −0.39, t −3.96), and 2022 averaged −0.04 with 35 % of cases up, against 2020 at +0.22 (t 3.38, 70 % up). Trading costs are not the problem: the unusual move per case is 57 times the 0.19 % round-trip cost.

## Ideas
- `021-03_thin-cloud-upward-breakout.d2_calm-breakout-lasts-longer.b1_calm-cloud-breakout-20-days` (from F2, F3, F4, F1): After a daily close that crosses up from below a coin's Ichimoku cloud to above it, the coin rises over the next 20 days, and the lower its 20-day realised volatility at the cross, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
