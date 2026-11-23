---
line: 7.g patterns
backtest: 029-01_failed-breakout-depth-decline.d1_thin-volume-failed-breakout-falls_1d
idea tested: 029-01_failed-breakout-depth-decline.d1_thin-volume-failed-breakout-falls
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3965 USD
---
## Findings
- **F1:** Closes above the prior 20-day closing high are followed by a rise, which is the opposite of the brief: over 799 non-overlapping breakout cases, the 5-day unusual move is +1.34 % (t 3.13) and the total move +1.93 % (t 4.49), about 10 times the 0.19 % cost of a trade. Fresh first-day breakouts alone show the same, mean 0.130 usual moves (t 3.20, 708 cases).
- **F2:** The rise after a breakout grows with how far the close clears the old high, measured in the coin's daily volatility: 0.048 usual moves (t 0.80) in the smallest third, 0.122 (t 1.76) in the middle and 0.172 (t 2.55) in the largest, 267 cases per third. The rank correlation over all cases is only 0.039, so the grading is coarse.
- **F3:** Failed breakouts are not followed by a fall: over 619 cases the mean 5-day move is +0.037 usual moves (t 0.98). Thin-volume failures lean the other way, +0.118 (t 1.67, 206 cases), and failure depth shows nothing (deep 0.034, mid 0.054, shallow 0.021).
- **F4:** On the 5-day grid, a strong up day predicts a further rise, graded by its size in units of 20-day volatility. The next 5 days average -0.022 usual moves after days within ±1 sigma (t -1.05, 2072 cases), +0.126 after 1–2 sigma up days (t 2.25, 286) and +0.222 after days above 2 sigma (t 1.82, 94). Down days of any size show nothing (−2 sigma or worse: +0.046, t 0.45).
- **F5:** The continuation after strength depends on the period. Up days above 1 sigma give +0.273 usual moves (t 3.11, 163 cases) in 2018–21 but only +0.058 (t 0.93, 217 cases) in 2022–25. Breakout cases give +0.278 (t 3.41) in 2020, +0.438 (t 3.39) in 2021 and +0.221 (t 2.14) in 2024, against −0.234 (t −2.33) in 2022.
- **F6:** The book is mostly short exposure to the coin's own moves rather than timing. On its 1358 active coin-days its daily return correlates −0.85 with the coin's, and its mean daily return across all days is only 5.2e-05. Its mean allocation when active is −1.01, against a coin drift that is positive for all six coins (+0.30 % to +0.91 % per 5 days).
- **F7:** Weekdays stand out but follow no gradient. Grid cells starting Monday average +0.135 usual moves (t 3.04) and Tuesday +0.128 (t 2.71), against −0.105 on Sunday (t −2.18), and both halves of the sample agree on Monday and Tuesday. With about fifteen angles examined, this is reported as calendar context, not as a graded idea.

## Ideas
- `029-01_failed-breakout-depth-decline.d1_thin-volume-failed-breakout-falls.g1_breakout-margin-predicts-continuation` (from F1, F2, F3): When a coin's daily close rises above its highest close of the prior 20 days, the coin rises over the next 5 days, and the further the close clears that old high relative to the coin's 20-day daily volatility, the larger the rise.
- `029-01_failed-breakout-depth-decline.d1_thin-volume-failed-breakout-falls.g2_strong-up-day-follow-through` (from F4, F5, F1): The larger a coin's daily up move relative to its 20-day volatility of daily returns, the more the coin rises over the next 5 days, most clearly while the coin's 20-day return is positive.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
