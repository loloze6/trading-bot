---
line: 7.g patterns
backtest: 077-01_falling-calm-deep-close-drift_1d
idea tested: 077-01_falling-calm-deep-close-drift
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3630 USD
---
## Findings
- **F1:** In falling calm bars, the further a coin's close sits above its 20-day low, measured in 20-day daily-return standard deviations, the higher its 3-day return beyond the coin's mean. The slope t is 2.15 on 170 grid cases (offset 0), 3.65 on 165 (offset 1) and 2.83 on 173 (offset 2). The top third minus the bottom third is +1.8 %, +3.8 % and +1.9 %, against a trade cost of 0.33 %.
- **F2:** The same rise-off-the-low gradient holds at other horizons. At 5 days the slope t is 2.57, 2.87, 3.13, 1.20 and 2.05 over the five grid offsets (93 to 109 cases each), with top minus bottom of +1.9 % to +4.7 %. At 1 day it is t 2.86 on 525 cases.
- **F3:** By quintile of the distance off the low (3-day, offset 0, 34 cases each), the mean excess return climbs from -1.44 % (t -1.17) in the lowest quintile to +1.91 % (t 1.80) in the highest (5.1 to 17.8 swings off the low).
- **F4:** The tested depth below the 20-day high shows no continuation: its slope t is 0.66. The deepest quintile returns -0.79 % excess and the shallowest +1.10 % (t 1.37), so what the bars show is closes near the high rising, not deep closes falling.
- **F5:** The 5-day return in swing units, which correlates 0.51 with the distance off the low in this profile, gives a similar long-side gradient. At 3 days the slope t is 2.17, 2.20 and 1.09 over the three offsets; at 5 days it is 2.78, 3.21, 2.00, 1.01 and 1.90. Its lowest quintile returns -2.30 % excess over 3 days.
- **F6:** The pattern is weak inside single groups, so it may partly come from differences between coins and periods. Taking a day's cases together, its t is 1.97 over 114 days. By coin the slope t is 0.26 for BTC (64 cases), 0.57 for XMR (83) and 1.66 for DOGE (23); by year it is 0.29 in 2018, -0.41 in 2019 and 1.63 in 2021. Outside the profile it is about as strong (t 1.99 on 847 cases), so it is not specific to falling calm markets.
- **F7:** The other angles I looked at do not stand out given how many I checked. These were the one-day move, the close location in the day's range, the range width, volume against its 20-day mean, the swing level and the weekday. Their slope t values are 0.46, 1.08, -0.40, -1.62 and -0.29, with non-monotone quintiles.

## Ideas
- `077-01.g1_falling-calm-rebound-continuation` (from F1, F2, F3, F4, F6): In a falling, calm market, the further a coin's close has risen above its lowest low of the past 20 days, measured in its standard deviation of daily returns over the past 20 days, the larger its rise over the next three to five days.
- `077-01.g2_calm-decline-five-day-momentum` (from F5, F2, F6): In a falling, calm market, the larger a coin's 5-day return measured in its standard deviation of daily returns over the past 20 days, the larger its rise over the next five days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
