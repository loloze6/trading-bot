---
line: 7.g patterns
backtest: 031-04_down-streak-length-continuation_1d
idea tested: 031-04_down-streak-length-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3566 USD
---
## Findings
- **F1:** The book's loss comes from the market's own rise, not from timing. It held a short on 92 % of coin-days, with a mean position of -0.78. Its mean daily return of -0.097 % (t -1.84) splits into -0.100 % from the coins' drift and +0.014 % from timing (t 0.26).
- **F2:** Down streaks are not followed by graded continuation. On the 5-day grid the unusual move after a down streak shows no order with length:
- **F3:** Next-day moves run against the last day's move, measured in the coin's own 30-day daily volatility, and the effect is graded.
- **F4:** The reversal fades with the horizon. Over 3 days the correlation is weaker: -0.048 (p 0.002) for the last day's return and -0.034 (p 0.03) for the run's return, on 4,026 cases. Over 5 days it is gone or turned: +0.023 (p 0.27) and +0.018 (p 0.38), on 2,346 cases.
- **F5:** The other angles show no pattern that stands out once the number of cuts is counted:

## Ideas
- `031-04.g1_one-day-volatility-scaled-reversal` (from F3, F4): The larger a coin's return on its last day, measured against its own daily volatility over the past 30 days, the more the coin moves the opposite way over the next 1 day. A large down day is followed by a rise above its drift, and a large up day by a weaker day.
- `031-04.g2_run-depth-short-horizon-reversal` (from F3, F4, F2): The larger the total return of a coin's current run of same-direction daily closes, measured against its own 30-day volatility, the more the coin moves against that run over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
