---
line: 7.b inconclusive
backtest: 032-01.b1.b1_large-weekly-rise-continues_1d
idea tested: 032-01.b1.b1_large-weekly-rise-continues
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 1
cost: 0.2231 USD
---
## Findings
- **F1:** Step 5's main measure is on the side the idea predicts but just short of the bar: the mean unusual 7-day move of the long cases is +4.92 % with a day-clustered t of 1.94 over 103 cases on 63 days, and the slope on the forecast is positive (0.0042); its size is +2.24 % per case (t 1.72, 192 days), a strength of 0.152 of a usual 12.44 % move, which is 11.6 times the 0.19 % cost of a trade.
- **F2:** The effect is spread thinly and unevenly across the six coins: in folds B and C the 7-day long cases average +2.2 % (t 0.68, 65 cases, 36 days), carried by XRP (+13.4 %, 12 cases) and BTC (+3.9 %, 10 cases), while ETH (−0.1 %), LTC (−3.3 %), XMR (−1.3 %) and ZEC (−1.4 %) are near zero or below, each on only 8 to 15 cases.
- **F3:** Over all grid bars in folds B and C, the next 7-day unusual move rises steadily with the 7-day return counted in 30-day swings: −2.7 % for scaled moves of −2 to −1 (99 cases), −0.5 % for −1 to 0 (304), +0.2 % for 0 to 1 (279), +2.2 % for 1 to 2 (112), +4.9 % for 2 to 2.5 (24) and +9.5 % for 2.5 to 3 (14). Above 3 it is −1.6 % on 8 cases, and inside the rises of at least 2 the correlation of the scaled rise with the move is only −0.07, so the grading shows across the whole range and is too thin to see inside the tail alone.
- **F4:** The effect shows at short horizons and is gone by two weeks: on the forecast's cases the strength is 0.197 over 3 days (t 1.58, 118 cases), 0.118 over 7 days (t 0.68, 65 cases) and −0.076 over 14 days (t −0.62, 28 cases).
- **F5:** The result varies by period: the 7-day long cases average −1.8 % in 2018 (7 cases) and −6.6 % in 2019 (13 cases), against +7.5 % in 2020 (21 cases) and +3.5 % in 2021 (24 cases). Window w15 alone gives −11.4 % on 8 cases, so a few periods decide the sign at this sample size.
- **F6:** Among rises of at least 2 scaled units, the continuation is larger when the 30-day swing is high against its own recent level: +12.6 % (17 cases, t 1.41) in agitated periods against +1.7 % (17 cases, t 0.50) in calm ones. It is +5.8 % (t 1.93) in choppy periods against +4.6 % (t 0.62) in trending ones; the case counts are too small to rely on either split.

## Ideas
- `032-01.b1.b1.b1_large-weekly-rise-continues-more-coins` (from F1, F2, F5): When a coin's price has risen over the past 7 days by a large amount compared with its typical daily swing over the past 30 days, it tends to keep rising over the next 7 days. The larger that 7-day rise counted in 30-day daily swings, the larger the further rise.
- `032-01.b1.b1.b2_scaled-weekly-move-continues` (from F3, F4): The larger a coin's 7-day return counted in its 30-day typical daily swing, the larger its return in the same direction over the next 7 days, from large weekly falls through large weekly rises.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
