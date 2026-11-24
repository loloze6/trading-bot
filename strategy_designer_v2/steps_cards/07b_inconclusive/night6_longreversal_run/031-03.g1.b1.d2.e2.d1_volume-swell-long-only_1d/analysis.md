---
line: 7.b inconclusive
backtest: 031-03.g1.b1.d2.e2.d1_volume-swell-long-only_1d
idea tested: 031-03.g1.b1.d2.e2.d1_volume-swell-long-only
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4014 USD
---
## Findings
- **F1:** The tested result points the way the idea predicts but falls short of the bar: the forecast-weighted mean 14-day excess return is +2.61 % with t 1.43 (1145 positive-forecast grid cases on 182 days, slope +0.0018). The test already used all 19 coins on every fold, so no further data can raise its t.
- **F2:** The effect sits almost entirely in coins trading above their 30-day mean close. There the weighted excess is +5.93 % (t 1.83, 428 cases on 87 days, strength 0.24). Below that mean it is +1.20 % (t 0.53, 320 cases on 74 days, strength 0.04). The 60-day mean splits the same way: +5.06 % (t 1.22) above against +1.28 % (t 0.38) below.
- **F3:** The same split shows on the coin's recent direction. After a 7-day rise the weighted excess is +4.36 % (t 1.70, 591 cases); after a 7-day fall it is −0.43 % (t −0.21, 451 cases). After a 14-day rise it is +3.81 % (t 1.54, 602 cases); after a 14-day fall it is +0.23 % (t 0.11, 439 cases).
- **F4:** The yearly results are mixed and follow the market, which drowns the pooled result:
- **F5:** The grading is weak at its low end. The lowest quarter of positive forecasts loses −2.63 % (t −1.36, 287 cases), while the second to fourth quarters gain +2.20 %, +3.86 % and +2.47 %.
- **F6:** The plan's 14-day horizon is where the effect is largest. At 7 days the weighted excess is +0.67 % (t 0.84, 2447 cases); at 28 days it is +2.89 % (t 0.63, 564 cases), with an unweighted unusual move of only +0.45 %.
- **F7:** No coin reaches t 2 on its own:
- **F8:** Grid cells with no swell (forecast 0) average −1.59 % excess (t −1.31, 1303 cases on 186 days). This sits on the opposite side of the swell cases, which is consistent with the effect being real but small.

## Ideas
- `031-03.g1.b1.d2.e2.d1.b1_volume-swell-above-trend` (from F1, F2, F3, F4): The more a coin's mean daily volume over the last 14 days sits above its mean daily volume over the last 30 days, the more its price rises over the next 14 days, on the long side only, only while its price sits above its mean close of the last 30 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
