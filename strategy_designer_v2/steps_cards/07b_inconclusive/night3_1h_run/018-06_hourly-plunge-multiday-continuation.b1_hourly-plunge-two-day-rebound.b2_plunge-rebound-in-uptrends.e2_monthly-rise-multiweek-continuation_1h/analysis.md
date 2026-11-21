---
line: 7.b inconclusive
backtest: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation_1h
idea tested: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3432 USD
---
## Findings
- **F1:** The main measure is on the side the idea predicts but rests on a handful of cases: the forecast-weighted mean excess 336-bar return is +2.41 % at t 1.77 over 568 cells, yet without the 10 largest contributions the weighted sum falls from 142.05 to −0.17, the median excess is −2.09 %, only 43.3 % of cells beat the coin's drift (Wilcoxon p 0.17), the 2 %-winsorised weighted mean is +1.28 % at t 1.53, and the 5 %-trimmed mean excess is −0.77 %.
- **F2:** Those 10 largest cells come mostly from two coins and the latest years: 8 of the 10 are ZEC and XRP, carrying 12.2 of the 13.7 summed contribution, with mean excess returns of +112 % and +85 %, and 6 of the 10 fall in 2024–2025.
- **F3:** The effect changes sign with the period. It is positive in 2020 (+5.5 %, t 2.75, 93 cells), 2021 (+6.0 %, t 2.12, 84) and 2024 (+5.3 %, t 1.88, 82). It is negative in 2018 (−13.1 %, t −3.44, 42) and 2022 (−4.8 %, t −1.48, 42). By fold it runs from A at −2.4 % (t −1.81, 121 cells) to D at +7.8 % (t 1.86, 148).
- **F4:** The effect is mixed across coins: ZEC +10.2 % (t 1.50, 91 cells), ETH +2.7 % (t 1.26), LTC +2.3 % (t 1.12) and BTC +1.4 % (t 0.99) are positive, while XMR −0.7 % (t −0.47) and XRP −1.1 % (t −0.37) are negative. No coin reaches t 2 on its own roughly 90–106 cells.
- **F5:** The effect is clearest at a shorter horizon than the plan's: over 168 bars (7 days) the weighted mean excess is +1.19 % at t 2.19 over 1,196 independent cells. Over 336 bars it is +2.41 % at t 1.77 over 568 cells, and over 672 bars +2.23 % at t 0.62 over 276 cells.
- **F6:** The grading shows on the standardised rise but not on the raw one. The slope of excess on forecast has t 2.62, and forecast quartiles go from −4.07 % (q1) to +4.18 % (q4). But raw 30-day-return quintiles over all cells are flat, from −0.14 % (lowest) to −0.17 % (highest, mean 30-day return +53 %). Cells with zero forecast average −0.77 % (t −1.01, 580 cells).
- **F7:** The effect sits where the coin's shorter rise agrees with its longer trend:
- **F8:** The size is above the cost but small next to the noise. The unusual move is +0.75 % per case (strength 0.029, about half the 0.05 of F10 in the prior findings), 3.9 times the 0.19 % round trip; the total move is +2.77 %, 14.4 times the cost. The book beat holding (Sharpe 1.07, 0.52 above holding's) with 0.13 trades a day.

## Ideas
- `018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.b1_monthly-rise-on-more-coins` (from F1, F2, F4, F8): A coin whose 30-day return is positive keeps rising over the next 2 weeks by more than its usual 2-week drift, and the larger its 30-day return, the larger that rise.
- `018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.b2_monthly-rise-one-week-continuation` (from F5, F6, F8): A coin whose 30-day return is positive keeps rising over the next 7 days by more than its usual 7-day drift, and the larger its 30-day return, the larger that rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
