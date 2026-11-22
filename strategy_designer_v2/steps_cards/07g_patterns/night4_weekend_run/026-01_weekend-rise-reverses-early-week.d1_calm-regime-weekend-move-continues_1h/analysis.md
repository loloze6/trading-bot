---
line: 7.g patterns
backtest: 026-01_weekend-rise-reverses-early-week.d1_calm-regime-weekend-move-continues_1h
idea tested: 026-01_weekend-rise-reverses-early-week.d1_calm-regime-weekend-move-continues
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4236 USD
---
## Findings
- **F1:** Over the two hours after the 21:00 UTC close, every coin rises on average. BTC +0.085 % (t 4.69, 2886 cases), ETH +0.112 % (t 4.84), LTC +0.096 % (t 3.75), XMR +0.095 % (t 3.53), XRP +0.090 % (t 2.99) and ZEC +0.110 % (t 3.26). The next-hour returns after the 21:00 and 22:00 closes are the two strongest hours of the day (+0.0545 %, t 6.75; +0.0436 %, t 5.66). The rise holds in 6 of 8 years and in windows w7 to w24 (t 4.47 to 7.23), but it is absent in windows w1 to w6 (−0.006 %, t −0.31) and in 2022 (−0.043 %, t −1.41).
- **F2:** The evening rise is graded by the coin's return from 14:00 to 21:00 UTC. In the quintile with the largest falls it is +0.272 % (t 8.47, 3394 cases), then +0.116 % (t 5.95), +0.056 % (t 3.18), +0.023 % (t 1.14) and +0.022 % (t 0.80) in the quintile with the largest rises.
- **F3:** A day's move reverses the next day only when 30-day volatility is high against its own history. In the top volatility-ratio quintile the slope of the next 24-hour return on the past 24-hour return (both in volatility units) is −0.136 (t −6.48, 1721 cases), against −0.014 to +0.044 (|t| ≤ 1.45) in the other four quintiles. In the high-volatility tercile it is negative for all six coins, with t ≤ −2.0 for ETH, LTC, XMR and ZEC, and with t ≤ −2.48 in 2018, 2019 and 2023.
- **F4:** In calm volatility (ratio ≤ 1), the 48-hour move from Wednesday 00:00 to Friday 00:00 continues over Friday and Saturday: slope +0.161 (t 4.73, 595 cases), sign-weighted move +0.096 usual moves (t 2.97). The same 48-hour test on Mondays in calm gives slope +0.076 (t 1.07, 627 cases). This is the strongest of the 14 weekday × volatility cells.
- **F5:** The tested Monday continuation is not graded by the weekend move's size. By size tercile of the weekend move, the sign-weighted move is +0.095 (t 2.83) for the smallest, +0.058 (t 1.65) for the middle and −0.035 (t −0.78) for the largest. It shows in the low-volatility tercile only (slope +0.172, t 2.04), against −0.082 and −0.017 in the mid and high terciles.

## Ideas
- `026-01_weekend-rise-reverses-early-week.d1_calm-regime-weekend-move-continues.g1_late-evening-rebound-after-afternoon-fall` (from F1, F2): The more a coin has fallen over its 7 hours to 21:00 UTC, the more it rises over the next 2 hours.
- `026-01_weekend-rise-reverses-early-week.d1_calm-regime-weekend-move-continues.g2_turbulent-daily-moves-reverse` (from F3): When a coin's 30-day hourly volatility is high against its own last 6 months, its 1-day move is partly reversed over the next day. The higher that volatility ratio and the larger the move, the larger the reversal.
- `026-01_weekend-rise-reverses-early-week.d1_calm-regime-weekend-move-continues.g3_calm-mid-week-move-continues` (from F4, F5): When a coin's 30-day hourly volatility is low against its own last 6 months, its move from Wednesday 00:00 to Friday 00:00 UTC continues in the same direction over Friday and Saturday. The larger that move, the larger the continuation.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
