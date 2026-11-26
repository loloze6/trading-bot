---
line: 7.g patterns
backtest: 031-01.b2.b1_long-up-streaks-ten-day-continuation_1d
idea tested: 031-01.b2.b1_long-up-streaks-ten-day-continuation
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3775 USD
---
## Findings
- **F1:** A coin's one-day fall, scaled by its own 20-day daily volatility, is followed by a next-day rebound that grows with the fall. The slope of next-day excess return on the scaled return, over all down days, has t -4.63 (n 6849, r -0.056). The lowest decile then gains +0.107 of a usual daily move (t 3.48, 1397 cases). The second-lowest gains +0.053 (t 2.05). Deciles 3 to 10 sit between -0.05 and +0.01.
- **F2:** That next-day rebound after the largest scaled falls is about +0.51 % above the coin's mean daily return, which is 2.7 times the 0.19 % cost of a trade. It is positive on all six coins (from +0.074 to +0.198 usual moves; XMR t 2.96). It is positive in 7 of 8 years (2020 +0.33, t 3.07; 2021 +0.23, t 2.30; 2024 -0.01).
- **F3:** On the non-overlapping 10-day grid, closes in the top fifth of nearness to the 30-day high are followed by a 10-day excess return. Raw nearness gives +0.194 usual moves (t 2.74, 247 cases). Nearness in units of 20-day volatility gives +0.161 (t 2.26, 247 cases), which is about +2.68 % above drift. The other four quintiles all sit between -0.08 and -0.02. The effect is positive on all six coins (+0.02 to +0.42) but uneven by year (2023 -0.16, 2018 -0.96 on 5 cases), so it is weaker evidence than F1.
- **F4:** The tested streak idea carries no move of its own: its unusual move is -0.21 % per case (t -0.34, 596 days), against a total move of +1.13 % that is almost entirely the coins' drift (+1.33 %). The book's beta to holding its coins is 0.44, and its mean daily return of 0.078 % is below holding's 0.123 %. Its Sharpe edge (0.74) comes from holding about 0.44 of the market at half the volatility (1.99 % against 4.04 % a day), not from timing.
- **F5:** Excess returns by signed streak on the 10-day grid do not rise steadily with streak length. A 1-day up close is followed by -0.112 usual moves (t -2.31, 358 cases), 3 days up by +0.284 (t 2.64, 77 cases) and 4 or more by +0.192 (t 1.62, 98 cases). Up streaks are a noisy subset of the near-30-day-high situation in F3.
- **F6:** Next-day excess return varies by weekday: Wednesday -0.070 (t -3.02), Monday -0.045 (t -2.29), Friday +0.059 (t 3.63). Monday and Friday keep their sign in both halves of the period, but Wednesday's size shrinks from -0.105 to -0.036. This is an ungraded calendar effect, so I do not turn it into an idea.

## Ideas
- `031-01.b2.b1.g1_next-day-rebound-after-sharp-falls` (from F1, F2): The larger a coin's one-day fall, measured in units of its own daily volatility over the past 20 days, the more it rises over the next day.
- `031-01.b2.b1.g2_near-high-ten-day-continuation` (from F3, F5, F4): The closer a coin closes to its highest close of the past 30 days, measured in units of its own daily volatility over the past 20 days, the more it rises over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
