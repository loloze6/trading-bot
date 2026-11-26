---
line: 7.b inconclusive
backtest: 034-01_rising-nearness-to-high-rises_1d
idea tested: 034-01_rising-nearness-to-high-rises
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3468 USD
---
## Findings
- **F1:** Step 5's result points the way the idea predicts but falls short of the bar: slope +0.00179, day-clustered t 1.64, on 2841 in-profile grid cases over 447 days, with the supporting difference positive (+0.80 %). The test already used all four folds and all 19 coins on daily bars, so no more daily data is available to add.
- **F2:** On folds B and C the effect sits only at the top of the distance range and is not graded below it. The sextile of the raw distance nearest and above the 20-day high (above -0.18 swings) has a mean drift-removed 5-day return of +3.29 % (t 2.44, 191 cases), and the forecast's top sextile (above 4.5) has +3.47 % (t 2.54, 191 cases). The three sextiles between -2.2 and -0.18 swings all sit near +0.7 % (t below 0.8), and the -3.3 to -2.2 sextile sits at -3.44 % (t -3.72), so the middle of the range is noise.
- **F3:** The test measured at a shorter horizon than the one where the effect shows best. On folds B and C the forecast's slope t is 1.38 at 5 days (1144 cases), 2.03 at 10 days (574 cases) and -0.30 at 20 days (275 cases). The raw distance's slope t is 1.38 at 5 days and 2.33 at 10 days (slope 0.0165).
- **F4:** The effect is mixed across periods but mostly on the predicted side across coins. The 5-day slope's t is 2.21 in 2020 (379 cases) but -0.14 in 2021 (504 cases), and window w11 is negative (t -1.10, 234 cases). 10 of the 12 coins with a slope have a positive one, while UNI is negative (t -1.76).
- **F5:** The rising profile itself carries part of the move. In-profile grid cases beat the coins' normal 5-day drift by +0.41 % on average (1144 cases), so the market's own rise drowns much of the graded difference at 5 days.

## Ideas
- `034-01.b1_nearness-to-high-10-days` (from F3, F1, F5): In a rising market, the closer a coin's daily close sits below its 20-day high, measured in units of its own daily swing over the last 20 days (the standard deviation of its daily returns), the more it rises over the next 10 days.
- `034-01.b2_close-above-high-drifts` (from F2, F4): In a rising market, the further a coin's daily close stands above its 20-day high, measured in units of its own daily swing over the last 20 days (the standard deviation of its daily returns), the more it rises over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
