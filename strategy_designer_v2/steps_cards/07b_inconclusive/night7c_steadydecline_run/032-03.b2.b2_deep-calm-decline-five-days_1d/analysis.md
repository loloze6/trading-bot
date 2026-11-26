---
line: 7.b inconclusive
backtest: 032-03.b2.b2_deep-calm-decline-five-days_1d
idea tested: 032-03.b2.b2_deep-calm-decline-five-days
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3303 USD
---
## Findings
- **F1:** The test's main measure is on the side the idea predicts but well short of the bar (t 0.88 over 380 case days, slope +0.00049), and the idea is small: an unusual move of +0.30 % per case over 5 days (t 0.68 over 544 days), only 0.027 of the coin's usual 10.60 % move, while the total move in the short direction is −0.29 % against a trade cost of 0.19 %.
- **F2:** In folds B and C the effect comes from one bear year: the short-direction unusual 5-day move is +3.19 % in 2018 (t 2.07, 57 days), against −0.06 % in 2019, −1.11 % in 2020 and −1.67 % in 2021, so the rising years' market moves drown it.
- **F3:** It is mixed across windows: 6 of the 12 windows are positive, w7 is +3.58 % (t 2.04) and w12 is −4.27 % (t −1.81), with no window other than w7 reaching |t| 2.
- **F4:** It is present on every coin but weak on each: BTC +1.56 % (t 1.49), LTC +1.28 % (t 1.26), and ETH, XMR, XRP and ZEC between +0.11 % and +0.51 % with t under 0.4.
- **F5:** The grading by the plan's forecast is only partly there: the deepest and second quartiles of the fall carry +1.73 % (t 1.38) and +2.20 % (t 1.63), while the third and the shallowest quartiles are −0.29 % and −1.01 %.
- **F6:** The same sign holds at every horizon up to 10 days, with t falling as the horizon lengthens (1 day +0.20 % t 1.23, 3 days +0.52 % t 1.06, 5 days +0.66 % t 0.79, 10 days +0.81 % t 0.45); at 20 days it turns to −1.69 %, so the plan's horizon is not where the effect shows least.
- **F7:** Measuring the 28-day fall against the coin's own 60-day daily volatility grades the effect more clearly in low-volume falls. The slope of the 5-day short-direction unusual move on this depth has t 2.09 (251 cases), against 1.75 at 3 days and 1.05 at 1 day. By quartile it runs from +2.77 % and +5.13 % (t 2.85) for the deepest two to −1.96 % for the smallest.
- **F8:** The low-volume condition matters. Among all 28-day falls, those on low volume are followed by short-direction unusual 5-day moves of +2.77 % (deep, t 1.12) and +4.06 % (mid, t 2.37). Those on high volume give −1.33 % (deep), +1.08 % and −0.57 %.

## Ideas
- `032-03.b2.b2.b1_calm-decline-more-coins` (from F1, F3, F4, F8): Among coins whose volume over the past 28 days is below their own usual volume, the larger the fall over those 28 days, the larger the further fall over the next 5 days.
- `032-03.b2.b2.b2_volatility-scaled-calm-decline` (from F5, F7, F8): Among coins whose volume over the past 28 days is below their own usual volume, the larger the fall over those 28 days measured against the coin's own typical daily move over the past 60 days, the larger the further fall over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
