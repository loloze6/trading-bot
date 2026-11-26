---
line: 7.g patterns
backtest: 060-01.g1_wide-day-high-close-fade_1d
idea tested: 060-01.g1_wide-day-high-close-fade
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4097 USD
---
## Findings
- **F1:** In the falling agitated profile, high-close days (close in the top quarter of the range) fall more the wider the day's range is against its last 20 days, step by step. The mean unusual next-day move is +0.40 % below 0.7 times the usual range (110 cases), -0.68 % at 0.7–1 (90), -1.57 % at 1–1.5 (45, t -1.86), -2.41 % at 1.5–2.2 (28, t -2.90) and -2.22 % above 2.2 (8). The fade is graded across the whole range of widths, not only above the plan's 1.5 cutoff.
- **F2:** The book failed on activity, not on edge. It was in a position on 1 % of coin-days and made 0.005 trades a day against the 0.01 required. Its total move per case is 9.7 times the 0.19 % cost of a trade. Widening the situation, not the size per trade, is what the book lacks.
- **F3:** In the profile, a close in the upper half of the range fades about as much as one in the top quarter: -0.74 % at 0.5–0.75 (306 cases, t -2.24) and -0.63 % at 0.75–1 (319, t -2.08). Up days that close in the upper half fall -0.95 % the next day (449 cases, 198 days, day-clustered t -2.16). How near the high the close sits adds no grading beyond the upper half.
- **F4:** The effect lives in the profile. Outside it, high closes in falling-but-calm markets move -0.34 % the next day (t -0.85), and in rising markets they move +0.48 % (t 1.37). Inside the profile they move -0.63 %. This fits the brief's claim that only a downtrend with high agitation fades strong closes.
- **F5:** The fade on up days in the profile held in 2018, 2019 and 2020 (-1.74 %, -1.37 % and -0.81 %, with t -1.87, -2.38 and -1.03). It reversed in 2021 (+0.62 %, t 0.51), and the tested cases rose in 2021 as well (4 cases, +3.36 %). It points the same way on 5 of 6 coins, XRP excepted.
- **F6:** In the same profile, low closes rebound +1.51 % the next day (322 cases, t 4.17), and the two lowest quintiles of scaled one-day return rebound +1.92 % and +1.37 % (t 4.74 and 3.77). This is the falling agitated long rebound the profile map already holds 12 times, so it is not a discovery.

## Ideas
- `060-01.g1.g1_graded-width-high-close-fade` (from F1, F2, F3, F4, F5): In a falling, agitated market, a coin that closes in the upper half of its day's high-low range falls over the next day, and the wider that day's range is against its ranges of the last 20 days, the larger the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
