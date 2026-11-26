---
line: 7.g patterns
backtest: 032-02.b1_choppy-weekly-falls-keep-falling_1d
idea tested: 032-02.b1_choppy-weekly-falls-keep-falling
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4282 USD
---
## Findings
- **F1:** A large down day relative to the coin's usual daily swing (30-day volatility) is followed by a next-day rebound, and the rebound grows with the size of the fall. The unusual next-day move after days below -1.5 usual swings is +1.17 % (t 2.15 with the cases of one day together, 372 cases on 122 days). By size of the fall, it is +2.97 % below -2.5 swings (t 3.22, 69 cases), +0.77 % between -2.5 and -1.5 (t 2.55, 303 cases) and +0.33 % between -1.5 and -0.5 (t 2.30, 1325 cases). Over 3 days it is +2.25 % below -2 swings (t 2.50, 43 cases).
- **F2:** The rebound after large down days holds across the data and in both kinds of market. It is positive in 11 of the 12 windows (w9 alone -0.19 %) and in all 6 coins (+0.54 % for BTC to +1.49 % for XMR). It shows in chop (+0.97 %, t 1.89, 250 cases) and in trend (+1.56 %, t 1.50, 122 cases). Large up days show no mirror move (z1 above 1.5: -0.22 %, t -0.54, 443 cases).
- **F3:** In calm choppy periods (30-day efficiency ratio below 0.3, volatility percentile below 0.5), the past week's move continues over the next week, which is the opposite of the brief's reversal. In the move's direction the unusual 7-day move is +3.93 % on grid offset 0 (t 2.17, 235 cases, 69 days) and +3.40 % on offset 3 (t 2.04, 223 cases, 65 days). It grows with the weekly move's size in usual swings (slope 0.051, unclustered t 4.93, 235 cases). In agitated chop the continuation is absent (slope 0.009, t 0.50, 96 cases; -2.4 %, t -1.13 on offset 3).
- **F4:** The book's extreme days are the coin moving against its shorts. On the book's worst 2 % of days (mean -0.82 %) the coins rose +9.8 %, and on its best 2 % (+0.98 %) they fell -12.2 %. The book's mean daily return stays within ±0.06 % in every window, so the short side caught no move larger than its cost.
- **F5:** The other angles I looked at (weekday, raw volatility level, efficiency-ratio level, 30-day move) showed nothing graded that stands out once the number of angles is counted. The largest was a weekday split: Thursday's next day +0.47 % (t 3.19) against Wednesday's -0.49 % (t -2.69), on about 1240 days each. It is not graded and is one of many cuts, so I write no idea from it.

## Ideas
- `032-02.b1.g1_sharp-daily-drop-rebounds` (from F1, F2): When a coin falls sharply in one day compared with its usual daily swing over the past 30 days, it tends to rise over the next day, and the larger the fall in units of that usual swing, the larger the rebound.
- `032-02.b1.g2_calm-chop-weekly-continuation` (from F3, F4): When a coin's past 30 days were choppy but calm, with little net progress and daily swings small for the coin, its move over the past 7 days tends to continue over the next 7 days, and the larger that 7-day move is compared with the coin's usual swings, the larger the continuation.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
