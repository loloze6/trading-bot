---
line: 7.b inconclusive
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d1_range-expansion-in-uptrends_1d
idea tested: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d1_range-expansion-in-uptrends
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3271 USD
---
## Findings
- **F1:** The tested result points the way the idea predicts but falls short of the bar: the pooled slope of the 5-day excess return on the forecast is +0.00084 with t 1.44 over 1,685 trending grid cases, the top-minus-bottom-third difference is +0.90 %, and in the forecast quintiles only the strongest fifth stands out (+1.19 % mean excess return at forecast 18.5, against −0.19 % to +0.44 % in the other four).
- **F2:** The shortfall comes from where the 5-day grid happens to start rather than from a missing effect: on the same trending bars, moving the grid's starting day gives forecast-slope t values of 1.44, 3.35, 3.64, 2.59 and 1.22 (offsets 0 to 4, about 1,620 to 1,690 cases each). The plan's grid, offset 0, is one of the two weakest.
- **F3:** The raw range ratio (today's range over its 30-day mean) predicts more clearly than the standardised forecast. In trending bars its 5-day slope has t 2.12 (1,281 cases) on offset 0, and t 5.51, 3.59, 1.15 and 2.56 on the other offsets. At 3 days it has t 5.21 (2,167 cases) and at 10 days t 4.73 (623 cases).
- **F4:** The uptrend condition carries the effect. While the 20-day return is at or below zero, the ratio's slope is −0.0035 (t −0.69, 1,274 cases) at 5 days and −0.0078 (t −0.88) at 10 days. In a pooled 5-day regression, the ratio-times-uptrend term is +0.013 (t 1.92), while the ratio alone is −0.0035 (t −0.67).
- **F5:** The effect is uneven across coins and years.
- **F6:** Cost does not block the idea: the total move per case (+0.92 %) is 4.8 times the 0.19 % cost of a trade, and the unusual move is 1.7 times it. The book had a Sharpe of 0.80 but failed only on Calmar (0.515).

## Ideas
- `022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d1_range-expansion-in-uptrends.b1_range-expansion-uptrend-more-coins` (from F1, F2, F5): The wider a coin's daily high-low range is relative to its average range over the past 30 days, the higher that coin's return over the next 5 days, only while the coin's own 20-day return is positive.
- `022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d1_range-expansion-in-uptrends.b2_range-expansion-three-day-rise` (from F3, F4, F5): The wider a coin's daily high-low range is relative to its average range over the past 30 days, the higher that coin's return over the next 3 days, only while the coin's own 20-day return is positive.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
