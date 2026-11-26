---
line: 7.g patterns
backtest: 032-03.b1_thin-volume-decline-more-coins_1d
idea tested: 032-03.b1_thin-volume-decline-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4180 USD
---
## Findings
- **F1:** Inside 28-day declines, the 5-day return minus drift is not graded by the depth of the fall. Across quintiles of the 28-day return (deepest first) it was -0.07 % (t -0.03), -2.18 % (t -1.52), -2.94 % (t -2.56), -1.26 % (t -1.01) and +0.47 % (t 0.49), on 167 cases each. The linear slope of that return on the 28-day return was -0.019 (t -0.26, 835 cases on 171 days).
- **F2:** Moderate declines (28-day return between -30 % and -12 %) were followed by a negative 5-day return minus drift in every year: -3.4 % (t -2.00, n 100) in 2018, -1.7 % (t -1.40, n 112) in 2019, -3.6 % (t -0.68, n 29) in 2020 and -2.9 % (t -1.34, n 101) in 2021. Falls deeper than -30 % were followed by -0.42 % (t -0.19, 202 cases on 58 days). I chose this band after seeing F1, so it cannot be told from chance.
- **F3:** The recorded thin-volume value does not grade the further fall inside declines. Its quintiles gave 5-day returns minus drift of -1.38 %, -1.53 %, -2.15 %, -0.96 % and +0.05 %, with a slope t of 0.65 (835 cases, 171 days). Measured the same way, the 28-to-42-day volume ratio had a slope t of 0.58 and the 7-to-28-day volume ratio a slope t of 1.32.
- **F4:** Splitting declines by the change in daily range (calm against panic, at the median) does not separate them.
- **F5:** No other angle stood out. The strongest results were:
- **F6:** The book's largest days are coin moves against the short, so its gains and losses net out.

## Ideas
- No ideas: Across about 60 groupings and slopes (depth of the decline, volume and range ratios over several spans, calm against panic, volatility, past returns, weekday, year), no pattern exceeded a t of about 2.6, which is what chance gives among that many looks. The one consistent shape, moderate declines continuing while deep ones do not, was chosen after seeing the data and was never tested on its own.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
