---
line: 7.b inconclusive
backtest: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b2_moderate-flat-range-slide-continues_1d
idea tested: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b2_moderate-flat-range-slide-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3272 USD
---
## Findings
- **F1:** The main measure is on the side the idea predicts, a mean short-side unusual 5-day move of +1.09 % with t 2.32 over 436 cases, but the grading fails: the larger-|forecast| half beats the smaller half by -0.77 %, and Spearman's rho between |forecast| and the unusual move is -0.09 (p 0.06).
- **F2:** The grading is hump-shaped, not monotone: by |forecast| quartile the unusual move is +0.66 % (t 0.59), +2.30 % (t 2.31), +1.13 % (t 1.26) and +0.29 % (t 0.39) from the weakest to the strongest. By raw 10-day return quartile it is +1.94 % (deepest), +2.78 %, -1.20 % and +1.31 % (shallowest), so a deeper slide does not reliably give a larger follow-through.
- **F3:** The effect is split in time: in 2018-2022 the unusual move is +2.33 % with t 3.42 over 268 cases, and every coin is positive there (+1.6 % to +4.2 %). In 2023-2025 it is -0.87 % with t -1.63 over 168 cases, and five of the six coins are negative (only ZEC is +2.08 %). The halves' difference is negative in both periods (-0.48 % and -1.31 %).
- **F4:** ZEC carries much of the pooled t: ZEC alone gives +3.42 % with t 2.99 over 73 cases. Without ZEC, the 5-day measure drops to +0.63 % with t 1.22 over 363 cases. The other coins lie between +0.23 % and +0.87 %, all with t below 0.81.
- **F5:** The 5-day horizon is not where the effect stands out: the unusual move is +0.37 % (t 1.98, 1131 cases) over 2 days, +0.44 % (t 1.44, 750) over 3 days, +1.09 % (t 2.32, 436) over 5 days and +1.61 % (t 2.00, 203) over 10 days.
- **F6:** The "moderate, not extreme" veto removes almost nothing: only 12 of 316 situation bars on the 5-day grid were vetoed. Their unusual move, +0.90 % (t 0.39), is close to the kept bars' +1.04 % (t 2.16), so the comparison the idea adds is not testable at this size.
- **F7:** The effect is small against the cost of trading it: the total move per case is +0.12 % over 5 days, against a cost of 0.19 % per trade, because shorting fights a normal drift of -0.59 %. The book's Sharpe is -0.55.

## Ideas
- `023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b2_moderate-flat-range-slide-continues.b1_moderate-flat-range-slide-more-coins` (from F1, F2, F4): In a coin whose 30-day net move has been small relative to its 30-day high-low range and whose close sits below the middle of that range, the more its 10-day return is negative, the more it falls over the next 5 days, only while that fall is moderate rather than extreme against its own recent 10-day moves.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
