---
line: 7.b inconclusive
backtest: 036-02_agitated-scaled-fall-delayed-rebound_1d
idea tested: 036-02_agitated-scaled-fall-delayed-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3521 USD
---
## Findings
- **F1:** Step 5's main measure is on the side the idea predicts but short of the bar: the slope of the 2-bar excess return on the forecast has t 1.21 over 1879 grid cells with a positive forecast, and the forecast-weighted mean excess is +0.28 %. The size is tiny and cannot be told from 0: an unusual move of +0.04 % per case (t 0.18, 987 days, 2287 cases), 0.005 of a usual 6.58 % move.
- **F2:** In folds B and C, on agitated bars, the day-2-to-3 excess return grows with the fall measured in usual daily moves. It is −0.62 % after falls under 0.5 (322 cells), +0.35 % at 0.5–1 (205), +1.13 % at 1–1.5 (112), +1.57 % at 1.5–2 (51) and +1.97 % at 2–3 (24). The slope has t 2.14 on 715 cells and the Spearman rho is 0.071 (p 0.057). In calm markets the same slope has t 0.05 on 959 cells, as the brief predicts.
- **F3:** The graded delayed rise has the predicted sign almost everywhere but is too small to show in any one part. The capped slope is positive on 5 of 6 coins (t from 0.71 to 1.63; ETH −0.30) and in 3 of 4 years (2019 t 2.93, 2021 t 2.00, 2018 −0.34). No part is clean enough to narrow to, and each has only 89 to 272 cells.
- **F4:** The next-day rebound in agitated markets is stronger than the delayed one: its slope has t 4.62 on 1439 bars, against t 2.45 in calm markets. That slope falls to t 1.76 once falls are capped at 3 usual moves, because 12 falls beyond 3 usual moves are followed by +11.7 % the next day. So the day-1 move is driven by a few extreme cases, while the delayed rise in F2 is graded over the whole range.
- **F5:** The test's forecast tracks the raw lagged fall closely: its correlation with the lagged fall in usual moves is 0.90 on 1427 active bars, and 100 % of those bars follow a fall. The test therefore measured the idea's own situation, and the gap between F2's t 2.14 and step 5's t 1.21 points to too few cases rather than a wrong measure.

## Ideas
- `036-02.b1_delayed-rebound-more-coins` (from F1, F2, F3, F5): In an agitated market, the larger a coin's one-day fall against its 30-day daily swing, the larger its rise over the second and third days after the fall, leaving out the day right after it.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
