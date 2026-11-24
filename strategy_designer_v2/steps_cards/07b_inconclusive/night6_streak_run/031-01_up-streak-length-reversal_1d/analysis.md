---
line: 7.b inconclusive
backtest: 031-01_up-streak-length-reversal_1d
idea tested: 031-01_up-streak-length-reversal
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3780 USD
---
## Findings
- **F1:** The test's cases hardly ever caught a long up streak, so it measured the first up close rather than the idea's long streaks. Of 3,132 cases at 5 days, 2,691 came on the first up close, 329 on the second and only 13 on the third, and none came on a fourth or later up close. The mean streak was 0.99 in the bottom third of |forecast| and 1.28 in the top third.
- **F2:** The main measure is on the predicted side but too small for this data to show. It is +0.32 % unusual move per short case over 5 days, with t 1.08 over 1,206 days. That is a strength of 0.035 of the coin's usual 10.60 % move, and the short side's normal drift of -0.66 % turns the total move to -0.34 %.
- **F3:** The grading the idea needs is absent. The top third of |forecast| gave +0.30 % short over 5 days (t 0.63) and the bottom third +0.47 % (t 0.95), so the top minus the bottom is -0.17 %. On the 10-day horizon the top third gave +0.32 % and the bottom +0.41 %.
- **F4:** Where the test's cases do show a reversal, it lasts one day, not five. The short unusual move per case was +0.40 % over 1 day (t 3.03, 3,234 cases), against +0.12 % over 3 days (t 0.53), +0.32 % over 5 days (t 1.08) and +0.18 % over 20 days (t 0.25).
- **F5:** On the 1-day grid, the next-day fall belongs to the first up close only. The unusual next-day return was -0.31 % after one up close (t -2.63, 4,545 cases), -0.01 % after two (t -0.09), +0.14 % after three (t 0.69) and +0.05 % after four or more (t 0.27).
- **F6:** Longer up streaks are followed by continuation, rising with the streak's length.
- **F7:** The effect is mixed across coins and years, which leaves a weak mean.
- **F8:** The book lost money. Its Sharpe was -0.67 and its yearly return -42.1 %, while it held a position on 96 % of the coins' days. A trade cost 0.19 %, against a total move per case of -0.34 %, so the short side paid the coins' upward drift on top of costs.

## Ideas
- `031-01.b1_up-streak-reversal-more-coins` (from F2, F7): The more days in a row a coin has closed higher, measured against the lengths of its own up-close streaks over the past 365 days, the more it falls over the next 5 days.
- `031-01.b2_long-up-streaks-continue` (from F1, F5, F6): The more days in a row a coin has closed higher, measured against the lengths of its own up-close streaks over the past 365 days, the more it rises over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
