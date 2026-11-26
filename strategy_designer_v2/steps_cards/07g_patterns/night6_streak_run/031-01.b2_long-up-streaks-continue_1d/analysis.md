---
line: 7.g patterns
backtest: 031-01.b2_long-up-streaks-continue_1d
idea tested: 031-01.b2_long-up-streaks-continue
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3763 USD
---
## Findings
- **F1:** The longer a coin's current run of same-direction daily closes, the larger its next 3-day move in absolute terms, scaled by its past 20-day volatility. On the non-overlapping 3-day grid the slope of this scaled move on streak length is 0.045 per day of streak (t 3.40 with cases of one day taken together; 4586 cases on 860 days).
- **F2:** The volatility effect holds after up runs and after down runs alike. The slope is 0.035 per day after up runs (t 2.26; 2412 cases, 650 days) and 0.060 per day after down runs (t 2.34; 2170 cases, 614 days).
- **F3:** After runs of 4 or more same-direction closes, the scaled 3-day move averages 1.04, against 0.79 after shorter runs (Welch t 4.63; 455 vs 4131 cases). The gap appears in all 6 coins, with values from 0.95 to 1.19 after long runs against 0.78 to 0.82 otherwise.
- **F4:** The direction after a run does not stand out from chance once the number of angles looked at is counted.
- **F5:** The tested forecast does not sort the 3-day excess return. It is −0.26 % at forecast 5–10 and −0.47 % at forecast 10–15 (t −1.38), then +0.32 % at forecast 15–20 (t 0.99).
- **F6:** Past 7-, 14- and 30-day returns scaled by volatility show only weak continuation (slopes t 1.44, 1.54 and 1.53). The 30-day slope changes sign by year, at −0.021 (t −2.04) in 2018 against +0.007 (t 1.45) in 2025.
- **F7:** The book is mostly the coin's own move. Its daily return correlates 0.78 with the coin's daily return. On its worst 2 % of days it loses 8.6 % while the coin loses 10.5 %, and on its best 2 % it gains 10.7 % while the coin gains 12.1 %. This is consistent with being in a position on 91 % of coin-days.
- **F8:** None of these other cuts shows a clear 3-day excess return:

## Ideas
- `031-01.b2.g1_long-streaks-precede-volatility` (from F1, F2, F3): The more days in a row a coin has closed in the same direction, up or down, the larger its absolute price move over the next 3 days, relative to its own daily volatility over the past 20 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
