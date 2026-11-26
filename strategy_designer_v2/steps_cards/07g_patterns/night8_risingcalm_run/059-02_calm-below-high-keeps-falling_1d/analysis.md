---
line: 7.g patterns
backtest: 059-02_calm-below-high-keeps-falling_1d
idea tested: 059-02_calm-below-high-keeps-falling
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4117 USD
---
## Findings
- **F1:** In calm markets (folds B, C, non-overlapping 5-day grid), the tested depth below the 14-day high is strongly graded. The deepest fifth (mean depth −4.94 swings) is followed by a 5-day excess return of −2.95 % (t −3.67, 155 cases) and the next fifth by −2.46 % (t −3.36). The fifth at the high is followed by +2.98 % (t 3.16). Across all calm grid bars the slope t of the excess move on depth is 6.06, and on the forecast 5.70 (forecast–depth correlation 0.86).
- **F2:** The same graded effect is absent in agitated markets. Depth fifths there give −1.52 % to +1.68 % with no order and no |t| above 1.74, and the depth slope in falling agitated is the other way (t −1.93, 150 cases). The effect lives in calm markets only.
- **F3:** The brief's literal situation, the swing-scaled 14-day return, sorts calm cases the same way. The lowest fifth is followed by −3.03 % over 5 days (t −3.67) and the second by −2.49 % (t −3.49), against +2.81 % for the highest fifth (t 2.93).
- **F4:** The book still lost because it was short in every calm state, including rising ones. On its in-position days it gained +0.299 % a day in falling markets (1,101 coin-days) and lost −0.462 % a day in rising ones (884) and −0.063 % in choppy ones (2,502).
- **F5:** In falling calm markets the depth terciles are cleanly ordered. The deepest third (−5.57 swings) is followed by −3.45 % over 5 days (t −2.49) and the middle third by −2.72 % (t −2.49), against +2.06 % (t 2.12) for the third near its high; the slope t is 3.58 over 219 cases. By year the slope is unstable: t 3.45 in 2018, −1.33 in 2019 and 0.98 in 2021.
- **F6:** In calm markets a single day's swing-scaled return carries on over the next 5 days. The largest-up fifth (+1.40 swings) is followed by +3.11 % (t 3.25) and the two lowest fifths by −1.55 % (t −2.24) and −2.30 % (t −2.88). In agitated markets this is absent: every fifth has |t| ≤ 0.82.
- **F7:** The calm one-day continuation keeps its sign every year: slope t 0.68 in 2018, 3.99 in 2019, 1.57 in 2020 and 2.52 in 2021. It is strongest in rising calm (t 3.54, 178 cases) and choppy calm (t 2.67, 101 cases).
- **F8:** The calm depth slope keeps its sign on every coin, with t from 1.99 (BTC) to 2.98 (XMR), and in every year, with t from 1.62 to 2.43. Even so, step 5 found the slope reversed on the check folds A, D (−0.00036). The plain calm-wide version of the tested idea is fragile out of sample, and the 5-day move of 2 to 3 % in the deep cases is about 15 times the 0.19 % cost of a trade.

## Ideas
- `059-02.g1_falling-calm-decline-continues` (from F3, F4, F5, F2): In a falling, calm market, the lower a coin's 14-day return sits measured in units of its own 30-day daily swing, the larger its fall over the next 5 days.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `059-02.g2_calm-day-move-continues` (from F6, F7, F2): In a calm market, the larger a coin's one-day return measured in units of its own 30-day daily swing, the further it moves the same way over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
