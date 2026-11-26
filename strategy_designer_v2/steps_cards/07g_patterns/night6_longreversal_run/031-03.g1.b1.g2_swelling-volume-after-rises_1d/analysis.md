---
line: 7.g patterns
backtest: 031-03.g1.b1.g2_swelling-volume-after-rises_1d
idea tested: 031-03.g1.b1.g2_swelling-volume-after-rises
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4292 USD
---
## Findings
- **F1:** Over all 14-day grid bars, whatever the coin's 14-day direction, the volume swell (the 14-day mean volume over the 30-day mean, minus 1) predicts the next 14-day excess return. The slope is 0.121 with t 2.97 on 1530 cases. All 19 coins have a positive slope (8 of them with t ≥ 2). The effect sits mostly in the later half: after 2021 the slope is 0.163 (t 3.20, 1020 cases), and up to 2021 it is 0.042 (t 0.69, 510 cases).
- **F2:** The swell works after 14-day falls too, not only after rises.
- **F3:** Shrinking volume is the more reliable side. The bottom 20 % of the volume swell is followed by a −4.4 % excess return over 14 days (t −2.59, 1530-case grid), against +5.1 % (t 1.88) for the top 20 %. In the lowest swell quintile after a 14-day rise, the excess return is −5.1 % (t −2.65, 131 cases).
- **F4:** The effect is strongest at 14 days.
- **F5:** The brief's own reversal is absent. The 60-day return has no slope on the next 14-day excess return: −0.0014, t −0.07, 918 cases. The 14-day return leans toward continuation, not reversal: slope 0.108, t 2.32, 2142 cases.
- **F6:** The book's gain is spread across bars but tracks the market and the weekend. Its daily returns correlate 0.68 with the coins' mean daily return. Its Saturday mean is +0.19 % a day (t 3.43, 414 days) and its Friday mean +0.18 % (t 2.51). Among the many angles looked at, this weekday pattern is the only one of that strength, so I take it as possibly chance and draw no idea from it.

## Ideas
- `031-03.g1.b1.g2.g1_swelling-volume-after-falls` (from F2, F1, F4): When a coin has fallen over the last 14 days, the more its mean daily volume over those 14 days has risen above its 30-day mean, the more its price rises over the next 14 days.
- `031-03.g1.b1.g2.g2_drying-volume-precedes-falls` (from F3, F1, F4): The more a coin's mean daily volume over the last 14 days has fallen below its 30-day mean, the more its price falls over the next 14 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
