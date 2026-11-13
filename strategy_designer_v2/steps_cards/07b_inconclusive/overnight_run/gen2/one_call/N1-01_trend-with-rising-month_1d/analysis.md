---
line: 7.b inconclusive
backtest: N1-01_trend-with-rising-month_1d
idea tested: N1-01_trend-with-rising-month
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.4597 USD
---
## Findings
- **F1:** The positive mean is carried by a few outliers. Over the 251 non-overlapping active 20-bar cases, the mean excess return is +0.015 (t 0.63), but the median is −0.038 and only 43.4% of cases are positive. The skew is 7.3, the 5 best cases sum to 8.37 against a total of 3.77, and the 5%-trimmed mean is −0.015.
- **F2:** Measured against the six-coin average 20-bar return at the same moment, active cases show no edge: mean +0.0003, t 0.01, n 251, hit 47%. The active coin's forward return has a correlation of 0.54 with that market average, so the market's own moves account for much of what the test measured.
- **F3:** The effect sits in BTC only. BTC's active cases have a mean 20-bar log excess of +0.039 (t 1.86, n 50, hit 56%), and their median beats the market average (+0.015, hit 62%). XMR (−0.025, t −0.92, n 41), XRP (−0.047, t −0.86, n 36, hit 28%) and LTC (−0.014) are negative. ZEC's +0.13 arithmetic mean rests on a median of −0.023.
- **F4:** When BTC itself is not in the trending state, altcoins in the trending state lag their own average by −0.110 in 20-bar log excess (t −3.09, n 57, hit 37%). When BTC is also trending, the figure is +0.0005 (t 0.02, n 144).
- **F5:** Larger forecasts do not lift the typical case. The top forecast tercile has a mean of +0.051 but a median of −0.039 and a hit rate of 34.5% (n 84), against a 50% hit rate in the low tercile. Terciles of 200-day distance and of 20-bar momentum show no ordering either (t between −0.8 and 0.9).
- **F6:** Regime age matters slightly. Cases 1–10 bars into the trending regime average −0.014 (t −0.76, n 147), while those 11–40 bars in average +0.033 (t 1.10, n 94).
- **F7:** The effect varies strongly by year. The 2018 active cases average −0.176 (t −2.72, n 10) and 2022 averages −0.099 (n 6), while 2021 averages +0.046 (n 45) and 2024 +0.027 (n 46). No year reaches t 2 on the positive side.

## Ideas
- `N1-01_trend-with-rising-month.b1_btc-trend-above-rising-average` (from F3, F2, F1): On BTC, when the daily close is above its 200-day average and above its close of 20 bars earlier, BTC's return over the next 20 bars exceeds its own average 20-bar return.
- `N1-01_trend-with-rising-month.b2_established-trend-keeps-rising` (from F6, F1): When a coin has been in the trending state (close above its 200-day average and above its close of 20 bars earlier) for 11 to 40 consecutive bars, its next 20-bar return exceeds its own average 20-bar return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
