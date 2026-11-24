---
line: 7.b inconclusive
backtest: 031-03.b1.b1.b2_up-streak-continuation-in-two-month-uptrend_1d
idea tested: 031-03.b1.b1.b2_up-streak-continuation-in-two-month-uptrend
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4505 USD
---
## Findings
- **F1:** The tested result points against the idea, not toward it: across all trending grid bars the 20-day slope is -0.0036 with t -1.36 (545 bars), and among bars with a positive forecast only it is -0.0019 with t -0.45 (305 bars), so this is not a near-miss that more data would turn into a confirmation.
- **F2:** Over 10 days, among up-close days inside the two-month uptrend, the effect shows on the idea's side: the slope of the 10-day unusual move on the forecast is +0.0060 with t 2.63 (635 grid bars, day-clustered). It is positive in all four folds (A t 1.02, B 1.52, C 2.14, D 1.22). At 5 days it is weaker but still on the same side (+0.0019, t 1.79, 1266 bars).
- **F3:** At 20 days the most extreme streaks give part of the run back: the mean unusual 20-day move falls from +2.5 % (forecast 0–8, 19 bars) to +0.6 % (8–12, 91), -3.3 % (12–16, 34) and -1.1 % (16–20, 161). Five coins have a 20-day slope t of -2 or less (AAVE -2.35, ADA -2.00, LINK -2.94, TRX -2.03, UNI -2.27). The continuation fades past about 10 days and turns to giveback by 20.
- **F4:** Inside the uptrend, the bars with no up streak (forecast 0, mostly down-close days) are followed by the largest moves: +5.4 % unusual over 20 days (t 3.23, 240 bars). Their weight in the plan's slope pulls the slope down and drowns the streak effect. The length of a down run inside the uptrend is only weakly graded (20-day slope +0.026, t 1.19, 545 bars; 10 of 15 coins positive).
- **F5:** Outside the two-month uptrend, a longer up streak is followed by a lower 20-day move. With the raw up-close count capped at 5, the slope is -0.027 with t -2.71 (950 grid bars). Unusual moves fall from +1.1 % after no up close (673) to -5.2 % after 1 (139), -9.9 % after 2 (77) and -7.2 % after 4 or more (39). This is the brief's crowding reversal, showing where the trend filter is off.

## Ideas
- `031-03.b1.b1.b2.b1_uptrend-streak-continuation-ten-days` (from F2, F3, F4): Among days a coin closes higher, the more days in a row it has closed higher, measured against the lengths of its own up-close streaks over the past 365 days, the more it keeps rising over the next 10 days, only while its 30-day return is positive and its 60-day return is positive.
- `031-03.b1.b1.b2.b2_up-streak-reversal-outside-uptrend` (from F5, F1): The more days in a row a coin has closed higher, measured against the lengths of its own up-close streaks over the past 365 days, the more it falls over the next 20 days, only while its 30-day return or its 60-day return is negative.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
