---
line: 7.b inconclusive
backtest: 006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound.g1_volume-surge-predicts-weekly-return_1d
idea tested: 006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound.g1_volume-surge-predicts-weekly-return
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.2777 USD
---
## Findings
- **F1:** The tested measure lies on the side the idea predicts but just short of the bar: the 7-day slope is +0.000462 with t = 1.94 over 2443 independent cases, the top-minus-bottom tercile difference is +0.0075, and the 7-day quintile means of excess return run from -0.0018 and -0.0086 in the two lowest to +0.0085 and +0.0064 in the two highest. That spread is small against a 7-day excess-return standard deviation of 0.134, so the market's own moves largely drown it.
- **F2:** The effect is clearer at horizons shorter than the plan's 7 days and fades at longer ones: the slope t is 4.70 at 1 day (17380 cases), 3.51 at 2 days (8650), 3.62 at 3 days (5723), 2.87 at 5 days (3419), 1.94 at 7 days (2443), 0.48 at 14 days (1152) and 0.16 at 21 days (720).
- **F3:** At 7 days the effect is concentrated in part of the data. XRP gives t = 2.90 and ZEC t = 1.15, against BTC at -0.06 and XMR at -1.22 (about 407 cases each). By year, 2024 gives t = 3.90, against 2018 at -0.89 and 2019 at -0.01 (about 300 cases each).
- **F4:** At 7 days the effect also depends on the last 5 days' direction, so it is mixed. After a 5-day rise the slope t is 2.13 (1202 cases), and after a 5-day fall it is 0.36 (1097). At 14 days the two sides have opposite signs: t = +2.09 after a rise (544) and -2.16 after a fall (608).
- **F5:** At 3 days the effect holds across the data and keeps its order. The slope is positive for all 6 coins (t from 0.11 for LTC to 3.14 for XRP) and in 7 of 8 years (t from 0.54 to 3.89, with 2018 at -0.22). The quintile means of excess return rise from -0.0061 in the lowest to +0.0072 in the highest.

## Ideas
- `006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound.g1_volume-surge-predicts-weekly-return.b1_volume-surge-more-coins` (from F1, F3): For a coin, the higher its 5-day average volume against its 30-day average, the higher its return over the next 7 days, whatever the direction of its last 5 days.
- `006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound.g1_volume-surge-predicts-weekly-return.b2_volume-surge-three-day-return` (from F2, F5): For a coin, the higher its 5-day average volume against its 30-day average, the higher its return over the next 3 days, whatever the direction of its last 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
