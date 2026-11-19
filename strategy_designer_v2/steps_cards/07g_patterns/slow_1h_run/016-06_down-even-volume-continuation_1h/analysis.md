---
line: 7.g patterns
backtest: 016-06_down-even-volume-continuation_1h
idea tested: 016-06_down-even-volume-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3866 USD
---
## Findings
- **F1:** Among falling coins, the larger the fall over the last 24 hours, the higher the next 72 hours' return above the coin's average. The pooled slope of excess return on the 24-hour return is -0.149 (t -4.34, 2669 non-overlapping cases). Cases in the steepest-fall quintile gained +1.26% (t 3.15, 536 cases), against -0.22% to -0.75% in the other four quintiles.
- **F2:** The F1 rebound after a sharp 24-hour drop shows in most coins and years. The slope is negative in all 6 coins, with t ≤ -2 in ETH (-2.32), LTC (-2.06) and XRP (-2.96). It is negative in 6 of 8 years, strongest in 2020 (t -3.18), 2021 (-3.33) and 2025 (-4.84). The exception is 2022, where the slope is positive (t +1.85).
- **F3:** Among falling coins, the size of the 3-day fall also works against the tested short. The slope of excess return on the 72-hour return is -0.101 (t -3.53, 2669 cases). Volume evenness adds nothing (concentration slope t -0.04), and neither does path smoothness (efficiency slope t -1.22).
- **F4:** Among rising coins, the more efficient the 3-day climb, the more it continues over the next 72 hours. Efficiency here is the net hourly move over the sum of absolute hourly moves. The slope is +0.056 (t 3.30, 2865 cases), and the volatility-scaled 3-day return gives t 3.36. The efficiency slope is positive in all 6 coins and all 8 years.
- **F5:** The book mostly lost because it shorted falls that then rebounded. Its daily return correlates -0.73 with holding the coins, and its Sharpe is negative in 19 of 24 windows.
- **F6:** The hours starting 20:00 and 21:00 UTC carry a positive 1-hour return, at t 3.0 to 4.4 in every coin. The Welch t against all other hours is 8.0. The effect is positive in 7 of 8 years and negative only in 2022. It is a calendar effect with no graded strength, so no idea is drawn from it.

## Ideas
- `016-06_down-even-volume-continuation.g1_fresh-drop-rebound` (from F1, F2, F3, F5): When a coin has fallen over the past 3 days, the larger its fall over the last 1 day, the more it rises over the next 3 days.
- `016-06_down-even-volume-continuation.g2_smooth-climb-continuation` (from F4): When a coin has risen over the past 3 days, the larger the share of its summed absolute hourly moves that points in the direction of the rise, the more it keeps rising over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
