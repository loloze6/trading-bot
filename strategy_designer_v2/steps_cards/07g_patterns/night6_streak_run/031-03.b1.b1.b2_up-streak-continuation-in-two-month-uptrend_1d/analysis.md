---
line: 7.g patterns
backtest: 031-03.b1.b1.b2_up-streak-continuation-in-two-month-uptrend_1d
idea tested: 031-03.b1.b1.b2_up-streak-continuation-in-two-month-uptrend
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6581 USD
---
## Findings
- **F1:** The book's gain comes from the two-trend condition itself, not from the streak grading: per in-position bar the position gained +0.387 % when the regime was on (t 3.44, 11,220 bars on 2,091 days, day-clustered) and -0.035 % when it was off (t -0.30, 6,824 bars on 1,988 days); on daily bars it gained +0.50 % on average in the both-up state (6,290 bars) and -0.07 % elsewhere (9,452 bars).
- **F2:** Inside the both-up regime, a longer up-close streak was followed by a lower, not higher, 20-day unusual return: the slope was -0.0216 per streak day (t -2.00, 291 cases on 48 days, day-clustered). Step 5's own slope points the same way (t -1.36). By streak length, streaks of 2 days were followed by -7.96 % (t -2.88, 44 cases) and streaks of 4 and 5+ days by -1.82 % and -5.03 %, against +6.48 % after no streak (t 2.71, 138 cases).
- **F3:** Across all bars, the 30-day return scaled by the coin's 60-day daily volatility had a positive slope on the next unusual return at every horizon: +0.0122 at 10 days (t 1.99, 2,272 cases on 229 days), +0.0063 at 5 days (t 1.85, 4,603 cases on 466 days) and +0.0165 at 20 days (t 1.15, 977 cases on 97 days). By 30-day-return quintile, the 20-day unusual move rose step by step from -3.94 % to +2.75 % (144 cases each).
- **F4:** By trend state, the 20-day unusual move was +3.21 % when both the 30-day and 60-day returns were positive (t 2.06, 291 cases), -1.99 % when both were negative (t -1.36, 259 cases) and -3.48 % when they disagreed (t -1.87, 168 cases); inside both-up, the size of the 60-day return graded nothing (quartiles +1.0 %, +4.7 %, +3.2 %, +3.9 %, all t under 1.4).
- **F5:** The book's profit sits in its long holds: trades held 60–120 days returned a mean of +67.3 % net (median +27.0 %, 285 trades); trades of 20–30 days returned a mean of -11.3 % (median -14.2 %, 160 trades); overall the median trade was -3.4 % against a mean of +14.2 % (1,208 trades). This fits a trend held for a long time, not a short streak move.
- **F6:** The other angles did not stand out once one day's cases were taken together. No weekday had a day-clustered t above 1.80 (Saturday +0.26 %, Thursday -0.33 % with t -1.57). After a single large daily move, the 5-day return was +2.73 % following a move of 1.5–2.5 standard deviations (t 1.96, 280 cases) and -3.59 % following one below -2.5 (t -1.77). The 20-day slope on the 60-day trend changed sign from year to year (2022 -0.147 with t -3.84, 2023 +0.035 with t 1.80). The volatility-quartile splits rested on 11–15 distinct days.

## Ideas
- `031-03.b1.b1.b2.g1_vol-scaled-monthly-trend-continuation` (from F3, F4, F1): Over the next 10 days, the more a coin has risen over the past 30 days, measured against its own day-to-day volatility over the past 60 days, the more it keeps rising.
- `031-03.b1.b1.b2.g2_uptrend-streak-giveback` (from F2, F1, F5): While a coin is up over both the past 30 days and the past 60 days, the longer its current run of higher daily closes, compared with its own up-close runs over the past 365 days, the lower its return over the next 20 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
