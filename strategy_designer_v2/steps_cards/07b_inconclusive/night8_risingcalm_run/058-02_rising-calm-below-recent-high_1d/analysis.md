---
line: 7.b inconclusive
backtest: 058-02_rising-calm-below-recent-high_1d
idea tested: 058-02_rising-calm-below-recent-high
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3443 USD
---
## Findings
- **F1:** The test's result points against the idea. Inside the rising calm profile, on the 5-day grid of folds B and C, the scaled dip below the 5-day closing high has a negative slope on the 5-day excess return: t -3.15 on the raw dip (284 cases, 109 days) and t -1.89 on the forecast (333 cases). Step 5's own measure was t -1.67, with a forecast-weighted mean excess of -0.28 %.
- **F2:** The deepest dips are followed by further falls, not recoveries. Across in-profile dip quintiles at 5 days, the excess return runs +2.5 %, +4.9 %, +2.7 %, +0.1 % and -2.0 % (raw return +3.2 % down to -1.3 %, about 57 cases each). The shallow half earns +3.4 % in excess (t 2.56, 142 cases) and the deep half -0.2 % (t -0.21, 142 cases).
- **F3:** The negative grading is not confined to one coin or one year. The in-profile 5-day dip slope is negative on all six coins (ETH t -2.46, XMR t -2.08, LTC -1.72, XRP -1.42, ZEC -1.41, BTC -0.60) and in every year with enough cases (2019 t -2.07, 2020 -1.56, 2021 -1.00).
- **F4:** The idea's recovery does not appear at another horizon either. In profile, the dip slope's t is +1.47 at 1 day, +0.20 at 2 days, +0.89 at 3 days and -1.09 at 7 days, all short of 2. The 5-day return scaled by the swing gives no clear slope at any horizon, with t between 0.23 and 1.43.
- **F5:** The continuation after a deep dip is not special to rising calm markets. Outside the profile, the 5-day dip slope is also negative in choppy markets (t -2.31, 125 cases), falling markets (t -2.24, 369 cases) and rising markets outside the calm state (t -1.43, 140 cases).
- **F6:** The idea's size is not what keeps the book from paying, but this data does not support it. The unusual move is +0.44 % per case (t 0.77, 413 days), 0.044 of a usual 10.60 % move. That is 2.3 times the 0.19 % cost of a trade, yet the move comes from the shallow dips (F2), not from the graded deep ones.

## Ideas
- `058-02.b1_rising-calm-deep-dips-extend` (from F1, F2, F3): In a rising, calm market, the further a coin's close sits below its highest close of the past 5 days, measured against its usual daily swing over the past 30 days, the larger its fall over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
