---
line: 7.g patterns
backtest: 024-02_fading-volume-downrun-rebound-size.d3_trend-strength-lifts-pullback-rebound.e1_thirty-day-trend-continuation-graded_4h
idea tested: 024-02_fading-volume-downrun-rebound-size.d3_trend-strength-lifts-pullback-rebound.e1_thirty-day-trend-continuation-graded
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4361 USD
---
## Findings
- **F1:** Volume predicts the 3-day move better than the tested 30-day return does. The log of a coin's last-day mean volume over its last-ten-day mean volume has a pooled slope on the 18-bar excess return of +0.0077 (t 3.81, 5148 non-overlapping cases), and the 3-day versus 20-day version has slope +0.0104 (t 4.00, 4716 cases). Excess return rises from -0.55 % in the lowest per-coin volume quintile to +0.79 % in the highest (t 2.64).
- **F2:** The volume effect holds broadly and is stronger over one day and after a rising day.
- **F3:** The coin's 7-day return, divided by its 30-day bar volatility, carries the tested idea's effect.
- **F4:** The 30-day return alone is weak and unstable.
- **F5:** The 4h bar that opens at 20:00 UTC rises more than the coin's average bar.
- **F6:** The book is mostly the coins' own large up-days.
- **F7:** A short run of bars in one direction does not predict the 3-day move. The signed count of consecutive same-direction bars has a rank-slope t of only 0.55, and the 1-day vol-scaled return a t of -1.58. The brief's run-and-exhaustion structure does not show in the next 3 days.

## Ideas
- `024-02_fading-volume-downrun-rebound-size.d3_trend-strength-lifts-pullback-rebound.e1_thirty-day-trend-continuation-graded.g1_volume-surge-predicts-rise` (from F1, F2): The higher a coin's volume over its last day relative to its average volume over the last ten days, the more the coin rises over the next day beyond its normal drift.
- `024-02_fading-volume-downrun-rebound-size.d3_trend-strength-lifts-pullback-rebound.e1_thirty-day-trend-continuation-graded.g2_rising-day-on-volume-continues` (from F1, F2): After a day on which the coin rose, the higher its volume over that day relative to its ten-day average volume, the more it keeps rising over the next three days beyond its normal drift.
- `024-02_fading-volume-downrun-rebound-size.d3_trend-strength-lifts-pullback-rebound.e1_thirty-day-trend-continuation-graded.g3_vol-scaled-weekly-trend-continuation` (from F3, F4): The larger a coin's 7-day return, measured in units of its own 30-day volatility, the more it rises over the next three days beyond its normal drift.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
