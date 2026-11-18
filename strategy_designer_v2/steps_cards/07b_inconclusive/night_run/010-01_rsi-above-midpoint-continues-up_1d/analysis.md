---
line: 7.b inconclusive
backtest: 010-01_rsi-above-midpoint-continues-up_1d
idea tested: 010-01_rsi-above-midpoint-continues-up
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.1568 USD
---
## Findings
- **F1:** The tested slope is on the side the idea predicts but short of the bar: 7-day slope 0.000629, t 1.82 on 815 independent cases. Only BTC and ETH ran (BNB is absent), so the test had about two thirds of the roughly 1,200 cases its plan expected.
- **F2:** The sign holds at every horizon, but only the shorter ones clear the bar: t 2.65 at 1 day (5,794 cases), 2.48 at 3 days (1,907), 1.82 at 7 days (815), 1.03 at 14 days (384) and 1.97 at 21 days (240). As cases thin out at longer horizons, the t falls, which fits a small effect that this data is too short to show.
- **F3:** Both coins point the same way at 7 days, each too weak alone: BTC slope 0.000379, t 0.90 (408 cases); ETH slope 0.000882, t 1.61 (407 cases).
- **F4:** The effect is mixed across years. Only 2025 is strong (slope 0.00173, t 2.87, 102 cases); 2020 and 2021 are mildly positive (t 0.59 and 0.52), while 2018, 2019, 2022, 2023 and 2024 are negative (t between -0.98 and -0.06). Part of the pooled slope may come from bull years carrying both high forecasts and high returns.
- **F5:** The 7-day forecast quintiles are not monotone. The lowest quintile has the weakest return (-0.0121, t -1.38) and the fourth the strongest (+0.0111, t 1.13), but the top quintile drops back to +0.0041 (t 0.53). The long side alone has a slope of t 1.33 (396 cases) and the short side t 1.10 (391 cases).
- **F6:** The bar-level gain before costs comes from the long side: long bars average 0.00194 (2,801 bars), short bars 0.00007 (2,784 bars).

## Ideas
- `010-01_rsi-above-midpoint-continues-up.b1_rsi-share-more-coins` (from F1, F2, F3): The larger the share of the past 14 days that a coin's 14-day RSI has spent above its midpoint, the larger the coin's rise over the next 7 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
