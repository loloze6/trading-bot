---
line: 7.c rejected
backtest: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample_1d
idea tested: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample
step 5: rejected
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3478 USD
---
## Findings
- **F1:** The idea was rejected because the market did the opposite of the forecast: at the extreme high-RSI cases (forecast ≤ -5), the 5-bar return beat the coin's average by +0.0129 (t 2.26, 523 non-overlapping cases), and the 10-bar return beat it by +0.0318 (t 2.36, 254 cases); the verdict's own count was +0.0144 (t 2.58, 595 cases), with only 1 of 6 coins negative.
- **F2:** The effect grows with how strong the reading is: the most extreme quartile of short forecasts (mean forecast -17.6) beat the average by +0.0136 over 5 bars (t 2.08, n 355) and by +0.0346 over 10 bars (t 2.30, n 176); this falls through q2 (+0.0052 / +0.0231) to the mildest quartile (-0.0035 / -0.0075).
- **F3:** The coin's own 14-day return predicts continuation: over 5 bars the top two quintiles beat the average (q5 +0.0106, t 1.97; q4 +0.0080, t 2.01; about 597 cases each) while q2 lagged it (-0.0155, t -3.76), with Spearman rho 0.047 (p 0.010); over 10 bars rho was 0.053 (p 0.046), and q5 beat the average by +0.0221 (t 1.83).
- **F4:** Continuation is clearest inside a 60-day uptrend: with the 60-day return positive and RSI above 70, the 10-bar return beat the average by +0.060 (t 2.37, n 61), while with the 60-day return negative and RSI between 40 and 50 it lagged by -0.0239 (t -2.25, n 163).
- **F5:** Reversal after RSI above 70 held only in some years and one coin: the 5-bar excess was negative in 2018 (-0.097, n 4), 2019 (-0.034, t -2.17, n 28) and 2022 (-0.066, n 6), but positive in 2020 (+0.070, t 2.59, n 36); LTC was the only negative coin (-0.028, t -1.83, n 30).
- **F6:** The book lost because it was short into rising coins: it was short on 72% of bars with a mean position of -0.165, and its mean daily gain of -0.000684 splits into -0.000194 from the market's own rise and about -0.00049 from timing; timing was negative in 4 of 6 coins (BTC -0.00091, XRP -0.00113), giving a Sharpe of -1.256.
- **F7:** Across all readings, RSI level and the next return have almost no rank relation (5-bar Spearman rho 0.004, p 0.81), so the signal sits in the high tail and in the trend, not in a straight line through all RSI values.

## Ideas
- `001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation` (from F1, F2, F4, F6): The higher a coin's 14-day RSI stands above 50, the more its price rises above its usual move over the next 10 days, most strongly while its 60-day return is positive.
- `001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c2_two-week-momentum-continuation` (from F3, F1): The larger a coin's 14-day return, the more its price rises above its usual move over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
