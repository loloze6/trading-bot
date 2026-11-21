---
line: 7.b inconclusive
backtest: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high.b2_surge-in-rising-month_1h
idea tested: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high.b2_surge-in-rising-month
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3431 USD
---
## Findings
- **F1:** The tested effect points the way the idea predicts but is small and noisy. Over 1,156 cases with 240-hour returns, the mean excess 10-day return after a surge is +0.53 % (t 1.04), with a strength of 0.031 of a usual move. Step 5's own measure is +0.58 % (t 1.15, 1,148 cases). This is below the 0.05 typical of real ideas, and only 46 % of cases end above the coin's drift.
- **F2:** Most of the effect sits in the largest surges. The 359 cases where the forecast is at its cap of 20 gain +2.2 % over 10 days beyond drift (t 2.13). The 797 cases below the cap gain −0.2 % (t −0.40). By forecast quartile the excess climbs from −0.65 % to −0.40 %, +0.83 % and +2.38 % (t 1.91 in the top quartile).
- **F3:** The effect also sits in surges that end near the 30-day high. Cases within about 1 % of the 30-day high (top quartile, median 1.0 % below it) gain +4.6 % over 10 days beyond drift (t 2.86, 214 cases). The other three quartiles gain −0.1 %, −1.9 % and +0.9 %.
- **F4:** Market years drown the effect. Over 10 days the mean excess is −6.8 % in 2018 (t −3.07, 98 cases) and −3.2 % in 2022 (t −2.81, 125 cases). It is +3.1 % in 2020 (t 2.47), +4.2 % in 2021 (t 2.22) and +2.5 % in 2024 (t 2.01). Even the largest surges lose −4.3 % in 2022.
- **F5:** The effect is spread thinly across coins, which points to too little data rather than one coin carrying it. Five of the six coins are positive over 10 days (+0.3 % to +1.4 %, every t below 1.1), XMR is −1.1 % (t −1.27), and no coin reaches t 2 alone. The test used only 6 of the 19 coins available on hourly bars.
- **F6:** The move peaks before the plan's horizon. The excess is +0.63 % at 5 days (t 1.90, strength 0.057), +0.53 % at 10 days (t 1.04) and +1.2 % at 20 days (t 1.42). The 10-day horizon is not where the move is clearest.
- **F7:** The move is not too small to pay, but the book's falls are deep. The unusual move per case is 3.0 times the 0.19 % cost of a round trip, and the total move is 10.1 times it. The book's Sharpe is 0.82, above holding by 0.27, but it fails on Calmar (0.62), consistent with the losing years in F4.

## Ideas
- `018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high.b2_surge-in-rising-month.b1_hourly-surge-more-coins` (from F1, F5, F7): When a coin's 24-hour return, read at an hourly close, first reaches several times its 30-day average absolute daily return on the upside, the price keeps rising over the next 10 days by more than the coin's usual 10-day return, only while the coin's 30-day return is positive: the larger the surge in usual daily moves, the larger the rise.
- `018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high.b2_surge-in-rising-month.b2_surge-at-monthly-high` (from F2, F3, F7): When a coin's 24-hour return, read at an hourly close, first reaches several times its 30-day average absolute daily return on the upside, the price keeps rising over the next 10 days by more than the coin's usual 10-day return, only while that close is near the coin's 30-day high: the nearer the close to the 30-day high and the larger the surge in usual daily moves, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
