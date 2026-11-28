---
line: 7.c no effect
backtest: 086-02.c1_forceful-break-day-continues_1d
idea tested: 086-02.c1_forceful-break-day-continues
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 2
cost: 3.7997 USD
---
## Findings
- **F1:** In rising agitated markets the first up day after 2 or more down days was not followed by a rise. Over 5 days the 176 turning days averaged -0.90 % against drift (t -0.63), and every horizon from 1 to 10 days was negative (-0.71 % at 1 day, t -1.33). This agrees with step 5's -0.12 % (t -0.13, 338 cases, 228 days).
- **F2:** The force of the up day, which the test sized by, carried nothing. Over 5 days the weak, mid and strong thirds averaged +0.01 %, +1.22 % and +1.88 % (t 0.00 to 0.50, 47 cases each), and the rank correlation of force with the 5-day move was -0.11.
- **F3:** Depth mattered, against the brief's grading. Depth is the down run's summed return in 30-day standard deviations. Turns after the deepest third fell 5.12 % over 5 days against drift (t -2.51, 47 cases), while the middle and shallowest thirds rose 4.58 % (t 1.25) and 3.40 % (t 1.55). The slope of the 5-day move on depth points toward "shallower is better": beta +0.029 per standard deviation, t 2.36 clustered by day, 131 cases on 90 days, Spearman +0.21.
- **F4:** The depth pattern holds in both halves of the data.
- **F5:** The effect needs a run of at least 2 down days. With single down days included (298 cases), the depth slope fell to t 1.27 (183 days), the Spearman to -0.03, and the shallow third to +0.66 % over 5 days.
- **F6:** Run length in days did not grade the rise either. Turns after 2, 3, 4 and 5 or more down days averaged +0.25 %, -1.43 %, -2.16 % and -7.47 % over 5 days (93, 57, 15 and 11 cases), and the rank correlation with the 5-day move was -0.15. Longer runs tilted the move down, not up, as F3 found for depth.

## Ideas
- `086-02.c1.c1_shallow-pullback-break-continues` (from F3, F4, F5, F6): In a rising, agitated market, on the first up day after a run of two or more consecutive down days, the coin rises over the next 5 days, and the shallower that down run was, measured as its summed return against the standard deviation of the coin's daily returns over the past 30 days, the larger that rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
