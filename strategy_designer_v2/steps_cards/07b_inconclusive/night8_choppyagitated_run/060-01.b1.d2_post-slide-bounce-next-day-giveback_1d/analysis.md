---
line: 7.b inconclusive
backtest: 060-01.b1.d2_post-slide-bounce-next-day-giveback_1d
idea tested: 060-01.b1.d2_post-slide-bounce-next-day-giveback
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5438 USD
---
## Findings
- **F1:** The test's slope is on the predicted side but cannot be told from zero: -0.00028 with a day-clustered t of -0.59 on 2538 active bars over 758 days, using every fold and all 19 coins. No more daily data exists than the test already used. In the shown folds B and C, the slope on minus the forecast is again t -0.31 (590 active bars, 205 days).
- **F2:** The giveback is present as a level, not as a grade. In folds B and C, the drift-adjusted next-day return on active bars averages -0.98 % (t -4.37, n 590), or -0.82 % with day clustering (t -2.32, 205 days). Step 5 gives an unusual move of +0.62 % per case (t 2.27, 537 days), 2.8 times the 0.22 % cost of a trade. But that level is much the same across the forecast's quintiles: -0.41, -0.98, -0.53, -2.32 and -0.64 %, with no order.
- **F3:** The rise in swing units, the brief's own grade, does not scale the giveback at all. Its clustered slope has t +0.33, its rank slope t -0.02, and its Spearman rho is -0.016 (p 0.70). The largest-rise quintile (1.53 swing units) shows the smallest giveback, -0.28 % (t -0.56), against -1.82 % for the fourth quintile. That is exactly the brief's own falsification clause: the weakness does not grow with the size of the rise.
- **F4:** The depth of the prior 5-day fall leans the predicted way, but no part of the data shows it clearly. The deep tercile gives back -1.27 % (t -2.22, 87 days) and the shallow one -0.66 % (t -1.12, 85 days). Spearman rho is negative in 9 of 10 coins, and the year slopes are negative in 3 of 4 years. Yet the clustered depth slope has t -0.70 (rank t -0.87, scaled-return t -1.07), t -0.60 within prior-down cases only, and +0.60 in 2021.
- **F5:** The effect does not grow over a longer horizon. The two-day drift-adjusted mean is -0.69 % (t -2.19) and the three-day mean -0.69 % (t -1.97), against -0.98 % for one day. The scaled three-day return is -5.2 % of a usual move (day t -1.02), and the depth slope is t -0.38 at two days.

## Ideas
- No ideas: Rise days in falling agitated markets are followed by a next-day fall on average (F2). But that fall grows neither with the rise in swing units (F3) nor clearly with the depth of the prior slide in any coin, year or subset (F4), nor at a longer horizon (F5). So no amendment of this graded idea would give a clearer answer than this test, and the brief's own grading claim fails on the data.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
