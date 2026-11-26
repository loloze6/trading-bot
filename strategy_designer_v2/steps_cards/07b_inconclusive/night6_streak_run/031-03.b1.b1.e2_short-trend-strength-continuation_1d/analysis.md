---
line: 7.b inconclusive
backtest: 031-03.b1.b1.e2_short-trend-strength-continuation_1d
idea tested: 031-03.b1.b1.e2_short-trend-strength-continuation
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4113 USD
---
## Findings
- **F1:** The test's result is on the side the idea predicts but just short of the bar: the slope's t is 1.98 with day-clustered errors on 3587 grid bars. My own rebuild gives a clustered t of 1.82 on the forecast and 1.98 on the raw volatility-scaled 10-day rise (2399 grid bars, 325 days). The test already used all 19 coins and all four folds on daily bars, so no more data is available.
- **F2:** At the plan's 5-day horizon the effect sits only in the strongest rises. In the top fifth of the forecast (mean 19.96, at its cap of 20) the excess return is +2.23 % (t 3.0, 718 bars). The four lower fifths are all slightly negative (−0.17 %, −0.35 %, −0.59 %, −0.33 %, all |t| < 1.4). That is why the cases (every forecast rise of at least 2 points) show an unusual move of −0.01 % (t −0.01, 1179 days) and the supporting check fails.
- **F3:** The same continuation is clearer over 10 days than over 5. On positive forecasts the 10-day slope has a day-clustered t of 2.35 (1154 grid bars, 157 days), OLS t 4.44. On the raw scaled rise the clustered t is 2.29. The excess return is +1.35 % on average and +5.16 % in the top fifth (t 3.68).
- **F4:** Over 10 days, splitting the positive scaled rises into sixths:
- **F5:** The effect fades beyond 10 days. At 20 days the slope's OLS t is 1.05 and the top fifth's excess return is −1.94 %. At 1 and 3 days the OLS t's are 4.7 and 5.2 but the excess is small (+0.29 % and +1.39 % in the top fifth).
- **F6:** The effect is mixed across periods and coins.
- **F7:** The forecast's cap compresses the signal. The whole top fifth of the 5-day sample sits at a forecast of about 20, so the grading the idea claims is flattened exactly where the effect shows (F2).

## Ideas
- `031-03.b1.b1.e2.b1_scaled-rise-ten-day-continuation` (from F1, F3, F4, F5): The larger a coin's positive 10-day return relative to its own daily volatility over the past 60 days, the more it keeps rising over the next 10 days beyond its normal drift.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
