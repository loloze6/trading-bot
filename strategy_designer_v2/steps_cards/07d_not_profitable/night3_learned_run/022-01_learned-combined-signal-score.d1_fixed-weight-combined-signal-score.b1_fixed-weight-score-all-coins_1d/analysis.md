---
line: 7.d not profitable
backtest: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b1_fixed-weight-score-all-coins_1d
idea tested: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b1_fixed-weight-score-all-coins
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4389 USD
---
## Findings
- **F1:** The book fails on mean daily return (0.000301, against a floor of 0.0005), and the reason is that it is barely invested. Its mean absolute allocation is 0.16 of the book, and it is short 50 % of bars and long 47 %, so its net position is near zero (mean allocation +0.004). Holding the coins earned 0.00134 a day, 4.5 times the book.
- **F2:** The shorts carry about half the book's time but almost none of its gain. Short bars add 0.000028 of the 0.000322 gross gain per bar, against 0.000293 from long bars. Short trades average +0.10 % net (5081 trades), long trades +7.79 % net (5610 trades).
- **F3:** Shorts are paid for by falling years and lost in rising ones. Short-bar gain per bar is +0.00044 in 2018 and +0.00042 in 2022, but −0.00053 in 2023 and −0.00042 in 2024, when holding earned +0.32 % and +0.28 % a day. Being short against the coins' rise costs 0.000109 per bar.
- **F4:** The negative-score cases are not falls in total. Coins still rose +0.36 % over 5 days after them (3523 cases), against +1.15 % after positive scores. Most of what a short captures is the unusual move (−0.40 %), not a decline, so the short side's total move is small next to the 0.22 % round trip.
- **F5:** Two of the four signals carry the edge and the other two dilute it. On the 7128 non-overlapping 5-day cases, the score-times-excess-return t is 3.37 for 28-day momentum and 1.85 for nearness to the 90-day high. It is −0.99 for 1-day reversal (the wrong sign) and −0.21 for low volatility.
- **F6:** Momentum and nearness together predict better than the full score. Their average alone has t 3.63, against 2.82 for the four-signal forecast (7128 cases; correlation between the two scores 0.78).
- **F7:** Momentum plus nearness separates mainly at its upper half. The two top quintiles of the momentum-plus-nearness score are followed by +0.78 % and +0.97 % excess over 5 days (total +1.55 % and +1.73 %). The three lower quintiles are followed by −0.37 % to −0.71 %, while still rising +0.08 % to +0.35 % in total.
- **F8:** Low volatility is not graded. Excess 5-day return by volatility-score quintile runs +0.48 %, −0.07 %, −0.30 %, −0.73 %, +0.62 %, so the calm signal adds noise rather than a graded effect.
- **F9:** The idea's size covers its cost: its unusual move per case is +0.93 % over 5 days, 4.1 times the 0.22 % round trip (strength 0.072). The book's trades last 10 to 11 days, about twice the 5-day horizon, in line with earlier runs' finding that continuation moves outlast their stated horizon (findings F9, F11).

## Ideas
- `022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b1_fixed-weight-score-all-coins.d1_momentum-and-nearness-score` (from F1, F5, F6, F8): When a coin's signals are combined into one score, its return over the next 5 days is higher the higher the score, but only its 28-day return and its closeness to its 90-day high are kept. The other two signals, minus its last 1-day return and minus its 30-day volatility, are given no weight, so the rise grows with how strong its recent trend is and how near it trades to its high.
- `022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b1_fixed-weight-score-all-coins.d2_trend-near-high-rises` (from F2, F4, F7, F9): The higher a coin's 28-day return and the closer its close to its 90-day high, the more the coin rises over the next 10 days.
- `022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b1_fixed-weight-score-all-coins.d3_low-scores-fall-in-downtrends` (from F2, F3, F4): When a coin's four signals are combined into one score, its return over the next 5 days is higher the higher that score is. The four signals are its 28-day return, minus its last 1-day return, its closeness to its 90-day high and minus its 30-day volatility, each weighted equally in its known direction. The fall after a low score is larger the more negative the coin's own 90-day return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
