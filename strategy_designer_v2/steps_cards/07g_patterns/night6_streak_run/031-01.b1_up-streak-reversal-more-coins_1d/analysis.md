---
line: 7.g patterns
backtest: 031-01.b1_up-streak-reversal-more-coins_1d
idea tested: 031-01.b1_up-streak-reversal-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3910 USD
---
## Findings
- **F1:** Almost all of the book's loss comes from the market's own rise, not from timing. The position was short on 93.7 % of coin-bars with a mean allocation of -0.74. The mean gain per coin-bar was -0.1008 %, of which the market part was -0.1012 % and the timing part +0.0004 %, so the up-streak forecast added nothing over being short all the time.
- **F2:** The idea's own signal shows no graded edge. On the short side, the forecast quartiles' mean unusual 5-day moves were -0.11 %, +0.50 %, +0.73 % and -0.54 % from least to most short (t between -0.65 and 0.93, about 760 cases each), which is not monotonic.
- **F3:** The signed streak length predicts nothing over the next 5 days in either direction. No streak length from -6 to +6 reaches |t| 2: the largest were -1.96 after 4-day down streaks (139 cases, 64 days) and +1.83 after 3-day down streaks (385 cases, 136 days). These have opposite signs at neighbouring lengths, and up streaks of 3 to 6 days have t between -0.79 and +0.95.
- **F4:** Neither the size of the run nor its context sorts the next 5 days, and some splits run opposite to their neighbours:
- **F5:** The other angles give nothing either:

## Ideas
- No ideas: Across roughly 90 groupings over 3 rounds (streak length and sign, run size, day's move, 5- and 20-day returns, volatility regime, weekday, year, coin and forecast quartile), the one |t| above 2 (-2.52) was ungraded and sat between neighbours of the opposite sign, which is what chance produces among that many looks. The book's loss is simply the cost of being short a rising market (F1), so no pattern stands out enough to support an idea.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
