---
line: 7.d not profitable
backtest: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall.c1_broken-support-below-average_1d
idea tested: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall.c1_broken-support-below-average
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2540 USD
---
## Findings
- **F1:** The book loses mostly by being short against the coins' rise, not through its timing: per day the book averages -0.040 %, made of -0.059 % from the market's own rise (short in coins that drift up 1.19 % per 10 days), +0.033 % from timing and -0.014 % from costs, with a position on 65 % of days.
- **F2:** On the 627 grid cases with a forecast of -2 or below, the short-direction unusual 10-day move is +0.86 % (t 1.47), but the total move is -0.35 %, so the drift the short gives up outweighs the effect found.
- **F3:** The raw size of the cluster of turning-up lows does grade the fall. In the two upper quartiles of the raw value (mean 0.78 and 2.49), the unusual move is +2.19 % (t 2.27) and +2.24 % (t 2.42) and the total move is +1.01 % and +1.07 %, about 5 times the 0.19 % cost of a trade. In the two lower quartiles (mean 0.17 and 0.37), the unusual move is -0.53 % and -0.47 % and the total move is -1.77 % and -1.72 %.
- **F4:** The forecast loses that grading. A quarter of the cases sit at the cap of -20 and the median is -7.9, and the supporting check found 0 cases above the median, so the book sizes weak clusters about as large as strong ones.
- **F5:** Where the close sits in its 90-day range splits the cases. In the lowest two quartiles of the range position (mean 0.08 and 0.20), the total short move is -1.70 % and -1.45 % and the unusual move is -0.47 % and -0.26 %. In the third quartile (0.32) the unusual move is +3.52 % (t 3.03) and in the top quartile (0.51) +2.11 % (t 1.81).
- **F6:** After a deep 90-day fall the coin rebounds instead of falling. In the lowest quartile of the 90-day return (mean -47 %, 33 cases) the unusual short move is -5.83 % (t -2.09), against +5.26 % (t 3.08) and +4.13 % (t 3.39) in the next two quartiles (-23 % and -6 %). After the steepest 30-day falls (mean -32 %, 117 cases) it is -0.61 %, against +1.7 % to +2.1 % in the other quartiles.
- **F7:** The book's result follows the year's trend. It earns in years when the coins fall: 2018 +0.119 % per day with the coins at -0.347 %, and 2022 +0.148 % with the coins at -0.180 %. It loses in rising years: 2020 -0.112 % (coins +0.423 %), 2021 -0.082 % (+0.409 %), 2023 -0.245 % (+0.150 %) and 2024 -0.180 % (+0.244 %).

## Ideas
- `020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall.c1_broken-support-below-average.d1_broken-support-above-range-low` (from F2, F3, F5, F6): When a coin's daily close sits just below prices where it turned up several times in the past 90 days, it tends to fall over the next 10 days, and the more such past turning-up lows lie just above the close, the larger the fall, only while the close is below its 50-day average and still well above its 90-day low, the farther above that low the larger the fall.
- `020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall.c1_broken-support-below-average.d2_broken-support-in-downtrend` (from F1, F2, F3, F7): When a coin's daily close sits just below prices where it turned up several times in the past 90 days, it tends to fall over the next 10 days, and the more such past turning-up lows lie just above the close, the larger the fall, only while the coin's 200-day average is falling, the faster it falls the larger the fall.
- `020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall.c1_broken-support-below-average.d3_deep-fall-support-rebound` (from F5, F6): When a coin's daily close sits just below a cluster of past turning-up lows after a deep 90-day fall, it tends to rise over the next 10 days, and the deeper its 90-day fall, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
