---
line: 7.g patterns
backtest: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b2_false-breakout-in-downtrend.d1_false-break-while-month-falls_1d
idea tested: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b2_false-breakout-in-downtrend.d1_false-break-while-month-falls
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4974 USD
---
## Findings
- **F1:** A close far above the coin's highest close of the previous 90 days is followed by an unusually large rise. Closes 8 to 20 % above that high end 12.3 % above the coin's 10-day drift (strength 0.67, t 2.86, 38 cases, positive in 71 % of 14 windows, t across windows 2.57). Over 5 days the same closes end 6.9 % above drift (strength 0.48, t 2.31, 58 cases). The 5 closes more than 20 % above the high end 35 % above drift over 10 days (strength 1.58).
- **F2:** Any fresh close above the previous 90-day high is followed by a 10-day excess rise of +3.4 % (strength 0.22, t 2.66, 197 non-overlapping cases). All other bars show -0.2 % (strength -0.01, t -0.76, 3354 cases). Such breaks never occur with a negative 30-day return, so the tested idea's falling-month breaks are a different, weaker situation.
- **F3:** The continuation is graded by recent strength on the coin's own bars. The top fifth of the 30-day return ends +3.2 % above 10-day drift (strength 0.17, t 3.21, 532 cases). The top fifth of nearness to the 90-day high ends +2.6 % (strength 0.14, t 3.03). The rank correlation of nearness with the 10-day excess move is 0.049 (p 0.012, 2645 cases). The grading is not monotone below the top fifth: the second fifth of the 30-day return shows -0.13, t -3.9.
- **F4:** The tested fade fights both the drift and this continuation. Its 106 cases have a total move of -1.01 % per case, -4.5 times the 0.22 % cost of a round trip. Its unusual move of +0.30 % (strength -0.038) is inside chance (t 0.97). The book's 187 shorts lost 3.86 % each after fees (median -2.07 %), for a Sharpe of -0.34.
- **F5:** The size of F1's move covers the cost many times over. +12.3 % unusual over 10 days, and +3.4 % for every break in F2, against a 0.22 % round trip, is more than 15 times the cost. This is unlike the tested idea's 1.3 times.
- **F6:** The other angles I looked at did not hold up once each day was counted once:

## Ideas
- `020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b2_false-breakout-in-downtrend.d1_false-break-while-month-falls.g1_wide-90-day-high-breaks-continue` (from F1, F2, F3, F5): When a coin closes above its highest close of the previous 90 days, it keeps rising over the next 10 days by more than its normal drift. The farther its close sits above that previous high, the larger the rise.
- `020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b2_false-breakout-in-downtrend.d1_false-break-while-month-falls.g2_nearness-to-90-day-high` (from F3, F4, F2): The nearer a coin's close is to its highest close of the past 90 days, the more it rises over the next 10 days beyond its normal drift.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
