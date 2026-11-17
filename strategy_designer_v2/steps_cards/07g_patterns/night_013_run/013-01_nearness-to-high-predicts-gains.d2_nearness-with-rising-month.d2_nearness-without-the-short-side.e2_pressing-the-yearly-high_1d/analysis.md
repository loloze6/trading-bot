---
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e2_pressing-the-yearly-high_1d
idea tested: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e2_pressing-the-yearly-high
step 5: mismatch
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.4995 USD
---
## Findings
- **F1:** The 3-day return after a sharp one-day fall rises with the fall's size measured against the coin's own volatility. On the non-overlapping 3-day grid, a daily return below −2 of its trailing 30-day standard deviation is followed by +1.60% over holding (t 2.37, n 124). A return between −2 and −1 standard deviations is followed by +0.87% (t 1.47, n 337). A return between −1 and 0 is followed by −0.06% (n 1423). On all days the same ordering holds: +2.19% (t 4.04, n 370), then +0.71% (t 2.85, n 1389), then +0.24% after ordinary days.
- **F2:** That rebound after falls beyond 1 standard deviation is carried by the smaller coins. It is +1.12% to +2.26% in LTC, XMR, XRP and ZEC (71 to 82 cases each) and slightly negative in BTC (−0.39%) and ETH (−0.69%). It is positive in 5 of 8 years, with 2021 the largest at +6.01%.
- **F3:** Saturdays are the strongest weekday for the coins: +0.44% mean daily return, t 5.39 over 2416 coin-days, against −0.18% to +0.32% on the other days. Saturday minus the other days is positive in all six coins, though only LTC is significant on its own (t 2.67). It is positive in 7 of 8 years.
- **F4:** The tested forecast does not sort the 7-day return in a graded way. Its forecast quintiles give excess returns of +0.43%, −2.07% (t −3.43), +0.50%, +0.25% and +0.89% (t 1.16, n 477) for the top. The raw distance-from-high quintiles are flat until the top one, which reaches +1.49% (t 1.87).
- **F5:** The book earned far less than the coins in the rising years. In 2020 it made 0.030% a day against 0.423% for holding, and in 2021 0.012% against 0.409%, which matches its Sharpe trailing holding's by 0.058. It beat holding mainly in falling years: 2018 at +0.043% against −0.353%, and 2022 at +0.011% against −0.180%.
- **F6:** A close at or above its 30-day high on heavier than usual volume was followed by +2.76% over 7 days (t 2.49, n 229). The same breakout on light volume was followed by −0.11% (n 108; Welch t 1.84). This volume effect is not graded: inside closes near the 30-day high, the Spearman correlation between volume ratio and the 7-day excess return is −0.02 (n 405). Given the many angles looked at, it does not stand out as a finding to act on.
- **F7:** Strength alone did not follow through. Daily moves above 2 standard deviations were followed by only +0.49% over 3 days (t 0.86, n 473), against +2.19% after falls of the same size.

## Ideas
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e2_pressing-the-yearly-high.g1_rebound-after-scaled-sell-offs` (from F1, F2, F7): The larger a coin's one-day fall measured in units of its own 30-day daily volatility, the larger its rebound over the next 3 days.
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e2_pressing-the-yearly-high.g2_nearness-to-high-finer-bars` (from F4): The nearer a coin's daily close sits to its highest close of the past 52 weeks, the higher its return over the next 7 days, with the effect concentrated in the closes closest to that high.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
