---
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma_1d
idea tested: 002-03_price-cross-above-long-sma
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3135 USD
---
## Findings
- **F1:** The main measure leans the way the idea predicts but falls short of the bar: block mean +0.126 with t 1.73 over 811 non-overlapping 20-bar blocks (502 with a position), and 8 of 24 windows have a positive block mean (t across windows 0.88).
- **F2:** The positive mean rests on a few very large blocks rather than a steady drift: the block sums have median 0 and skew 7.6, the top 10 blocks sum to 132.7 against 102.4 for all 811, and without those 10 the block mean is -0.038 (t -0.92).
- **F3:** The typical case does not beat holding the coin: on the 399 active 20-day grid bars the median excess is -0.036 and only 40.6% beat the coin's mean, against an active-bar mean excess of +0.0052.
- **F4:** The edge over the coin's own drift is barely there and barely graded. Active bars beat flat bars by only +0.0053 over 20 days (Welch t 0.27). The rank correlation of forecast with 20-day excess on active bars is just 0.04. Only the strongest forecast bucket (15-20) is clearly positive, at +0.055 (t 1.17, n 113), while the 0-5 bucket is -0.029 (t -1.63, n 111).
- **F5:** The result swings with the market regime. Active 20-day excess is -0.132 (t -2.76, n 21) in 2018 and -0.173 (t -3.12, n 10) in 2022, and about +0.02 to +0.04 in 2020, 2021, 2024 and 2025. Across coins it ranges from -0.022 (XRP) to +0.059 (ZEC), and no coin reaches |t| 0.7.
- **F6:** Fresh crosses do not start the move. Bars within 20 days of the forecast turning positive show -0.021 excess (t -1.21, n 162), against +0.026 (n 151) at 21-60 days and +0.017 (n 86) at 61-120 days.

## Ideas
- `002-03_price-cross-above-long-sma.b1_price-above-sma-more-coins` (from F1, F2, F5): After a coin's close crosses above its long moving average, the price keeps rising over the following bars more often and further than after random bars.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
