---
line: 7.g patterns
backtest: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around_1d
idea tested: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3272 USD
---
## Findings
- **F1:** The tested forecast does not grade the coming 5-day excess return. Over its quintiles (about 612 non-overlapping cells each) the means run -0.09 %, -0.24 %, +0.72 %, -0.56 %, +0.18 %, with no t beyond ±1.54. Its rank correlation with the excess return goes both ways across coins (-0.045 to +0.085), which fits step 5's t of 0.31.
- **F2:** A coin's 1-day return divided by its 20-day volatility, read at the close, predicts the next 5 days. The top quintile is followed by a 5-day excess return of +1.56 % (t 2.86, 510 non-overlapping cases), about 0.15 of the coin's usual 5-day move (10.60 %) and about 8 times the 0.19 % cost of a trade; the other four quintiles lie between -0.73 % and +0.02 %.
- **F3:** The F2 effect is graded and fairly broad. Among positive readings only, the Spearman correlation of the standardised 1-day rise with the next 5-day excess return is +0.065 (1231 cases, t about 2.3). The top quintile's mean is positive in 5 of 6 coins (BTC +1.52 %, ETH +0.96 %, XMR +0.53 %, XRP +3.00 %, ZEC +3.60 %; LTC -0.31 %) and in 7 of 8 years (2022 -1.13 %).
- **F4:** The raw 1-day return without volatility scaling shows no clean grading. Its quintile means are +0.69 %, -1.47 %, -0.10 %, -0.45 %, +0.99 %, and its per-coin rank correlations run from -0.067 to +0.018. Only scaling by the coin's recent volatility orders the effect into one tail.
- **F5:** The day of the week shows a seasonal pattern that the idea does not explain. Saturday's 1-day excess return is +0.31 % (t 3.61, 2225 days), and Monday plus Tuesday against Saturday plus Sunday differs by Welch t -3.16. That difference is negative in 7 of 8 years. It is not graded, so it supports no idea here.
- **F6:** The book's gain comes from being long, not from the tested timing. Its 1419 LONG trades average +4.70 % net and its 1424 SHORT trades average -3.98 % net, over trades lasting 20.4 days on average. The book's daily returns correlate only 0.09 with the coins' daily returns.

## Ideas
- `022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.g1_volatility-scaled-up-day-continuation` (from F2, F3, F4): The larger a coin's 1-day rise measured against its own 20-day volatility, the higher its return over the next 5 days, relative to its usual 5-day drift.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
