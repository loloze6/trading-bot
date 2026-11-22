---
line: 7.b inconclusive
backtest: 024-02_fading-volume-downrun-rebound-size.d3_trend-strength-lifts-pullback-rebound.e2_rising-volume-pullback-rebound-week_4h
idea tested: 024-02_fading-volume-downrun-rebound-size.d3_trend-strength-lifts-pullback-rebound.e2_rising-volume-pullback-rebound-week
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3418 USD
---
## Findings
- **F1:** The main measure sits on the side the idea predicts but is short of the bar: the mean 42-bar (7-day) unusual move is +0.46 % per case with t 1.23 over 1,360 independent cases, a strength of 0.036 of the coin's usual move (12.42 %), and the total move of +1.47 % is 7.6 times the 0.19 % cost of a trade.
- **F2:** The effect is clearer at shorter horizons than the plan's seven days: over 18 bars (3 days) the unusual move is +0.54 % with t 2.37 over 1,397 cases (strength 0.067, t 2.50), and over 6 bars (1 day) it is +0.27 % with t 1.95 over 1,415 cases. Over 42 bars it is +0.46 % (t 1.23), and over 84 bars +0.63 % (t 1.07): the move grows little after three days while the market's noise grows.
- **F3:** The supporting check could not be computed because 77 % of cases have a forecast at the +20 cap, so the median equals the cap and no case is above it. On the recorded size of the volume-rise component, the larger half beats the smaller half by +0.77 % at 42 bars. That grading comes from the weakest quartile alone: it loses −1.23 % (t −1.87, 335 cases), while the other three gain +1.36 %, +0.89 % and +0.80 %.
- **F4:** The 7-day effect is mixed across years: 2018 −4.66 % (t −2.68, 105 cases), 2020 +2.40 % (t 2.45, 215 cases), 2021 +2.51 % (t 1.70), and 2019, 2022 and 2023 between −0.56 % and −0.31 %. Part of the result is drowned by a few years' market moves.
- **F5:** No single coin carries the 7-day result. Five of six coins are positive at 42 bars, with none reaching t 1.05: BTC +0.59 % (250 cases), ETH +0.69 %, ZEC +1.21 %, XMR −0.06 %, XRP +0.02 %. At 18 bars all six are positive, ETH reaching t 2.17.

## Ideas
- `024-02_fading-volume-downrun-rebound-size.d3_trend-strength-lifts-pullback-rebound.e2_rising-volume-pullback-rebound-week.b1_rising-volume-pullback-more-coins` (from F1, F4, F5): When a coin with a positive 30-day return falls in a streak of four-hour periods on rising volume, it rises over the next seven days, and the more the volume rose across the streak, the larger that rise.
- `024-02_fading-volume-downrun-rebound-size.d3_trend-strength-lifts-pullback-rebound.e2_rising-volume-pullback-rebound-week.b2_rising-volume-pullback-three-days` (from F2, F3, F5): When a coin with a positive 30-day return falls in a streak of four-hour periods on rising volume, it rises over the next three days, and the more the volume rose across the streak, the larger that rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
