---
line: 7.d not profitable
backtest: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall.d1_broken-support-without-capitulation_1d
idea tested: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall.d1_broken-support-without-capitulation
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3840 USD
---
## Findings
- **F1:** The book loses because it is short most of the time against coins that rise, and its timing is too small to cover that. It is short on 63 % of bars. Short bars in the normal regime earn -0.000837 per bar in total: -0.001055 from the coin's own rise and only +0.000217 from timing. Their summed gain is -8.59, against +2.93 for the long rebound bars. Per case, the total move is -0.18 %, which is -0.9 times the 0.19 % cost of a trade.
- **F2:** The book is a bet against the market. Its daily return correlates -0.37 with the coins'. It loses in the windows where the coins rise: w11 had coins at +0.0126 a day and the book at -0.0048; w17 had +0.0042 against -0.0047. In 2023 and 2024 it held an average position of -0.83 and -0.78 and lost -0.0022 and -0.0006 a day.
- **F3:** The short pays only after the coin has already fallen over the past 10 days.
- **F4:** The short's move grows with how far the close sits below its 20-day high. By quartile of that distance, shorts earn a total move of +0.80 %, +0.35 %, -1.19 % and -1.23 %, from deepest (-27 %) to nearest (-2 %). The unusual move goes from +2.0 % to -0.04 %, about 196 cases each.
- **F5:** Among shorts after a 10-day fall, the move grows with the forecast's size. By tercile of |forecast|, the total move is -0.08 %, +0.25 % and +1.29 % (unusual +1.11 %, +1.46 %, +2.44 %), about 160 cases each. The top tercile's total move is 6.8 times the cost. The smallest-forecast quartile of all shorts loses -2.07 % (216 cases).
- **F6:** The rebound long after a deep 90-day fall pays when the past 10 days also fell hard.

## Ideas
- `020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall.d1_broken-support-without-capitulation.d1_broken-support-after-decline` (from F1, F2, F3, F4, F5): When a coin's daily close sits just below prices where it turned up several times in the past 90 days, it tends to fall over the next 10 days, only while its 10-day return is a fall. The more such past turning-up lows lie just above the close, and the further the close sits below its 20-day high, the larger the fall, except when its 90-day return is a deep fall, after which it rebounds instead.
- `020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall.d1_broken-support-without-capitulation.d2_capitulation-rebound-after-deep-fall` (from F6, F1): After a coin's 90-day return is a deep fall, the deeper its 10-day fall, the more it rises over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
