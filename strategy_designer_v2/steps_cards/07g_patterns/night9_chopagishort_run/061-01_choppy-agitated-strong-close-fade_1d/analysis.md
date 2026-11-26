---
line: 7.g patterns
backtest: 061-01_choppy-agitated-strong-close-fade_1d
idea tested: 061-01_choppy-agitated-strong-close-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3951 USD
---
## Findings
- **F1:** Across all profiles, a daily close in the top fifth of the day's high-low range is followed by a fall beyond the coin's drift: −0.56 % over the next day (t −3.14, 886 non-overlapping cases) and −0.54 % over the next two days outside the choppy-agitated profile (t −2.28, 851 cases). The fall shows in every year of folds B and C: 2018 −0.83 %, 2019 −1.06 % (t −2.86), 2020 −0.15 %, 2021 −0.44 %. It shows in 5 of 6 coins and in 9 of 12 windows.
- **F2:** The tested situation itself is too rare in folds B and C to read. Bars in the choppy-agitated profile are 4.9 % of the 2-day grid, and closes in the top fifth there number 35, with a 2-day unusual move of −1.24 % (t −0.71). The book's own cases gave +0.65 % short with t 1.49 over 194 days, so the theme's effect is about the right size but cannot be told from 0.
- **F3:** The fade after a high close is not graded at the very top. The 2-day unusual move is −0.84 % for closes at 0.8–0.9 of the range (t −2.57, 463), −1.04 % at 0.9–0.95 (t −1.99, 193) and +0.36 % at 0.95–1.0 (t 0.75, 230). The rank correlation of close location with the 2-day unusual move over all bars is only −0.06.
- **F4:** A coin's 5-day return predicts its next 2 days in the same direction, step by step across quintiles. The 2-day unusual move rises from −0.80 % in the bottom quintile (t −2.47) through −0.46 % (t −2.00), +0.14 %, +0.19 % to +0.59 % in the top quintile (t 1.91), 788 cases each. The bottom quintile is negative in all four years (−1.39 %, −0.65 %, −0.93 %, −0.11 %).
- **F5:** That continuation of a 5-day fall is strongest in a choppy market (60-day return between −10 % and +10 %). There the bottom 5-day quintile is followed by −3.73 % over 2 days (t −2.51, 49 cases) and the second by −1.59 % (t −2.12, 64 cases), against −0.03 % in the middle and +0.41 % / +0.46 % in the upper quintiles. In falling markets the same two quintiles give −0.92 % (t −1.77) and −1.15 % (t −2.75), and in rising markets none is below −0.09 %.
- **F6:** A single sharp day does the opposite of a 5-day run. The bottom quintile of 1-day returns (falls of more than 3.4 %) is followed outside the profile by +0.79 % over 2 days (t 2.48, 769). Wide days closing in the bottom fifth of their range are followed by +1.48 % (t 3.12, 188). Both are the one-day-fall rebounds the profile map already holds (044-01, 045-01, 039-02), so they are not new.
- **F7:** Weekday effects stand out, but they are conditions alone, not graded situations, and among about fifteen angles they are not strong enough to build on. Bars on Sunday are followed by −0.99 % over 2 days (t −2.81, 597), negative in 3 of 4 years, and Thursday bars by +0.70 % (t 3.02, 590), positive in 2 of 4 years.

## Ideas
- `061-01.g1_choppy-five-day-fall-continues` (from F4, F5): A coin that has fallen over its last five days keeps falling over the next two days in a choppy market (60-day return near flat), and the larger its 5-day fall, the larger the further fall.
- `061-01.g2_high-close-next-day-fade` (from F1, F3): When a coin's daily close sits in the upper part of that day's high-low range, its price falls over the next day, and the higher the close sits in the range, the larger the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
