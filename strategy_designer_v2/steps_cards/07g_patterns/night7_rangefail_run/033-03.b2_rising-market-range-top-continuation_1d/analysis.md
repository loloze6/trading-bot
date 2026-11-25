---
line: 7.g patterns
backtest: 033-03.b2_rising-market-range-top-continuation_1d
idea tested: 033-03.b2_rising-market-range-top-continuation
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3686 USD
---
## Findings
- **F1:** The tested relation holds inside the rising profile on the explored folds: the slope of the 5-day return above the coin's drift on the close's place in its 20-day range is 0.0296, with day-clustered t 2.49 (599 non-overlapping cases on 165 days). Closes above the top of the range are followed by +5.17 % above drift (90 cases), against -2.42 % for the lowest band (100 cases).
- **F2:** The relation is carried by calm markets, in and out of the rising profile. Calm is taken as 20-day volatility at or below the coin's median.
- **F3:** Outside the rising profile the relation is also present but weaker. Overall slope is 0.0170, clustered t 1.55 (823 cases). In choppy markets it is 0.0598 with t 2.22 (127 cases, 66 days). In falling markets it is 0.0270 with t 1.59 (401 cases).
- **F4:** The book earns almost entirely on its long side.
- **F5:** In the rising profile, the size of the last day's move relative to volatility predicts the next 5 days (clustered t 2.46, 599 cases). Measured together with the range position, both lose strength: range t 1.82, one-day move t 1.55. It is the same information, not a separate pattern.
- **F6:** Thursday and Friday bars are followed by higher next-day returns: +0.61 % with t 1.93, and +0.55 % with t 2.18 (about 207 days each). This was one of many angles looked at, so it does not stand out from chance and is not used.

## Ideas
- `033-03.b2.g1_calm-market-range-position-drift` (from F2, F1, F3): In a calm market, the higher a coin's daily close sits within its 20-day high-to-low range, the more the coin rises over the next 5 days.
- `033-03.b2.g2_rising-range-top-long-drift` (from F4, F1): In a rising market, the higher a coin's daily close sits within its 20-day high-to-low range, the more the coin rises over the next 5 days, and the move is largest for closes beyond the top of the range.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
