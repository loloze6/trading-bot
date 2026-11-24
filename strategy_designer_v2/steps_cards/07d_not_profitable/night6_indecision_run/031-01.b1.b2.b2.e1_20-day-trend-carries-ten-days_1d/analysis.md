---
line: 7.d confirmed, not profitable
backtest: 031-01.b1.b2.b2.e1_20-day-trend-carries-ten-days_1d
idea tested: 031-01.b1.b2.b2.e1_20-day-trend-carries-ten-days
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3790 USD
---
## Findings
- **F1:** The check failed on Calmar alone (0.506 against 0.75): the book's deepest fall of -45.8% stands against a yearly return of +23.4%. The deepest falls inside a window came in w9 (-38.2%, window return -35.7%) and w14 (-30.2%, window return -27.5%). In both, the coins' mean 20-day return was negative (-7.0% and -7.8%, against +2.6% over all bars), yet the book still held a mean allocation of 0.27 and 0.25.
- **F2:** On held days, the book's mean daily gain was -0.0007% when the coin's 5-day return was not positive (5938 coin-days), against +0.192% when it was positive (6571 coin-days). The held days after a 5-day drop carry the falls' risk and earn nothing.
- **F3:** On non-overlapping 10-day grid bars with a forecast above 0, the 10-day return minus the coin's drift was +1.77% (t 2.07, 471 cases) when the 5-day return was positive, against -0.44% (t -0.45, 223 cases) when it was not. By 5-day-return tercile it was graded: -1.07% (128), +0.18% (236), +2.51% (t 2.36, 330).
- **F4:** The 5-day-return condition is not an effect of its own. On grid bars with the forecast at 0 and a positive 5-day return, the 10-day return minus drift was -1.49% (t -1.78, 259 cases), and the top 5-day tercile with the forecast at 0 gave -1.50% (138 cases). It earns only together with the idea's scaled 20-day rise, as a trend still being pressed, which is the run's fuel in the brief's own theory.
- **F5:** The same book recomputed from its bars, holding only while the 5-day return is positive, gave a yearly return of +25.6%, a deepest fall of -28.1%, a Calmar of 0.91 and a Sharpe of 0.98. The unchanged book gave +25.2%, -45.3%, 0.56 and 0.82. A 3-day-return filter gave a Calmar of 0.78. Filters on the fall from the 20-day high did worse (Calmar 0.46 and 0.49).
- **F6:** The forecast itself is not graded beyond on/off. The 10-day return minus drift by forecast bin was +1.60% (0–5), -0.81% (5–10), -0.11% (10–15) and +2.29% (15–20). The idea's measured size is an unusual move of +0.04% (t 0.05). The total move of +1.22% is 6.3 times the 0.19% cost, so the unchanged book mostly earns the drift.
- **F7:** A wide day that closes near its open in the last 5 days goes with opposite moves depending on the forecast. With the forecast on, the top tercile of that measure was followed by +3.08% over 10 days beyond drift (t 2.24, 205 cases), against -0.77% in the bottom tercile. With the forecast off, the top tercile was followed by -2.69% (t -3.00, 215 cases). The condition carries an effect of its own and cannot serve as a repair.

## Ideas
- `031-01.b1.b2.b2.e1.d1_scaled-trend-while-still-rising` (from F1, F2, F3, F4, F5): The larger a coin's 20-day return relative to its daily volatility over those 20 days, the more the coin rises over the next 10 days, only while its 5-day return is positive.
- `031-01.b1.b2.b2.e1.d2_trend-graded-by-recent-push` (from F2, F3, F4, F5, F6): The larger a coin's 20-day return relative to its daily volatility over those 20 days, the more the coin rises over the next 10 days, and more so the larger its 5-day return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
