---
line: 7.b inconclusive
backtest: 027-03_panic-rebound-in-downtrend.d1_graded-sell-off-liquidity-premium_4h
idea tested: 027-03_panic-rebound-in-downtrend.d1_graded-sell-off-liquidity-premium
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 3.8410 USD
---
## Findings
- **F1:** The tested measure is zero, not short of the bar. The 1,050 cases show an 84-bar (14-day) excess over drift of +0.05 % with t 0.09. The other horizons are also near zero: +0.16 % (t 0.93) over 1 day, +0.16 % (t 0.54) over 3 days, −0.51 % (t −1.24) over 7 days and −0.61 % (t −0.68, 998 cases) over 21 days, so no other horizon holds the effect.
- **F2:** The effect is not graded, and the deepest falls are the worst. By forecast quartile, the 14-day excess is +0.25 %, +0.67 % and +0.09 % for the lower three quartiles. The top quartile (forecast 20) is −0.80 % (t −0.74). The plan's slope is negative (−0.00082). On a causal rebuild (the first fall of over 1.5 usual moves with the range above its 30-day mean, 699 cases), the Spearman correlation of fall × range with the 14-day excess is −0.03.
- **F3:** The range expansion that defines a panic does not sort the outcome. By range-ratio quartile (mean ratio 1.00, 1.14, 1.30, 1.88), the 14-day excess is +0.87 %, +0.04 %, −0.63 % and +2.34 %, with no t above 1.61. On the regular 14-day grid, falls sorted into fall × range quintiles give −0.47 %, −1.49 %, −1.37 %, −2.40 % and −0.07 %, all with |t| < 1.3 on 73 cases each.
- **F4:** The year's market sets the sign of the result, so the market's own moves drown the idea. The 14-day excess per case is −7.0 % (t −3.60) in 2018 and −4.9 % (t −3.63) in 2022. It is +3.5 % (t 1.69) in 2020, +4.1 % (t 1.79) in 2021 and +3.9 % (t 2.31) in 2024. The causal rebuild repeats this pattern: −7.1 % (t −2.64) in 2018 and +11.6 % (t 4.26) in 2021.
- **F5:** No coin carries the effect. The 14-day excess by coin runs from −1.25 % (ETH, t −0.95) to +1.48 % (ZEC, t 0.67), and every |t| is below 1.
- **F6:** The only positive part sits in coins that were already rising, which is the brief's own condition for the theory being wrong.
- **F7:** The strong rebounds in the round-2 exploration (+6.1 % over 14 days, t 8.96, 809 cases) are a look-ahead artefact and are not evidence. They come from picking each grid cell's deepest fall after the fact, which is its low. Taking the first qualifying fall instead, as a trader would, leaves +1.06 % (t 1.42, 699 cases) over 14 days and +0.65 % (t 1.86) over 3 days.
- **F8:** The book's Sharpe of 0.70 comes from the coins' normal drift, not from the idea. Per case, the total move is +2.14 %, of which the drift is +2.09 % and the unusual move +0.05 %. The unusual move is 0.3 times the 0.19 % cost of a trade, with a strength of −0.008.

## Ideas
- No ideas: The panic rebound is zero at every horizon (F1). It does not grow with the fall or the range expansion (F2, F3), and its sign follows the year's market (F4). The only positive part is a borderline 3-day bounce in coins that were already rising (F6), which is the brief's own condition for the theory being wrong, so the clear answer is that this data shows no panic premium to amend toward.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
