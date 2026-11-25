---
line: 7.b inconclusive
backtest: 038-01_calm-scaled-weekly-rise-continues_1d
idea tested: 038-01_calm-scaled-weekly-rise-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2099 USD
---
## Findings
- **F1:** In calm markets the effect is two-sided and clear. Pooling rises and falls on the 5-day grid (folds B and C), the regression of the drift-removed 5-day return on the scaled 7-day move has a slope t of 5.70 (718 cases). The sextiles run in order, from an unusual move of -3.40 % after the largest scaled falls (mean -1.37 usual swings) to +3.38 % after the largest scaled rises (+1.74).
- **F2:** Calm falls continue as calm rises do. On the fall side alone the slope t is 3.66 (336 cases), with a mean unusual move of -1.31 % (t -2.65). The rise side alone, the tested side, has a slope t of 2.71 (382 cases) and a mean of +1.46 %. Testing rises only left out half the cases and half the evidence.
- **F3:** The tested measure points the predicted way but falls short of the bar. Over all folds the slope t is 1.46 on 941 cases, and the unusual move is +0.27 % per case (t 0.68 over 645 days, strength 0.020). On folds B and C alone the forecast's slope t is 2.53 (382 cases), so the other folds dilute it but do not reverse it.
- **F4:** The effect is absent in agitated markets, as the brief predicts. On the 5-day grid the agitated slope t is 0.43 for both sides together (508 cases) and -0.47 for falls (258 cases), against 5.70 in calm markets.
- **F5:** The continuation holds across horizons in calm markets. The slope t for both sides together is 4.17 at 1 day (3,726 cases), 4.58 at 3 days (1,214), 5.70 at 5 days (718) and 3.86 at 10 days (350). The rise side alone at 10 days has a t of 4.37 (194 cases).
- **F6:** On the rise side the effect is uneven across coins and years. The slope t is 2.74 for XRP (53 cases) and -0.14 for LTC (64). It is 3.39 in 2020 and -0.45 to -0.48 in 2019 and 2021. Six coins give too few independent rise cases per coin to show a slope this small.

## Ideas
- `038-01.b1_calm-scaled-rise-more-coins` (from F3, F6): In a calm market, the larger a coin's 7-day rise measured against its 30-day daily swing, the larger its further rise over the next 5 days.
- `038-01.b2_calm-scaled-move-continues-both-ways` (from F1, F2, F4, F5): In a calm market, the larger a coin's 7-day move measured against its 30-day daily swing, the further it moves the same way over the next 5 days, rises continuing up and falls continuing down.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
