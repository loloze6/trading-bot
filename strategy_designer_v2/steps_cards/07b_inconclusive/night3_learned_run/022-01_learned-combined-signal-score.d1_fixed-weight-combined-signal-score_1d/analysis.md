---
line: 7.b inconclusive
backtest: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score_1d
idea tested: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3246 USD
---
## Findings
- **F1:** The result is on the side the idea predicts but too small for this grid to show: the mean product is +0.0065 (t 1.21, 3419 cases), and the forecast's top fifth is followed by +0.62 % above drift over 5 days against −0.10 % for its bottom fifth, with the quintiles in between not ordered (−0.61 %, +0.23 %, −0.14 %).
- **F2:** The t depends on which day the 5-day grid starts: moving the grid's start by 1 to 4 days gives t 2.37, 2.63, 3.15 and 1.43 (3307 to 3407 cases), so the plan's grid (phase 0, t 1.21) is the weakest of the five, not a typical reading.
- **F3:** At horizons other than 5 days the same forecast clears t 2: t 5.05 at 1 day (17380 cases), 3.45 at 2 days, 3.23 at 3 days, 2.81 at 10 days (1691 cases) and 2.33 at 20 days (827 cases).
- **F4:** Of the four signals, the 28-day return carries the score at 2 to 10 days (t 1.95 to 2.68), and closeness to the 90-day high adds a little (t 0.83 to 1.65). Together they reach t 2.24 to 2.72 from 2 to 10 days. The short reversal shows only at 1 day (t 5.10; −1.47 at 5 days), and minus volatility shows at no horizon (t −0.55 to −0.00).
- **F5:** The effect is uneven across coins and periods: at 5 days ETH has t 2.48 and XMR −1.18, the year 2020 has t 3.25 and 2023 has −3.30, and at 10 days windows w13–w24 give t 3.67 while w1–w12 give 0.03.
- **F6:** Size against cost: the unusual move is +0.96 % per case over 5 days, a strength of 0.082 and 5.0 times the 0.19 % round trip. Over 10 days it is +0.83 % in the signal's direction, against a usual move of 15.9 %. The book's Sharpe is 0.94, 0.38 above holding, and it fails only on mean daily return (0.00029) and Calmar (0.75).

## Ideas
- `022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b1_fixed-weight-score-all-coins` (from F1, F2, F5, F6): When a coin's four signals are combined into one score, the coin's return over the next 5 days is higher the higher that score is. The four signals are its 28-day return, minus its last 1-day return, its closeness to its 90-day high, and minus its 30-day volatility. Each signal is weighted equally in the direction its effect is known for, instead of by how well it predicted that coin's own 5-day returns over the past 365 days.
- `022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b2_momentum-near-highs-ten-days` (from F3, F4, F6): The higher a coin's 28-day return plus its closeness to its 90-day high, the higher its return over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
