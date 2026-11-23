---
line: 7.g patterns
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound.g1_heavy-fall-closing-at-low_1d
idea tested: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound.g1_heavy-fall-closing-at-low
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4315 USD
---
## Findings
- **F1:** The coin's 20-day volatility sets the size of the next-day reversal. In the coins' own top third of 20-day volatility, a down day is followed by a next-day excess return of +0.71 % (t 5.59, 2357 days) and an up day by -0.36 % (t -3.20, 2491 days). In the bottom third, down days are followed by -0.16 % (t -2.03) and up days by -0.00 % (t -0.03).
- **F2:** The reversal is graded by the size of the move times the volatility level. On down days, regressing the next-day excess return on the day's return gives t 2.63 for the return alone and t -6.64 for the return × relative volatility term (7151 days). On all days the return × relative volatility term has t -4.34 (14500 days).
- **F3:** Inside the high-volatility third, the next day follows the day's return quintile in a steady line: +1.13 % (t 5.18) after the largest falls, +0.45 % (t 2.31), -0.00 %, -0.46 % (t -2.64), and -0.32 % (t -1.59) after the largest rises, about 970 days each. In the low-volatility third, no quintile goes past +0.10 % or below -0.26 %.
- **F4:** The high-volatility reversal (next-day return signed against the day's move) is broad.
- **F5:** The tested idea's top fifth of down-day forecasts earns only when volatility is high. Next-day excess return is +1.50 % (t 6.01, 754 days) in the high-volatility third, +0.21 % (t 1.40) in the middle third and -0.13 % (t -1.04) in the low third.
- **F6:** Close location and volume still carry their own information on down days. With the volatility-scaled return in the regression, the closeness to the low × log volume ratio has t 4.38 and the volatility-scaled return itself has t 0.03 (7151 days).
- **F7:** The book earns on short holds and loses on longer ones.
- **F8:** Weekday patterns do not hold up. The pooled weekday t-values range from -2.70 to +3.76, but the same weekday's sign changes from year to year: Wednesday has t -6.99 in 2019 and +0.70 in 2021. I count this as chance, not a finding to build on.

## Ideas
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound.g1_heavy-fall-closing-at-low.g1_volatile-regime-fall-rebound` (from F1, F2, F3, F4): The larger a coin's one-day fall, and the higher its 20-day volatility against its own past level, the more it rises over the next day.
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound.g1_heavy-fall-closing-at-low.g2_volatile-regime-rise-fades` (from F1, F2, F3): The larger a coin's one-day rise, and the higher its 20-day volatility against its own past level, the more it falls over the next day.
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound.g1_heavy-fall-closing-at-low.g3_absorption-rebound-in-turbulence` (from F5, F6, F1): The nearer a coin closes to its day's low on a down day whose volume is heavy against its prior 20-day average, the more it rises over the next day. The higher its 20-day volatility against its own past level, the larger that rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
