---
line: 7.e profitable but not proven
backtest: 032-02.g1_uptrend-near-high-continues_1d
idea tested: 032-02.g1_uptrend-near-high-continues
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3448 USD
---
## Findings
- **F1:** Most of the book's gain is timing rather than the market's own rise: per coin-bar the position earns 0.001244, of which 0.000420 (34 %) is the position times the coin's mean daily return and 0.000824 (66 %) is timing; nearly all of it comes on trending bars (gain 0.002352 per coin-bar at a mean allocation of 0.53, against 0.000096 on "unknown" bars).
- **F2:** The tested idea, measured on the raw percent distance below the 28-day closing high instead of the plan's forecast standardised over its own past 60 values, is strong at the plan's horizon in folds B and C: on the in-regime 5-day grid, the slope t of the excess return on closeness is 4.47 (638 cases), against 3.65 for the recorded forecast, whose correlation with raw closeness is only 0.86.
- **F3:** The effect is graded across the whole range and is two-sided around the middle: in-regime 5-day excess return by distance quintile runs +3.88 % at the high (mean distance 0.05 %), +1.36 %, +0.23 %, +0.34 %, then −2.98 % for the coins pulled back furthest (mean distance 24.6 %).
- **F4:** The effect peaks at a 5- to 10-day horizon: the in-regime closeness slope t is 1.16 at 1 day, 0.71 at 3 days, 4.47 at 5 days, 3.08 at 10 days and 0.13 at 20 days (128 cases at 20 days).
- **F5:** The effect lives in the 28-day uptrend, not in the size of the trend: on bars with a 28-day fall, closeness has t 0.60 (640 cases); inside the uptrend, the 28-day return itself predicts nothing or slightly the opposite (t −0.89 at 5 days, −2.01 at 1 day).
- **F6:** Closeness to the high works best when the day's range is wide: on in-regime cases whose high-low range is above its median relative to the coin's 28-day mean range, the closeness t is 4.46 (319 cases), against 1.93 (319 cases) on calm-range cases.
- **F7:** The gain is spread out but uneven over time and coins: no handful of trades carries it (1762 trades, top 10 at 15 % and top 20 at 26 % of the summed net P&L, win rate 46.8 %); the closeness t is 0.22 in 2018, 1.36 in 2019, 3.14 in 2020 and 2.28 in 2021; by coin it is 2.0 to 3.8 for BTC, ETH, XMR and XRP and 0.57 and 0.51 for LTC and ZEC; book timing is negative in windows w7, w9, w12 and w14.

## Ideas
- `032-02.g1.e1_raw-nearness-to-uptrend-high` (from F2, F3, F4, F5, F7): Among coins whose close is above its close of 28 days ago, the smaller the percent distance of today's close below its highest close of the last 28 days, the larger the coin's rise over the next 5 to 10 days, with closes that have pulled back furthest from that high falling behind.
- `032-02.g1.e2_wide-range-breakout-continuation` (from F6, F3, F5, F1): In a coin whose close is above its close of 28 days ago, a close near its 28-day highest close on a day whose high-low range is wide compared with its ranges of the last 28 days is followed by a rise over the next 5 days, larger the nearer the close is to that high.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
