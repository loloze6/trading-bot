---
line: 7.b inconclusive
backtest: 032-02.b2.d1_volatile-ten-day-low-rebound_1d
idea tested: 032-02.b2.d1_volatile-ten-day-low-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3337 USD
---
## Findings
- **F1:** The result is unclear because step 5 could not measure its supporting check, not because the effect is weak: the main measure is on the predicted side (+2.04 % unusual 1-day move, t 2.48 over 124 case days, 195 cases), but the deeper-minus-shallower check came back "None", since `debug_info.components` is not recorded in this backtest (the first sample read "{}" and the column was missing in round 2).
- **F2:** When the depth is recomputed from prices (prior 10-day low minus close, in 30-day mean daily ranges), the idea's grading shows in folds B and C, with some noise: over 99 cases on 53 days (mean +3.94 %, t 2.82, 69 % positive), depth correlates 0.54 with the unusual move, and the deep tercile gains +6.24 % against +2.09 % for the shallow one, but the middle tercile is at −0.30 % and the deep tercile's t is only 1.54 on 11 days.
- **F3:** The recorded forecast, standardised over its own past 60 values, grades the move worse than the raw depth: its correlation with the unusual move is −0.05, against 0.54 for depth, and its terciles read +2.69 %, +2.24 % and +6.89 %.
- **F4:** The rebound appears on every coin but not in every period: all six coins are positive (ZEC +6.01 % t 3.81, ETH +3.34 % t 2.41, XRP +6.87 % t 2.09, BTC +1.71 % t 1.37, LTC +1.86 % t 0.99, XMR +5.67 % t 1.38), while by year it is +1.11 % in 2018, −0.06 % in 2019, +7.56 % (t 2.39) in 2020 and +4.92 % in 2021.
- **F5:** The rebound is largest in the mildest 30-day falls: +6.50 % (t 1.73, 23 cases) in that tercile, against +0.85 % and +0.67 % in the middle and deepest-fall terciles, so the move is not drowned by the market's fall but sits mostly in shallower declines.

## Ideas
- `032-02.b2.d1.b1_volatile-ten-day-low-rebound-wider` (from F1, F2, F4): In a coin that has fallen over the past 30 days and whose daily high-low ranges over that month are wide compared with its own past year, a close below its lowest low of the prior 10 days is followed by a rise over the next 1 day. The further that close sits below the prior 10-day low, measured in units of the coin's mean daily high-low range over the past 30 days, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
