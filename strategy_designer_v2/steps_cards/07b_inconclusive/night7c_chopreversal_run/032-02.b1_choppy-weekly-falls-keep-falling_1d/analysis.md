---
line: 7.b inconclusive
backtest: 032-02.b1_choppy-weekly-falls-keep-falling_1d
idea tested: 032-02.b1_choppy-weekly-falls-keep-falling
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3726 USD
---
## Findings
- **F1:** The tested result points the way the idea predicts but falls short of the bar. Over all folds, short cases had a mean unusual 7-day move of +1.06 % (day-clustered t 1.41, 441 cases on 350 days, strength 0.075). In folds B and C alone, the 7-day grid cases in the situation had a mean of +2.29 % (t 1.44 with the cases of one day together, 228 cases on 86 days, strength 0.14).
- **F2:** The effect is mixed across periods and coins.
- **F3:** The further fall is graded by the raw 30-day efficiency ratio.
- **F4:** The plan's forecast standardises ER against its own past 60 values, which correlates only 0.68 with the raw ratio. That may be why the full-data supporting check failed (stronger minus weaker −0.56 %). In folds B and C the forecast terciles were still graded: +0.33 %, +2.76 %, +4.41 % from weak to strong forecast.
- **F5:** Weekly falls outside the situation show no continuation (mean −0.19 %, t −0.26, 361 cases), so what the move follows is the choppy 30-day path.
- **F6:** The 7-day horizon is where the effect shows: −0.66 % over 3 days (t −1.01), +2.29 % over 7 days and +2.72 % over 14 days (t 1.74, plain t, 214 cases).
- **F7:** The total move per case over all folds was +0.17 %, 0.9 times the 0.19 % cost of a trade. The unusual move was 5.5 times that cost, so only a clearer, larger effect would let a book pay.

## Ideas
- `032-02.b1.b1_choppy-falls-more-coins` (from F1, F2, F6): When a coin has fallen over the past 7 days while its past 30 days were choppy and agitated, with large daily swings both ways and little net progress, it tends to keep falling over the next 7 days. The less net progress the coin made over those 30 days relative to the path it travelled, the larger that further fall.
- `032-02.b1.b2_weekly-falls-after-directionless-months` (from F3, F4, F5): When a coin has fallen over the past 7 days, it tends to keep falling over the next 7 days, and the less net progress its past 30 days made relative to the path its price travelled, the larger that further fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
