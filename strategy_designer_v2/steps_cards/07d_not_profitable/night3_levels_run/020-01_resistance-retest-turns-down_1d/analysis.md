---
line: 7.d not profitable
backtest: 020-01_resistance-retest-turns-down_1d
idea tested: 020-01_resistance-retest-turns-down
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3127 USD
---
## Findings
- **F1:** The book lost because it stood short against coins that rose. Its mean position was -0.45 of the book, while the six coins rose 0.07 % to 0.16 % a day on average over all windows. The part of its daily gain owed to the market's own rise was -0.053 %, out of a total of -0.058 %, so timing added almost nothing. Two thirds of the 24 windows lost, and the book's mean daily return was -0.085 %.
- **F2:** The resistance effect is not in these bars. The verdict's unusual move was -0.05 % per case over 5 days, a strength of 0.002 against a usual move of 10.6 %, or -0.2 times the 0.19 % cost of a trade. The Spearman correlation between the count of turns above and the 5-day unusual move is 0.009. Unusual moves across count bins from 0–1 to 5 or more show no gradient (-0.12 %, +0.11 %, +0.78 %, -0.93 %).
- **F3:** Closeness to the 90-day high is followed by rises, not falls. The two grid quintiles nearest the high had 5-day unusual moves of +0.95 % (t 1.97) and +0.60 % (t 1.27), 511 cases each. The middle quintiles were -0.90 % and -0.59 %.
- **F4:** Closes above the prior 90-day high continue, and more so the further above. In terciles of distance above, the 5-day unusual moves were +0.40 %, +1.11 % and +1.83 %, and the total moves +0.99 %, +1.67 % and +2.47 %. That is 5 to 13 times the 0.19 % cost, but on only 165 cases with t 1.15.
- **F5:** The 30-day return grades the next 5 days. By quintile of the 30-day return, the 5-day unusual move runs -0.35 %, -0.68 %, -0.38 %, +0.25 % and +1.26 %; the top quintile reaches t 2.13 on 511 cases. Inside the book's own short cases, the quarter with the strongest 30-day rise was followed by +1.47 % unusual, against the bet.
- **F6:** Breaking a level helps only slightly. Bars where the level above vanished after being present in the prior 5 days were followed by +1.32 % unusual and +1.91 % total over 5 days (155 cases, t 1.24). The move does not grow with the number of earlier turns: +1.81 %, +3.94 %, -2.83 % and +1.46 % by count bin.

## Ideas
- `020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high` (from F3, F4, F6, F1): The further a coin's daily close stands above its highest close of the previous 90 days, the more it rises over the next 5 days.
- `020-01_resistance-retest-turns-down.d2_thirty-day-momentum-continues` (from F5, F3, F1): The larger a coin's 30-day return, the more it rises over the next 5 days.
- `020-01_resistance-retest-turns-down.d3_nearness-to-90-day-high` (from F3, F2, F1): The closer a coin's daily close sits below its highest close of the past 90 days, the more it rises over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
