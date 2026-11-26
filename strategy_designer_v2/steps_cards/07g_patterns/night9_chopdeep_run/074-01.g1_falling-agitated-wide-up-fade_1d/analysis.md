---
line: 7.g patterns
backtest: 074-01.g1_falling-agitated-wide-up-fade_1d
idea tested: 074-01.g1_falling-agitated-wide-up-fade
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4745 USD
---
## Findings
- **F1:** Outside the tested profile (not falling agitated), an up day with a range above its 20-day mean range that comes after a 20-day return below -10 % is followed by a next-day unusual move of -1.71 % (t -3.61, 216 cases), against -0.07 % (t -0.19, 139 cases) after a 20-day return of -10 to 0 %, +0.30 % (t 0.97, 211 cases) after 0 to +10 %, and +0.15 % (t 0.43, 578 cases) after more than +10 %.
- **F2:** The fade outside the profile is graded by width. Among up days after a 20-day fall of more than 10 %, the range terciles give a next-day unusual move of -0.37 % (lo, t -0.75), -0.62 % (mid, t -1.36) and -1.68 % (hi, mean multiple 1.49, t -3.62, 118 days). The next-day return correlates -0.11 with the range multiple.
- **F3:** Over all up days after any 20-day fall, the depth of the fall times the range multiple orders the next day monotonically by quartile: -0.30 % (t -1.26), -0.56 % (t -1.82), -0.66 % (t -1.68) and -1.23 % (t -2.14, 382 cases, 150 days).
- **F4:** The fade lives outside falling agitated too. Wide up days with a 20-day fall whose 60-day return is also below -10 % (falling but not falling agitated, so calm) are followed by -1.69 % (t -2.62, 80 cases, 45 days). Those with 20-day swing at or below their 60-day swing give -1.36 % (t -2.22, 69 cases). This contradicts the tested consequence that a calm downtrend gives no edge.
- **F5:** Inside the falling agitated profile, up days by range-multiple quartile give next-day unusual moves of -0.24 % (q1), -0.53 % (q2), -1.62 % (q3, t -2.19) and -1.35 % (q4, t -1.30). This is the tested effect, on only 113 to 169 cases per quartile.
- **F6:** The fade is spent in one day. Outside the profile, wide up days in the deepest 20-day-fall quintile have a second-day unusual move of +0.03 % (t 0.06), against -1.78 % on the first day (t -3.42, 186 cases).
- **F7:** The same fade shows with other lookbacks for the prior fall. Wide up days in the lowest quartile of the 10-day return (mean -17 %) are followed by -1.64 % (t -3.21, 138 days), and in the lowest quartile of the 40-day return (mean -32 %) by -1.62 % (t -2.77, 125 days). The other quartiles stay within ±0.6 % with |t| below 1.4.
- **F8:** The outside-profile fade points the same way on 6 of 6 coins and 4 of 4 years:
- **F9:** Wide down days inside falling agitated (top range quartile) are followed by +3.26 % (t 2.93, 129 cases). This is the falling-agitated rebound family the map already holds 16 times, so it is not a discovery.
- **F10:** No weekday pattern stands out (largest |t| 1.52 over 7 weekdays). The book is in a position on only 4 % of coin-days, with most windows' mean daily return near 0, which is why its Calmar fails while the per-case move is 6.3 times the cost.

## Ideas
- `074-01.g1.g1_falling-wide-up-day-fade` (from F4, F5, F2, F6, F8): In a falling market, an up day whose high-to-low range is wide compared with the coin's average daily range over the past 20 days is followed by a fall over the next day; the wider that range is against the 20-day average, the larger the next day's fall.
- `074-01.g1.g2_recent-fall-wide-bounce-fade` (from F1, F2, F3, F6, F7, F8): An up day whose high-to-low range is wide compared with the coin's average daily range over the past 20 days, coming after a fall in the coin's 20-day return, is followed by a fall over the next day; the deeper the 20-day fall and the wider the day's range, the larger the next day's fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
