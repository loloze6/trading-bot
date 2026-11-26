---
line: 7.b inconclusive
backtest: 060-01_falling-calm-wide-high-close-fade_1d
idea tested: 060-01_falling-calm-wide-high-close-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3660 USD
---
## Findings
- **F1:** The tested effect sits on the predicted side but is weak and uneven. Over all folds the next-day unusual move is +0.30 % (t 1.00, 321 cases, 186 days). In the visible folds B and C it is +1.25 % (t 2.52, 105 cases, strength 0.196), which means folds A and D carry almost none of it.
- **F2:** Even inside folds B and C the effect is concentrated in time. It is strong in w9 (+2.09 %, t 4.37, 13 cases), w12 (+2.32 %, t 1.79) and w14 (+3.19 %, t 1.90). It is flat or reversed in w15 (0.00 %), w17 (-0.27 %) and w18 (-0.83 %, t -0.91, 16 cases). By year it is +1.96 % in 2018 and +1.48 % in 2019, against +0.04 % in 2020 and +0.58 % in 2021.
- **F3:** The grading by close location works and the grading by width does not. Across the 89 cases with both measures, the slope of the next-day unusual move on close location is +0.123 (t 2.29). The slope on width is -0.0033 (t -0.87), and the slope on the plan's combined |forecast| is -0.0004 (t -0.18). The supporting check therefore rests on the wrong grader.
- **F4:** Sorted by close location, the next-day fade grows step by step. It is +0.62 % (t 0.92, 46 cases) for closes at 0.75–0.85 of the range, +1.62 % (t 2.49, 43 cases) at 0.85–0.95, and +2.06 % (t 1.74, 16 cases) at 0.95–1.0. By width tercile it is flat or falling: +1.29 %, +1.29 %, +0.90 %.
- **F5:** The falling, calm profile matters. Wide, high-closing days outside the profile show only +0.41 % next-day unusual move (t 0.83, 396 cases), and nothing over 2 to 3 days (-0.35 %, -0.53 %). The profile's cases show +1.25 % (F1).
- **F6:** The test already used every coin and every fold available, so no more data exists for this idea. Its total move per case (+0.16 %) is 0.7 times the 0.22 % cost of a trade, so the effect only becomes usable if a sharper grader enlarges the move per case.

## Ideas
- `060-01.b1_falling-calm-high-close-fade` (from F1, F3, F4, F5, F6): In a falling, calm market, a day whose high-to-low range is wide against the coin's 30-day swing of daily returns and that closes near its high is followed by a fall over the next day, larger the closer the close sits to the day's high.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
