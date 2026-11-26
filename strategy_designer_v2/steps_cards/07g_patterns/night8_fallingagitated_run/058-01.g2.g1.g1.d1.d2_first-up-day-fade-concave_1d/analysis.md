---
line: 7.g patterns
backtest: 058-01.g2.g1.g1.d1.d2_first-up-day-fade-concave_1d
idea tested: 058-01.g2.g1.g1.d1.d2_first-up-day-fade-concave
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3955 USD
---
## Findings
- **F1:** Inside the falling agitated profile, a coin's 3-day return measured in 30-day daily-return standard deviations (times √3) predicts the next 3 days, read on non-overlapping 3-day stretches. The top quintile is followed by an unusual move of −2.46 % (t −2.39, 69 cases). The bottom quintile is followed by +2.21 % (t 1.84, 72 cases). Outside the profile the same top quintile continues upward, +1.40 % (t 2.93, 377 cases). The give-back of a multi-day rise is specific to this profile. This is the brief's own situation, which the tested one-day idea did not use.
- **F2:** The tested grading holds in folds B and C. Among first up days after a down day in the profile, the next-day unusual move falls with the day's range in 30-day return standard deviations: −0.71 % (t −1.63), −1.18 % (t −2.37) and −2.31 % (t −3.98) by tercile, 106 cases each. The fade appears in every year (2018 −2.32 % t −3.90; 2019 −0.69 %; 2020 −1.37 %; 2021 −0.76 %) and in every coin (−1.16 % to −1.69 %).
- **F3:** Among those first up days, where the day closes inside its own range also grades the fall. Closes in the lowest third of the range (far below the day's high) are followed by −1.77 % (t −3.48). The middle third is followed by −1.50 % (t −3.20) and the top third by −0.93 % (t −1.68). An up day that gives back much of its intraday high fades most.
- **F4:** The first up day fades out of the profile as well, but by a quarter as much: −0.37 % (t −3.09, 1598 cases) against −1.40 % (t −4.75, 318 cases) inside it. One-day rises in the profile also fade: the top two z-quintiles of the day's return are followed by −0.85 % (t −2.23) and −0.83 % (t −1.91), against −0.16 % and −0.12 % outside it.
- **F5:** In the profile, down days rebound more after longer down streaks: +0.89 % after 1 down day (t 2.78), +1.20 % after 2 (t 3.09), +3.06 % after 3 (t 2.96) and +3.90 % after 4 or more (t 2.99). The widest-range down days rebound +2.59 % (t 5.19), and the lowest-close days +2.12 % (t 5.06). The profile map already holds twelve long falling-agitated rebound strategies, so these are already held and not proposed.
- **F6:** The book's summed daily returns are concentrated in two windows: w14 gives +85.3 % and w16 +29.8 % of about +142 % in total, and five windows are flat or negative. The profile covers only 15.8 % of coin-bars. This concentration is consistent with the Calmar failure (0.56) despite a total move per case 4.2 times the cost.

## Ideas
- `058-01.g2.g1.g1.d1.d2.g1_falling-agitated-3-day-rally-fade` (from F1, F4): In a falling, agitated market, a coin's rise over the past 3 days is partly given back over the next 3 days. The larger that 3-day return against the standard deviation of its daily returns over the past 30 days, the larger the fall.
- `058-01.g2.g1.g1.d1.d2.g2_first-up-day-weak-close-fade` (from F3, F2): In a falling, agitated market, the first up day after a down day is followed by a fall over the next day. The lower that day closes within its own low-to-high range, the larger the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
