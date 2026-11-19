---
line: 7.b inconclusive
backtest: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation_1h
idea tested: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3156 USD
---
## Findings
- **F1:** The main measure is clearly on the side the idea predicts: the pooled slope of the 240-bar excess return on the forecast is 0.00280 with t 4.74 over 1,674 grid cases. The same positive slope holds at 24, 120, 480 and 720 bars (t 2.54, 3.72, 3.96 and 4.22), so the horizon is not the issue.
- **F2:** The effect is graded. Among the 821 positive-forecast cases, the mean 240-bar excess return rises steadily across forecast quartiles, from -0.0101 to 0.0026, 0.0131 and 0.0391 (about 205 cases each). The positive-only slope is 0.0036 (t 3.59).
- **F3:** The result is unclear only because the regime split is too weak to separate. On all grid bars the slope is 0.00336 (t 3.83, n 841) in `trending` and 0.00143 (t 1.56, n 833) in `unknown`. On positive-forecast bars it is 0.0039 (t 2.95, n 574) against 0.0024 (t 1.75, n 247). The difference therefore leans the predicted way, but its Welch t is only 1.53, with just 247 positive cases in `unknown`.
- **F4:** The effect is mixed across coins and periods, which lowers its power on six coins. Per-coin slopes run from 0.0004–0.0005 (t 0.37–0.42) for XMR and LTC up to 0.0060 (t 3.30) for XRP. By year, 2023 runs strongly the other way (slope -0.0043, t -3.89) and 2018 and 2022 are negative, against t 2.6–3.8 in 2019, 2020 and 2025.
- **F5:** The book's loss comes from trading costs, not from the signal. Gross daily return is 0.00077 (t 3.10), of which 0.00035 is the market's own rise. Fees are 0.00218 a day on a daily turnover of 1.99, which turns the book to a mean of -0.00144 a day (Sharpe -2.07).

## Ideas
- `001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation.b1_rsi-continuation-wider-coin-set` (from F1, F2, F3, F4): The higher a coin's 14-day RSI stands above 50, the more its price rises above its usual move over the next 10 days, most strongly while its 60-day return is positive.
- `001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation.b2_graded-high-rsi-continuation` (from F1, F2, F5): The higher a coin's 14-day RSI stands above 50, the more its price rises above its usual move over the next 10 days, and the larger that excess rise is the further RSI stands above 50.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
