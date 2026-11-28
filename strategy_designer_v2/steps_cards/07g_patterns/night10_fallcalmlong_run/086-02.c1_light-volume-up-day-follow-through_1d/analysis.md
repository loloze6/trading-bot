---
line: 7.g patterns
backtest: 086-02.c1_light-volume-up-day-follow-through_1d
idea tested: 086-02.c1_light-volume-up-day-follow-through
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3530 USD
---
## Findings
- **F1:** In the explore half, the falling calm profile (regimes mean_reversion and unknown) holds 146 non-overlapping 5-day cases on the 4 coins present. Their mean unusual 5-day move is -0.83 % (t -1.00). So, before any condition, the coin does no better than its normal drift there (BCH +1.67 %, ETH -1.79 %, XMR -0.66 %, ZEC -1.05 %).
- **F2:** The tested idea's light-volume up days ended +2.27 % on the grid starting at position 0 (29 cases, t 1.38). Across the five grid offsets they ranged from +2.27 % to -0.36 %. Heavy-volume up days were negative on 4 of 5 offsets (-3.23 %, +2.25 %, -4.34 %, -2.51 %, -3.73 %). The brief's claimed direction, heavy-volume up days carrying on, shows nowhere.
- **F3:** Heavy-volume down days in the profile were followed by +2.69 % on offset 0 (21 cases, t 1.63). The same group gave -0.03 %, +0.23 %, -4.48 % and -5.91 % on the other four offsets. A heavy-volume fall rebound is not a stable pattern.
- **F4:** A graded score that is high after a heavy down day or a light up day (minus the day's move scaled by its 20-day swing, times the log volume ratio) rose across quintiles on offset 0, from -4.26 % to +3.29 % (top quintile t_day 2.12, correlation 0.12, 121 cases). On all 622 in-profile bars it was -0.04. The grading comes from one grid's sampling, not from the bars.
- **F5:** In the profile, the weakest prior 5-day returns were followed by a further unusual fall of -4.94 % (28 cases, t -2.50). This was a short-side continuation, outside this research's long-only box. The strongest 10-day returns gave only +2.61 % (t 1.32), unstable by window (w12 -4.46 %, w17 +6.27 %).
- **F6:** No other cut stood out: weekday, the day's return, the close's place in its range and the range against its 20-day mean all had |t| under 2 in every bucket. Window means ran from -10.5 % (w9) to +9.9 % (w13) on 5 to 46 cases each, so no cut holds across windows.
- **F7:** The book's trades averaged +2.8 % to +4.9 % net per coin (213 trades). The idea's size per case was only +0.18 % unusual (t 0.41) against a 0.31 % trade cost. What the book earned was the coins' drift, +1.06 % to +1.25 % per 5 days, not timing.

## Ideas
- No ideas: I looked at the forecast, volume on up and down days, prior 5- and 10-day returns, range, close position, weekday, coin and window. Every long-side pattern in falling calm markets (F2–F4) changes sign or vanishes when the 5-day grid is shifted or all bars are used, so none can be told from chance across this many angles.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
