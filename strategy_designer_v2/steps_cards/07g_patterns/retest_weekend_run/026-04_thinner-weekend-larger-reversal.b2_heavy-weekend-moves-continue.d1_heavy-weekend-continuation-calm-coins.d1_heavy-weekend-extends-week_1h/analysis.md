---
line: 7.g patterns
backtest: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d1_heavy-weekend-extends-week_1h
idea tested: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d1_heavy-weekend-extends-week
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 3
cost: 0.6582 USD
---
## Findings
- **F1:** Across all six coins the evening hours carry a steady rise: the bar opening at 21:00 UTC averages +0.055 % (t 6.87, about 17,400 bars) and the one at 22:00 +0.044 % (t 5.76). The 2-hour 21:00–23:00 return is positive in every coin (+0.08 % to +0.13 %, t 2.0 to 4.7), in 20 of 24 windows, and in 6 of 8 years (2022 −0.016 %, t −0.50; 2025 +0.03 %, t 1.01). It holds on every weekday, from +0.059 % on Monday to +0.142 % on Sunday.
- **F2:** The evening rise is graded by how heavy the day's volume has been. Taking the mean volume from 01:00 to 21:00 against the prior week, the volatility-scaled 21:00–23:00 return grows from 0.008 (t 0.52) in the lightest-volume quintile to 0.131 (t 4.75) in the heaviest. Its slope on the log volume ratio is +0.055 (t 3.72, 13,518 day-cases) and is positive in 5 of 6 coins. The same test on 17:00–19:00 gives −0.023 (t −1.62).
- **F3:** Weekend moves made on thin volume are reversed over Monday and Tuesday. On Sunday-close cases with a below-median weekend-to-weekday volume ratio, the slope of the next 48-hour excess return on the weekend's 48-hour move is −0.18 (t −3.15, 945 cases), negative in all six coins (t −0.7 to −1.9). Across all Sundays, the weekend move divided by the volume ratio predicts the next 48 hours with slope −0.058 (t −2.85, 1,893 cases) and the next 24 hours with −0.045 (t −2.88). The effect weakens after 2021 (2018–21: −0.086, t −2.66; 2022–25: −0.024, t −0.97).
- **F4:** The tested continuation sits only in the heavy-volume, week-extending weekends: signed continuation of 0.33 usual moves (t 3.36, 202 cases), with a within-cell slope of +0.21 (t 2.6). It is not graded by the weekend move's size as the idea states: the largest-move quintile of all Sundays gives −0.05 (t −0.81) against +0.12 (t 2.33) in the second.
- **F5:** Sunday continuation depends on how calm the coin has been. The slope of the next 48 hours on the weekend move is +0.23 (t 2.82, 631 cases) in the calmest third of the past 7 days' hourly volatility, +0.14 (t 2.26) in the middle third, and −0.08 (t −1.77) in the most volatile third.
- **F6:** Heavy-volume continuation is not specific to weekends. 48-hour moves ending Tuesday to Thursday that extend the prior five days on above-average volume continue by 0.074 usual moves (t 2.81, 1,675 overlapping cases) against 0.33 on Sundays.

## Ideas
- `026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d1_heavy-weekend-extends-week.g1_heavy-day-evening-rise` (from F1, F2): A coin's price rises during the 21:00–23:00 UTC evening hours. The rise over those two hours is the larger, the heavier the coin's volume since 01:00 that day has been against its mean over the preceding week.
- `026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d1_heavy-weekend-extends-week.g2_thin-weekend-moves-reverse` (from F3, F4): A coin's Saturday–Sunday move made on thinner volume than its preceding five weekdays is reversed over the next 48 hours. The reversal is the larger, the larger the weekend move and the thinner the weekend volume against the weekdays.
- `026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d1_heavy-weekend-extends-week.g3_calm-coin-weekend-continuation` (from F5, F4): A coin's Saturday–Sunday move continues over the next 48 hours. The continuation is the larger, the larger the weekend move and the calmer the coin's hourly returns have been over the preceding seven days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
