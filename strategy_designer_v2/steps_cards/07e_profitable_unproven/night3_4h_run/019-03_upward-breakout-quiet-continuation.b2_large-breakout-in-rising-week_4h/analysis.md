---
line: 7.e profitable but not proven
backtest: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week_4h
idea tested: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3954 USD
---
## Findings
- **F1:** The book's gain is mostly timing, not the market's own rise. Summed over bars, the position's gain is 22.3 against 9.7 from the coins' mean drift, so timing is about 12.6. Timing is positive on all 6 coins: XRP +3.61, ETH +3.43, ZEC +2.82, BTC +1.86, LTC +0.52, XMR +0.37.
- **F2:** The gain is concentrated in time and in a few days. 2020 and 2021 bring 12.7 of the 22.3, with book Sharpes of 2.58 and 1.83. 2022 loses (Sharpe -0.86, timing -1.87). The best 5 % of days hold 247 % of the book's summed daily return. Of 3942 trades, 44 % win, and the top 50 hold 2882 of the 6465 net percent (45 %).
- **F3:** The break itself adds nothing over the regime. On non-overlapping 3-day grid bars with a positive 7-day return, bars in an upward break show +0.49 % unusual move (n 292, t 0.79). Bars not in a break show +0.19 % (n 2394, t 1.10).
- **F4:** The 7-day return carries the effect, graded at its top end. Among grid bars with a positive 7-day return, the 3-day unusual move by quartile of that return (mean 1.4 %, 4.4 %, 9.3 %, 24 %) is -0.40 %, -0.01 %, +0.27 % and +1.05 % (t 2.33, n 672). Among the idea's own entries the same quartiles give +0.03 %, +0.45 %, +0.35 % and +1.06 % (t 1.99).
- **F5:** The 7-day return measured in units of the coin's 4h volatility predicts both ways in its tails. Over 3 days the top sextile gives +0.91 % (t 2.67, strength 0.10, n 882). Over 12 days the top sextile gives +3.02 % (t 2.21, strength 0.15, n 210) and the bottom sextile -2.59 % (t -2.59, strength -0.15). Rank correlation over all bars is weak (0.009 at 3 days, 0.047 at 12 days).
- **F6:** The idea's move outlasts its 3-day horizon. Mean unusual move of entries: 1 day +0.09 % (t 0.85), 3 days +0.43 % (t 2.34), 6 days +0.56 % (t 2.16), 12 days +1.22 % (t 2.79). Case counts are 2446, 2409, 2358 and 2248.
- **F7:** The plan's grading check could not be read because the forecast is capped. 3 of 4 forecast quartiles of entries sit at the cap of 20, and their unusual moves are +0.44 %, -0.34 % and +1.17 %, not ordered.
- **F8:** In a rising week, the deepest pullback below the prior 2-day high is followed by the largest rise. On grid bars with a positive 7-day return, the lowest quartile of (close minus 2-day high) in 30-day mean 4h ranges (mean -3.65 ranges) shows +1.81 % over 3 days (t 4.23, strength 0.21, n 557). That is 9.5 times the 0.19 % cost of a trade. The middle quartiles give -0.23 % and -0.50 %, and the break quartile +0.50 % (t 1.24).
- **F9:** The momentum effect leans on one coin and two years. In the top third of the volatility-scaled 7-day return, XRP gives +2.17 % over 3 days (t 2.49) while the other coins sit between -0.01 % and +0.37 %. 2021 gives +1.61 % (t 2.37) and 2022 gives -1.35 % (t -2.39).

## Ideas
- `019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e1_volatility-scaled-weekly-momentum-continuation` (from F1, F3, F4, F5): The larger a coin's 7-day return, measured in units of its own 4h volatility, the more the coin rises over the next three days.
- `019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e2_pullback-inside-rising-week` (from F3, F8): While a coin's 7-day return is positive, the farther its 4h close sits below the highest high of the preceding two days, measured in its 30-day average 4h range, the more the coin rises over the next three days.
- `019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e3_weekly-momentum-over-twelve-days` (from F5, F6): The larger a coin's 7-day return, measured in units of its own 4h volatility, the more the coin rises over the next twelve days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
