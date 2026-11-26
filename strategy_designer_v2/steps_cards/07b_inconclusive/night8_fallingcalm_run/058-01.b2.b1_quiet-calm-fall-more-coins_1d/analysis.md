---
line: 7.b inconclusive
backtest: 058-01.b2.b1_quiet-calm-fall-more-coins_1d
idea tested: 058-01.b2.b1_quiet-calm-fall-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2420 USD
---
## Findings
- **F1:** The test's main measure is close to zero. The slope of the drift-adjusted 5-day return on the forecast is +0.00021 with a day-clustered t of 0.46 over 931 in-regime grid bars on 271 days. The unusual move is +0.32 % per case (t 0.63, 434 days), only 0.031 of the coin's usual 11.58 % move. The coin's own drift of -0.69 % against the short leaves the total move at -0.37 %, which is 1.7 times the 0.22 % cost of a trade, on the losing side.
- **F2:** The quieter-volume grading is absent in folds B and C. Split into forecast quartiles, the drift-adjusted 5-day return does not get steadily lower as volume gets quieter: -0.97 % in the quietest quartile (t -0.88), -0.79 % (t -0.63), +0.31 % (t 0.18), and -1.05 % in the least quiet (t -0.97), about 78 cases each. The bars with forecast 0 (heavy volume) averaged -1.22 % (n 25), lower than the -0.58 % of the quiet-volume bars (n 286), the opposite of the brief's claim.
- **F3:** Another horizon does not show it either. In folds B and C the forecast slope's t is 0.04, -0.76, 0.13, -0.57 and -1.06 at 1, 3, 5, 10 and 20 days. The 20-day reading is the only one near 1, and it has the wrong sign.
- **F4:** The brief's base claim, that a deeper 30-day fall keeps falling, is not in the falling-calm bars. The slope of the drift-adjusted return on the 30-day return has a t of 0.09 at 5 days, and -0.87 and -0.99 at 10 and 20 days, so deeper falls lean towards rebounding. Outside the profile the same slope is t -1.04 (n 434), so it does not single out the calm downtrend.
- **F5:** No coin or year carries the effect consistently. The coin slopes run from XMR's t +1.87 to XRP's t -1.81, and the year slopes from 2018's t +0.84 to 2019's t -0.43. Crossing depth with quietness gives one stand-out cell, middle-depth falls on quieter volume at -4.66 % against -1.71 % for louder volume, but it holds only 34 cases. Deep falls (-0.17 % against -0.07 %) and shallow falls (-0.36 % against +0.04 %) show no difference.

## Ideas
- No ideas: The theme's effect is not in the data. The test already used every coin and fold available, its result is a zero (F1), and neither the volume grading nor the depth continuation shows at any horizon, coin, year or depth (F2–F5).

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
