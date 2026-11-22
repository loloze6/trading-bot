---
line: 7.b inconclusive
backtest: 026-03_weekend-reversal-exceeds-weekday_1h
idea tested: 026-03_weekend-reversal-exceeds-weekday
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3633 USD
---
## Findings
- **F1:** The weekend reversal the idea needs is absent: after Monday 00:00 UTC the unusual 48-hour move in the reversal direction averages -0.24 % (t -1.56, 2387 cases), the graded slope of the next 48 hours on the weekend's standardised move is -0.017 (t -0.62), and even the largest-move fifth gives only +0.32 % (t 0.77, 478 cases); step 5's own check is -0.00095.
- **F2:** The main measure's positive difference (+0.031, Welch t 0.84) comes from the weekday comparison group, not from the weekend. Friday-ending cases have a reversal score of -0.069 (t -2.19), and their next 48 hours follow the past 48 hours with slope +0.056 (t 3.38, 2392 cases), which is momentum. Comparing Monday with all Tuesday-to-Friday cases leaves a difference of only 0.025 (Welch t 0.77).
- **F3:** What looks like continuation after weekend falls is Monday-Tuesday's own drift, and it is not graded. The next 48 hours from Monday 00:00 average -0.38 % above the coin's normal drift (t -2.52). Net of that drift, cases after a fall show -0.29 % (t -1.27) and cases after a rise +0.25 % (t 1.20). Among falls, the smallest fifth gives -1.16 % (t -2.99) while the largest gives +0.34 % (t 0.56).
- **F4:** That Monday-Tuesday drift changes sign across years: -2.08 % in 2018 (t -3.78), +1.28 % in 2020 (t 3.27) and -0.76 % in 2025 (t -2.13), so it is no stable effect.
- **F5:** The Friday continuation of the Wednesday-Thursday 48-hour move is strongest in 2018 (slope 0.156, t 4.12), 2022 (0.189, t 3.11) and 2025 (0.169, t 3.88). It is negative in 2019 (-0.112, t -1.98), 2020 (-0.064) and 2023 (-0.062). It is positive in 5 of 6 coins (ZEC 0.138, t 3.53; ETH 0.092, t 2.40) and negative only in XMR (-0.035).
- **F6:** Per case the tested book's total move is -0.26 % over 48 hours against a trade cost of 0.19 %, on a usual 48-hour move of 6.56 %. A move one usual size large with F2's slope of 0.056 would carry about 0.37 %, roughly twice the cost.

## Ideas
- `026-03_weekend-reversal-exceeds-weekday.b1_midweek-moves-continue-into-weekend` (from F2, F5, F6): A coin's 48-hour return over Wednesday and Thursday is followed by a move in the same direction over the next two days, Friday and Saturday, and the larger the Wednesday-Thursday move, the larger the move that follows.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
