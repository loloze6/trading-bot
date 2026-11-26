---
line: 7.g patterns
backtest: 032-02.b1.e1.e1.e1.e1_marginal-breakouts-keep-rising_1d
idea tested: 032-02.b1.e1.e1.e1.e1_marginal-breakouts-keep-rising
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3859 USD
---
## Findings
- **F1:** Across all bars on the non-overlapping 20-day grid (folds B, C), the closer a coin's close sits to its prior 60-day closing high, the larger its excess 20-day return. The per-coin quintile nearest the high (mean distance −4.75 %) gained +15.6 % above drift (t 3.31, 42 cases), while the middle quintile (mean distance −23.8 %) gave −10.75 % (t −3.71, 42 cases). Spearman of distance against excess return is 0.188 (p 0.008, 198 cases), and 0.222 (p 0.0017) with distance scaled by 60-day volatility.
- **F2:** The near-high effect holds in every slice we could cut. The top distance quintile beat the rest in all six coins (BTC +6.2 % vs −1.8 %, ETH +6.8 % vs −3.2 %, LTC +17.6 % vs −4.4 %, XMR +12.2 % vs −4.2 %, XRP +40.1 % vs −6.4 %, ZEC +10.9 % vs −4.5 %). It also beat the rest in every year that has top-quintile cases (2019 +10.2 % vs −11.0 %, 2020 +17.0 % vs +5.8 %, 2021 +17.4 % vs +7.7 %).
- **F3:** Most of that gain lies below the old high, not in true breakouts. On fixed bins of distance, closes 3–8 % under the 60-day high gained +16.0 % above drift over 20 days (t 2.89, 20 cases) and closes 0–3 % under gained +11.6 % (t 1.75, 7 cases). Closes above the high (the tested idea's only situation) gained +13.2 % (t 1.20, 7 cases).
- **F4:** The day after a fall larger than twice the coin's 60-day daily standard deviation, the coin rose +2.08 % on average (t 3.21, 102 cases). After falls of 1–2 standard deviations it rose +0.50 % (t 1.84, 320 cases), and after moves within ±1 it returned −0.04 % (2734 cases), so the bounce is graded. It is positive in 2019 (+2.08 %), 2020 (+5.41 %) and 2021 (+1.38 %), but only +0.04 % in 2018.
- **F5:** Up days larger than two standard deviations were followed by +4.09 % over 5 days (t 3.06, 136 cases), but this is not graded. Spearman of the up-move size against the 5-day return over all up days is 0.014 (p 0.55, 1844 cases), and the effect was +0.07 % in 2018, so it is not a finding to build on.
- **F6:** The book's trades do not scale with the forecast as the idea claims. The highest entry-forecast tercile (smallest margin) earned +21.0 % per trade net, against +13.4 % for the lowest tercile and +11.5 % for the middle, so the margin's ordering adds no graded edge. The weekday pattern (Sunday +0.41 %, t 2.40, one of seven days) does not stand out given the number of angles looked at.

## Ideas
- `032-02.b1.e1.e1.e1.e1.g1_nearness-to-60-day-high` (from F1, F2, F3): The closer a coin's daily close is to its highest close of the prior 60 days, the larger the coin's rise over the next 20 days, with closes just under the old high rising about as much as closes just over it.
- `032-02.b1.e1.e1.e1.e1.g2_next-day-bounce-after-big-falls` (from F4): The larger a coin's one-day fall relative to its usual daily move over the past 60 days, the larger its rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
