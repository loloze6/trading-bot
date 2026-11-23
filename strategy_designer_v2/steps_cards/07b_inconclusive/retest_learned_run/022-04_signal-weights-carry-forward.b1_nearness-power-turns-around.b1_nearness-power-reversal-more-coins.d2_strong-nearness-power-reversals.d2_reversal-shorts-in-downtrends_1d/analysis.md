---
line: 7.b inconclusive
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends_1d
idea tested: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 3.6986 USD
---
## Findings
- **F1:** The main measure is on the side the idea predicts but short of the bar (weighted t 1.50 over 699 cases), and it is weaker than the unweighted excess fall, whose mean is +0.83 % per 5 days with t 2.24. Weighting by |forecast| removes signal instead of adding it, because the move is not graded: the Spearman correlation of |forecast| with the excess fall is −0.015, and the supporting check is −0.40 % (t −0.53).
- **F2:** Larger readings do not bring larger falls. Mean excess fall by |forecast| quintile is +1.01 %, +1.26 %, +0.57 %, +0.79 % and +0.54 % from the weakest to the strongest. 137 of the 699 cases (20 %) sit at the clip of 20 and fall only +0.47 % (t 0.57), against +0.92 % (t 2.21) for the 562 unsaturated cases.
- **F3:** The effect sits in coins that rose over the 5 days before the signal inside their 20-day fall. Those 269 cases fall +2.04 % more than the coin's drift (t 3.53, weighted t 3.16, strength 0.18). The 430 cases after a falling 5 days show +0.08 % (t 0.17, weighted t −0.30). Inside the rising-5-day cases the above-median readings fall +0.84 % more than the below-median ones (t 0.72).
- **F4:** The effect fades in deep downtrends. Cases with a 20-day return below −20 % show −0.25 % (t −0.34, 149 cases). Cases between −11 % and −4 % show +1.61 % (t 1.84, weighted t 2.54, 140 cases).
- **F5:** A few large rallies drown the effect. Dropping the 2 % tails on each side lifts the 5-day t from 2.24 to 2.99 (weighted t from 1.50 to 2.71, 671 cases). 17 of 24 windows (71 %) and 11 of 15 coins have a positive mean excess fall.
- **F6:** The plan's 5-day horizon is where the effect is clearest. Unweighted t is 2.17 over 1 day, 1.76 over 3 days, 2.24 over 5 days, 1.52 over 10 days and 0.35 over 20 days. Strength is 0.07 over 5 days.

## Ideas
- `022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends.b1_nearness-reversal-more-coins` (from F1, F5): For a coin's nearness to its 90-day high, the higher that signal's predictive power for the coin's 5-day returns over the past 365 days, the lower its power over the following 90 days. The larger both the excess past power and today's deviation of nearness from its usual level, when the reading points against a past relation that implies a rise, the larger the coin's fall over the next 5 days, only while the coin's 20-day return is negative.
- `022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends.b2_reversal-shorts-on-downtrend-bounces` (from F3, F1, F6): For a coin's nearness to its 90-day high, the higher that signal's predictive power for the coin's 5-day returns over the past 365 days, the lower its power over the following 90 days. The larger both the excess past power and today's deviation of nearness from its usual level, when the reading points against a past relation that implies a rise, the larger the coin's fall over the next 5 days, only while the coin's 20-day return is negative and its 5-day return is positive.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
