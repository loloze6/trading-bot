---
line: 7.b inconclusive
backtest: 067-01.b1.b1_choppy-stretch-carries-both-ways_1d
idea tested: 067-01.b1.b1_choppy-stretch-carries-both-ways
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3860 USD
---
## Findings
- **F1:** The test missed because only one side carried. In folds B and C at the plan's 5 days, below-average closes kept falling: mean excess −2.68 % over 145 short cases. Above-average closes did not keep rising: −0.19 % over 142 long cases. Step 5's supporting check failed for the same reason, at −0.0053 on the long side, while the pooled slope was only t 0.91 (819 cases, 374 days).
- **F2:** On the short side the carry grows with the stretch. Short-case mean excess by quartile of raw stretch, smallest to largest, is −1.21 %, −1.21 %, −3.79 % and −4.93 %. On the long side three of the four quartiles of forecast size give negative signed excess (−1.37 %, −1.85 %, −1.62 %; t −0.98 to −1.09), and only the largest gives +2.37 % (t 1.20).
- **F3:** The effect sits on the predicted side and is stronger at 5 days than at other horizons. Signed excess is t 1.05 at 1 day, 0.84 at 3, 2.05 at 5, 1.58 at 10 and −0.72 at 20. The slope is t 2.87 at 5 days on 287 cases, with a strength of 0.10. Over all four folds it is still too small to show: +0.24 % per case, t 0.78, strength 0.018.
- **F4:** The effect is uneven across periods and coins, which dilutes the pooled test. In 2020 signed excess is +2.80 % (t 2.31, slope t 2.80), while 2018 and 2019 are near zero (t 0.40 and 0.08). Windows w16 (t 3.63) and w18 (t 2.58) carry most of it. ETH and LTC are slightly negative (t −0.15 and −0.25), while XRP is the strongest coin (slope t 2.90).
- **F5:** The effect is missing when the coin is swinging least. In the lowest third of 20-day swing, signed 5-day excess is −0.36 % (t −0.45). In the middle third it is +2.86 % (t 2.91) and in the top third +2.55 % (t 1.81).
- **F6:** The book cannot pay on the effect at its full-sample size. The total move per case is +0.23 % against a 0.19 % round-trip cost, 1.2 times the cost. Step 6 found a Sharpe of 0.23 and a Calmar of 0.07, and the book trailed holding by 0.32 in Sharpe.

## Ideas
- `067-01.b1.b1.b1_choppy-downside-stretch-keeps-falling` (from F1, F2, F3): In a choppy market, the further a coin's close stands below its 20-day average, measured in units of its 20-day standard deviation of daily returns, the more the coin keeps falling over the next 5 days.
- `067-01.b1.b1.b2_choppy-stretch-carry-all-coins` (from F3, F4): In a choppy market, the further a coin's close stands from its 20-day average, measured in units of its 20-day standard deviation of daily returns, the more the coin keeps moving the same way over the next 5 days, rising after closes above the average and falling after closes below it.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
