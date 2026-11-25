---
line: 7.a not observable
backtest: 032-01_volatile-decline-low-cascade_1d
idea tested: 032-01_volatile-decline-low-cascade
step 5: not observable
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4103 USD
---
## Findings
- **F1:** The test could not observe the idea because it had too few case days: over the whole backtest it found 42 cases on 27 distinct days, against the plan's minimum of 30 days. In the folds I can see (B, C), it found 23 cases, 21 of them with a 5-bar outcome, on only 11 distinct days, across 6 coins and 12 windows of about 122 bars each (mean 121.7, std 1.2).
- **F2:** The idea's situation is rare. The detector labelled only 75 of 8,400 bars "trending" (0.9 %), on 41 distinct days, at 10 to 16 bars per coin. These bars form 33 short runs (median 2 bars, max 5), and 60 of the 75 are the first bar of a run.
- **F3:** Only 23 of the 75 situation bars count as a case (a forecast drop of at least 2 points), because most breaks are shallow. The median absolute forecast in the situation is 1.20 (quartiles 0.52 and 2.60, 90th percentile 5.25), so most entries into the short side move the forecast by less than 2.
- **F4:** The volatile-range condition removes many breaks. Of 176 bars that both closed below the prior 30-day low and were down over 30 days, the detector kept 75. Four of 12 windows (w8, w10, w11, w14) have no situation bar at all, including w14, which had 39 such falling-break bars.
- **F5:** Situations and cases cluster on the same market days. 16 of the 41 situation days have two or more coins at once (one day has 6). The 23 cases fall on 11 days (one day holds 6 cases), and over the whole test 42 cases fall on 27 days (1.56 cases per day). Adding coins therefore adds case days less than in proportion.
- **F6:** The outcome varies widely from case to case. The short-signed 5-day return has a mean of -3.2 % and a standard deviation of 15.4 % over 21 cases. Summed per day, the mean is -7.5 % with a t of -0.61 on 9 days.
- **F7:** The available data could reach the minimum. At 42 cases over about 141 coin-windows (about 0.30 per coin-window), the other coins add about 158 coin-windows, which is roughly 47 more cases:

## Ideas
- `032-01.a1_volatile-decline-low-all-coins` (from F1, F2, F3, F5, F7): In a coin that has fallen over the past 30 days and whose daily high-low ranges over that month are wide compared with its own past year, a close below its lowest low of the prior 30 days is followed by a further fall over the next 5 days. The further that close sits below the prior 30-day low, the larger the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
