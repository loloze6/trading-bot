---
line: 7.b inconclusive
backtest: 024-02_fading-volume-downrun-rebound-size.d3_trend-strength-lifts-pullback-rebound_4h
idea tested: 024-02_fading-volume-downrun-rebound-size.d3_trend-strength-lifts-pullback-rebound
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3389 USD
---
## Findings
- **F1:** The result sits on the side the idea predicts but short of the bar. My recount of the cases (2,107 cases, mean unusual 18-bar move +0.32 %, t 1.67) matches step 5's figures (2,115 cases, +0.317 %, t 1.65). The size is 0.037 of a usual move, below the ~0.05 of real ideas measured so far, so even this many cases leaves the t under 2.
- **F2:** The effect is graded the way the idea says. By forecast quartile the mean unusual 18-bar move rises steadily: −0.64 % (t −1.92, 526 cases), +0.05 % (t 0.13), +0.32 % (t 0.88) and +1.55 % (t 3.28, 531 cases). By quartile of the raw 30-day rise it also rises, from −0.00 % (t −0.01) to +0.94 % (t 1.78).
- **F3:** The sign holds coin by coin, but no single coin is clear. All six coins show a positive mean unusual move: from +0.09 % on XMR (t 0.23, 363 cases) to +0.71 % on ETH (t 1.66, 341 cases). Each coin has only about 320 to 380 cases, too few to show an effect of this size alone.
- **F4:** The market's own regime drowns the effect in some years. It is negative in the bear years 2018 (−3.13 %, t −3.32, 146 cases) and 2022 (−1.53 %, t −2.91, 187 cases). It is positive in 2020 (+1.26 %, t 2.82), 2021 (+1.70 %, t 2.65) and 2024 (+1.01 %, t 1.98).
- **F5:** The horizon does not explain the unclear result. The mean unusual move is +0.16 % over 6 bars (t 1.57), +0.26 % over 12 bars (t 1.69), +0.32 % over 18 bars (t 1.67) and +0.06 % over 36 bars (t 0.21), so the plan's one-to-three-day horizon is where the effect shows, and it fades by six days.
- **F6:** Nearly all cases come from the shortest streak. Streaks of 2 bars give 1,820 of the 2,107 cases (+0.38 %, t 1.81), and longer streaks are few and not positive (4 bars: −1.08 %, 61 cases). The test therefore measured mostly brief two-bar pullbacks rather than long runs.

## Ideas
- `024-02_fading-volume-downrun-rebound-size.d3_trend-strength-lifts-pullback-rebound.b1_trend-pullback-rebound-more-coins` (from F1, F2, F3): When a coin has risen over the past 30 days and then falls in an unbroken streak of four-hour periods on declining volume, it rises over the next three days. The larger its 30-day rise, the larger that rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
