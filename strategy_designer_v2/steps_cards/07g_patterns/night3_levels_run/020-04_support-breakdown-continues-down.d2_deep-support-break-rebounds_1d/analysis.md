---
line: 7.g patterns
backtest: 020-04_support-breakdown-continues-down.d2_deep-support-break-rebounds_1d
idea tested: 020-04_support-breakdown-continues-down.d2_deep-support-break-rebounds
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3206 USD
---
## Findings
- **F1:** A large up day, measured against the coin's own volatility, was followed by an unusual 5-day rise. On the 5-day grid, the top decile of the 1-day return divided by its 20-day volatility had a strength of 0.197, which is +2.42 % unusual per case (t 3.40, 317 cases). That is about 12 times the 0.19 % cost of a trade. The top fifth had a strength of 0.151 (t 3.67, 629 cases). The middle deciles sat near 0 or below. Decile 7 was -0.106 (t -2.1), so the rise is not smooth until the top two deciles.
- **F2:** The large-up-day effect is fragile across grid phases. Measured from each of the 5 possible grid starts, the top fifth had strengths of 0.151, 0.010, 0.090, -0.023 and 0.026. Only phases 0 and 2 reach t ≥ 2 (3.67 and 2.17). The phase-averaged strength is about 0.05, which is still about 0.5 % per case against the 0.19 % cost. After the many angles looked at, this is the only pattern that stands out, and only weakly.
- **F3:** The effect is broad but not universal. The top-fifth strength is positive on 5 of 6 coins: BTC 0.216 (t 2.19), XRP 0.229 (t 2.00), ZEC 0.266 (t 2.09), ETH 0.103, XMR 0.105, and LTC -0.016. It is positive in 5 of 8 years, at 0.26 to 0.39 in 2019 to 2021 and slightly negative in 2018, 2022 and 2025. Among up days, the grade holds within coins: the correlation of size with the following move is 0.01 to 0.15, positive on all 6 coins.
- **F4:** A wide day that closes up is followed by the same rise, so it is the same signal seen through the range. The top decile of range over volatility, signed by the day's direction, had a strength of 0.189 (t 3.19, 317 cases). The unsigned range top fifth had 0.102 (t 2.62).
- **F5:** The tested situation (a close below a much-touched support) was followed by slightly less than the coin's usual move, not a rebound. Cases with a positive forecast had a strength of -0.027 (t -1.38, 2346 cases), against +0.059 when the forecast was flat. This agrees with the verdict: -0.19 % unusual per case, a total move of +0.39 %, 2 times cost, carried by drift.
- **F6:** Closes near the top of the 30-day range were followed by a mild 5-day rise. The top fifth by position in the 30-day range had a strength of 0.089 (t 2.00, 600 cases), against -0.056 and -0.082 in the two lowest fifths. This is consistent with earlier findings that nearness-to-highs pays on daily bars (findings F3, F9).
- **F7:** The weekday pattern is an artefact of the grid, not a market effect. Monday and Tuesday starts looked strong on phases 0 and 1 (t 3.9 and 3.5) but reversed on phase 2 (t -3.2). Volatility level, the 5-day past return and the volume surge showed no fifth with |t| ≥ 2 for 5-day volatility and 5-day return, and none at all for volume.

## Ideas
- `020-04_support-breakdown-continues-down.d2_deep-support-break-rebounds.g1_strong-up-day-continues` (from F1, F2, F3, F4): When a coin closes a day up by a large multiple of its usual daily move over the past 20 days, it tends to keep rising over the next 5 days, and the larger that day's rise relative to its usual move, the larger the rise that follows.
- `020-04_support-breakdown-continues-down.d2_deep-support-break-rebounds.g2_near-monthly-high-continues` (from F6, F1): When a coin closes near the top of its 30-day price range, it tends to rise over the next 5 days, and the closer its close to the 30-day high, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
