---
line: 7.g patterns
backtest: 016-06_down-even-volume-continuation.g2_smooth-climb-continuation_1h
idea tested: 016-06_down-even-volume-continuation.g2_smooth-climb-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3723 USD
---
## Findings
- **F1:** Among 3-day climbs, the raw 72-hour efficiency ratio (the share of summed absolute hourly moves that points up) predicts the next 3 days, while the recorded forecast does not. Pooled over 2865 non-overlapping up cases, the per-coin z-scored slope has t 3.43 for the raw ratio and t 1.41 for the recorded forecast, which is the same ratio standardised against its own past 72 values (correlation 0.72 with the raw ratio). The standardisation is where the idea's signal was lost.
- **F2:** The raw-ratio effect is graded and not a proxy for the size of the climb. The 72-hour forward excess return rises steadily across efficiency quintiles: -0.0044, -0.0025, +0.0013, +0.0033, +0.0113 (top quintile t 2.78, about 574 cases each). In a joint regression with the 3-day return, the ratio keeps t 2.48 while the 3-day return drops to t -0.31.
- **F3:** The F1 slope is positive in all 6 coins (t from 0.40 for XMR to 2.46 for ZEC) and in both halves of the windows (w1–w12 t 1.46, w13–w24 t 3.20).
- **F4:** After a 3-day fall, the coin reverts over the next 3 days, and more so the deeper the last day's fall. Over 2674 non-overlapping down cases, the slope of forward excess return on the 24-hour return has t -3.80, and on the 72-hour return t -2.98. The 24-hour slope is negative in all 6 coins (ETH t -2.32, LTC -2.04, XRP -2.96) and in both halves (t -2.04 and -3.12).
- **F5:** Also after 3-day falls, higher hourly volatility over the past 3 days is followed by higher 3-day forward excess return (t 2.75, n 2674). Among climbs the same effect is absent (t 0.60).
- **F6:** Hourly returns in the 21:00–23:00 UTC hours average 0.000475 more than all other hours (Welch t 8.16). The effect holds in every coin (t from 3.04 to 4.56) and in 7 of 8 years, with 2022 the exception (-0.00022).
- **F7:** Saturday hourly returns are positive overall (mean 0.000207, t 5.57) and in every coin (t from 1.31 to 2.80).
- **F8:** The book lost money: Sharpe -0.50 and mean daily return -0.00034. It earned less than holding the coins in 17 of 24 windows, consistent with the timing signal being diluted (F1).

## Ideas
- `016-06_down-even-volume-continuation.g2_smooth-climb-continuation.g1_absolute-smoothness-climb-continuation` (from F1, F2, F3): When a coin has risen over the past 3 days, the larger the absolute share of its 3-day summed absolute hourly moves that pointed up, the more it rises over the following 3 days. This share is taken on its own fixed scale, not relative to its recent values.
- `016-06_down-even-volume-continuation.g2_smooth-climb-continuation.g2_deep-drop-three-day-rebound` (from F4): When a coin has fallen over the past 3 days, the larger its fall over the past day, the more it rises over the following 3 days.
- `016-06_down-even-volume-continuation.g2_smooth-climb-continuation.g3_violent-decline-rebound` (from F5): When a coin has fallen over the past 3 days, the higher its hourly volatility over those 3 days, the more it rises over the following 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
