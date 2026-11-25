---
line: 7.b inconclusive
backtest: 059-01.b2_falling-calm-decline-continues_1d
idea tested: 059-01.b2_falling-calm-decline-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2113 USD
---
## Findings
- **F1:** The result points the way the idea predicts but falls short of the bar: step 5's slope is +0.00123 with a day-clustered t of 1.22 on 438 grid cases over 194 days, and the mean 5-day excess return is -0.58 %. The size agrees, with an unusual move of +1.28 % per case in the short's direction (t 2.29, 350 days, strength 0.116).
- **F2:** In folds B and C alone, the same 5-day grid gives a slope of +0.00274 (t 2.25, not clustered) on only 245 cases. That is about 20 cases per coin-year, so the effect is too thin for the bar rather than absent.
- **F3:** The effect is clearest at shorter horizons, which carry more independent cases. At 3 days the slope is +0.00165 (t 2.84) and the mean excess -1.37 % (t -3.75, 411 cases); at 1 day the mean excess is -0.48 % (t -3.79, 1,271 cases). At 10 and 20 days the slope fades (t 1.21 and -0.04).
- **F4:** The grading is present but noisy. By raw-depth quartile the 5-day mean excess runs from -2.33 % in the deepest quartile (51 cases) through -4.14 % and -3.29 % to +0.13 % in the shallowest. By forecast quartile it runs from -3.54 % (t -2.40, 62 cases) to +1.11 % in the shallowest.
- **F5:** Five of the six coins point the idea's way at 5 days, with slopes from +0.0014 to +0.0049 (ETH, XMR, ZEC, BTC, LTC), but none reaches t 2 on 28 to 55 cases. XRP alone goes against it (slope -0.0014, t -0.27, 37 cases), so the effect is spread thinly across coins rather than carried by one.
- **F6:** The years differ. 2018 (118 cases, slope t 2.21) and 2019 (93 cases, mean excess -2.60 %, t -3.72) carry the fall, while 2020 and 2021 hold only 34 cases with a positive mean excess. The falling calm profile is rare (23 % of bars in profile, 66 % of those short), so more coins are the way to more cases.

## Ideas
- `059-01.b2.b1_falling-calm-decline-more-coins` (from F1, F2, F5, F6): In a falling, calm market, the further a coin's 14-day return has fallen below zero, measured in units of its own 30-day daily swing, the larger its fall over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
