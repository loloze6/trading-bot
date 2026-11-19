---
line: 7.d not profitable
backtest: 017-01_presettle-drop-after-uptrend_1h
idea tested: 017-01_presettle-drop-after-uptrend
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3247 USD
---
## Findings
- **F1:** The book does not lose on its direction but on fees: its mean daily gain before fees is -0.000124 (t -1.02 over 2922 days), against 0.001699 a day in fees. That is about 1.8 round trips a day, each costing 0.0021 per unit of allocation, while the pre-settlement 2-hour excess return the book bets on averages only 0.000067 (t 0.37).
- **F2:** The forecast's grading runs the wrong way. On active bars the largest third of |forecast| (mean |allocation| 0.82) earns -0.000066 per bar, and the coin rises +0.000145 per bar. The smallest third earns -0.000001. Across the five 72-hour-rise quintiles of settlement episodes, the 2-hour excess return is +0.000015, +0.000124, -0.000498, +0.000546 and +0.000147, with no fall that grows with the rise.
- **F3:** Of the three settlements, only 08:00 UTC shows the effect. On a 2-hour grid of up-trend cases, the 2-hour excess return falls with the standardised 72-hour rise in the window ending at 08:00 (slope -0.00134, t -4.05, top third minus bottom third -0.00227, n 2323). The window ending at 16:00 is flat (slope -0.000004, t -0.01, n 2385), and the window ending at 00:00 runs the other way (slope +0.00033, t 1.00, n 2367).
- **F4:** The 08:00 effect is not tied to the settlement itself. It belongs to a morning stretch: the slope of the 2-hour return on the rise is also negative for starts at 05:00 (t -2.07), 07:00 (t -3.26) and 08:00 UTC (t -1.99). Afternoon starts at 15:00 and 16:00 UTC have positive slopes (t +3.56 and +4.96), so after a 3-day rise the coin continues rather than reverses in the afternoon.
- **F5:** The size of the one working window barely covers the costs. Its top-third-minus-bottom-third spread of -0.00227 is about one round-trip fee (0.0021). Down-trend episodes show nothing either: 2-hour excess return 0.000078, t 0.41, n 7137.

## Ideas
- `017-01_presettle-drop-after-uptrend.d1_08-00-settlement-uptrend-fade` (from F1, F3, F5): For a coin with a strong 3-day run up, the return over the 2 hours before the 08:00 UTC funding settlement is negative, and the stronger the 3-day rise, the larger that pre-settlement decline, only at the 08:00 UTC settlement and not at 00:00 or 16:00.
- `017-01_presettle-drop-after-uptrend.d2_morning-reversal-of-3-day-rise` (from F1, F3, F4): For a coin whose 3-day return is positive, the return over the next 4 hours from 05:00 UTC is negative, and the larger the 3-day rise against its recent range, the larger that morning decline.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
