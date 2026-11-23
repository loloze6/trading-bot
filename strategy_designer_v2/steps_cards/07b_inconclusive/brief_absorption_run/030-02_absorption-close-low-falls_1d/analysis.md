---
line: 7.b inconclusive
backtest: 030-02_absorption-close-low-falls_1d
idea tested: 030-02_absorption-close-low-falls
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3485 USD
---
## Findings
- **F1:** The test's result is on the opposite side from the idea. After the short bets the excess fall was -0.50 % per case over 5 days (t -0.66, 151 cases), which means the coin rose a little more than its drift. The slope on forecast size was also negative (-3.6e-05). My own recount of heavy flat days (volume at least 2 times its prior 20-day mean, body at most 1 %, one per 5-day cell) shows the same thing: an excess rise of +0.93 % over 5 days (t 1.11, n 120) and +1.80 % over 10 days (t 1.49, n 117).
- **F2:** On heavy flat days, where the close sits in the range does not grade the next move.
- **F3:** Heavier volume does not make the move larger.
- **F4:** The effect does not hold in one coin or period and fail elsewhere.
- **F5:** Ordinary-volume flat days show only a faint sign of the idea's direction, and none of the grading.
- **F6:** The size is far below the cost of a trade, even on the side the data leans to. The unusual move is -0.50 % per case (strength -0.046 of a usual 10.60 % move), against a trade cost of 0.19 %. The book lost -4.8 % a year (Sharpe -0.64).

## Ideas
- No ideas: The test's result sits on the opposite side from the idea (t -0.66). Neither close location nor volume grades the move on heavy flat days in any coin, period or trend regime (F2–F4). The faint signs left, a rise after heavy flat days (t 1.1–1.5) and a fall after low closes on ordinary days (t -1.3), are not clear in any part of the data, so no amended idea rests on a clear finding.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
