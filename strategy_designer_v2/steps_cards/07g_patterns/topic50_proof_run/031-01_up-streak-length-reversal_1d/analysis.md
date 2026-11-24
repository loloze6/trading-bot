---
line: 7.g patterns
backtest: 031-01_up-streak-length-reversal_1d
idea tested: 031-01_up-streak-length-reversal
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5871 USD
---
## Findings
- **F1:** In calm markets (the coin's 30-day swing at or below its own median), the coin's 20-day return scaled by its 30-day swing predicts its next 5-day unusual move with the same sign (standardised slope 0.156, t 2.93 with each day's cases taken together, 671 non-overlapping cases on 172 days; the 10-day return gives 0.180, t 2.89). In agitated markets the same reading is flat (0.013, t 0.17, 674 cases; 10-day −0.034, t −0.48).
- **F2:** The calm-market effect is graded across quintiles of the scaled 20-day return. The mean unusual 5-day move rises step by step: −3.85 %, −1.53 %, +0.19 %, +2.05 %, +2.25 % (about 134 cases each).
- **F3:** The calm-market effect has the same sign on all six coins, with slopes from 0.128 to 0.192 (t from 1.16 for XRP to 2.35 for ETH, 99 to 118 cases each). By window it is mixed: of 10 windows read in calm markets, 5 have a positive slope and 5 a negative one, each with |t| under 1.3.
- **F4:** The tested reversal is not in these folds. After up streaks, the unusual 5-day move is positive at every length: +0.60 % at 3 days, +0.87 % at 4 days, +1.58 % at 5 or more (t 0.49, 0.60, 0.99). By coin, 4 of 6 coins show a positive move after streaks of 3 or more days, the opposite of the idea's side.
- **F5:** Streak length itself adds little beyond the past return. The slope of the next 5-day move on up-streak length is 0.075 (t 1.26) in calm markets and 0.023 (t 0.33) in agitated ones. In rising markets it is 0.158 (t 1.67, 160 cases). None reaches 2.
- **F6:** The book lost mainly by being short while the coins rose. Its mean position was −0.73 of the book while the coins' mean daily return was +0.162 %, and the book's mean daily return was −0.128 %. It was below holding in 9 of 12 windows and on every one of the six coins.
- **F7:** The other angles checked do not stand out once the number of angles is counted. These were the 1-day move, the 3-day return, the weekday, trend crossed with agitation, and down-streak length. Their largest |t| values were about 2 to 3, without a graded pattern; for example, down streaks of 4 days have t −3.06 on 40 cases, but 5 days have t −1.82 on 21 cases and 3 days have t +1.34.

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `031-01.g1_calm-market-vol-scaled-momentum` (from F1, F2, F3, F6): In a calm market, the more a coin has risen over its last 20 days relative to its own daily swing over the past 30 days, the more it rises over the next 5 days; the more it has fallen, the more it falls.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
