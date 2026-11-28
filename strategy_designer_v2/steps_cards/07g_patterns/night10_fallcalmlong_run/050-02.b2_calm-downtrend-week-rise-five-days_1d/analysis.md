---
line: 7.g patterns
backtest: 050-02.b2_calm-downtrend-week-rise-five-days_1d
idea tested: 050-02.b2_calm-downtrend-week-rise-five-days
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6596 USD
---
## Findings
- **F1:** In the falling calm profile, the rise of a coin's close above its 20-day low, measured in units of its 30-day daily-return swing, ranks the excess return that follows. Over 5 days the top quintile (mean 6.5 swings off the low) beats holding by +4.80 % (t 2.13, 24 cases) and the bottom quintile (0.02 swings) trails it by -5.97 % (t -2.62). The rank correlation is 0.30 (t 3.32, 121 cases). Over 3 days it is +2.58 % (t 2.41) against -1.51 %, with correlation 0.22 (t 3.18, 216 cases).
- **F2:** The rise off the 20-day low holds on every non-overlapping grid offset. Its rank correlation with the excess return is 0.19 to 0.25 over 3 days (t 2.74 to 3.67) and 0.17 to 0.36 over 5 days (t 1.87 to 4.14). Its 10-day version gives 0.15 to 0.35.
- **F3:** When the rise off the 20-day low and the scaled 7-day return are regressed together, the rise off the low keeps a positive slope on all 8 offsets (0.0053 to 0.0126 per swing). The 7-day return's slope changes sign (-0.0009 to +0.0215). The rise off the low carries the information.
- **F4:** The tested idea's own long side is weak. Bars with a positive scaled 7-day return beat holding by only +0.6 % to +2.9 % over 5 days (t 0.37 to 1.93, 41 to 49 cases per offset). The scaled 7-day return's rank correlation (0.19 to 0.31) comes mostly from bars with a negative 7-day return, which trail holding by -1.7 % to -3.0 % (t -1.27 to -2.32).
- **F5:** Being in the falling calm profile is itself no edge for a long. All in-profile bars trail holding the coin by -0.83 % over 5 days (t -0.77, 146 cases) and by -2.67 % over 10 days (t -1.24, 70 cases). The 5-day excess is negative in 2018 and 2019 (-3.8 %, -2.9 %) and positive in 2020 and 2021 (+3.1 %, +3.4 %).
- **F6:** Split by coin over 3 days, the top tercile of the rise off the 20-day low beats holding on all four coins (+0.7 % to +1.8 %). The bottom two terciles trail it on ETH, XMR and ZEC (down to -4.9 %, t -2.32 on ZEC and -2.59 on ETH). By year the top tercile is positive in 2018 and 2021 (+2.7 %, +3.3 % with t 2.60) and near zero in 2019 and 2020.
- **F7:** Nothing else stood out. The day's close location in its range, the range scaled by the swing, volume against its 20-day mean, the 30-day swing level and the scaled 1-day and 20-day returns all give rank correlations with t under 1.8 over 3 and 5 days. Weekday effects on next-day returns and on the book's held bars stay at |t| ≤ 2.3 across 7 weekdays, which is not distinguishable from chance given the many angles looked at.

## Ideas
- `050-02.b2.g1_calm-downtrend-climb-off-low` (from F1, F2, F3, F4, F6): In a falling, calm market, a coin whose close has climbed far above its lowest close of the last 20 days rises over the next 5 days. The further it has climbed, in units of its 30-day daily-return swing, the more it rises.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
