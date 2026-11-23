---
line: 7.d confirmed, not profitable
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g1_volatility-scaled-fall-next-day-rebound_1d
idea tested: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g1_volatility-scaled-fall-next-day-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3844 USD
---
## Findings
- **F1:** The check failed on Calmar alone (0.50 against 0.75), and the cause is one deep fall: the book lost 30.2 % over 119 days from w8 into w9 (w9 alone −20.8 %), while holding the coins lost 40.2 % over the same stretch, against a yearly return of only +15.2 %.
- **F2:** The rebound depends on whether the coin's volatility is rising or falling, measured as the 20-day volatility against the 60-day volatility, and the dependence is graded. On signal days in the calmest fifth (ratio below 0.75) the next day's unusual move is −0.31 % (t −2.43, n 1454) and the position loses 0.10 % a day. In the next fifths it is +0.17 %, +0.15 % and +0.25 %. In the most expanding fifth (ratio above 1.16) it is +0.64 % (t 4.58, n 1389), and the position gains 0.37 % a day against about 0.04 % of fees.
- **F3:** Rising volatility does not predict a rise on its own. On days without the signal, the most expanding fifth has a next-day unusual move of −0.27 % (n 1511) and the calmest fifth −0.21 % (n 1446), so the volatility condition is not a separate effect. It is the idea's own theory: a fall counts as a forced, rebounding fall only when the coin is in a phase of stress, not when a calm coin is drifting down.
- **F4:** Rebuilding the book from its own bar gains and fees reproduces the base result (Calmar 0.52, deepest fall −30.2 %). Leaving out the calmest fifth changes it as follows:
- **F5:** Over a 3-day horizon on non-overlapping cases, the contrast grows. Signal days in the most expanding fifth are followed by +2.02 % unusual move (t 4.21, n 426), more than ten times the 0.19 % cost of a trade. Signal days in the calmest fifth are followed by −1.29 % (t −3.16, n 448).
- **F6:** The forecast's grading holds at the next day's horizon:
- **F7:** Inside the deepest fall (w8 and w9), signal days lost money in the calmer and middle volatility fifths: summed position gains of −0.46 in the calmest fifth and −0.78 in the middle fifth. They earned in the expanding ones: +0.89 and +0.50.

## Ideas
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g1_volatility-scaled-fall-next-day-rebound.d1_rebound-under-expanding-volatility` (from F2, F3, F4, F7, F1): The larger a coin's fall on a day, measured in units of its own 20-day daily volatility, the more the coin rises over the next day. The rebound is larger the further its 20-day volatility stands above its 60-day volatility.
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g1_volatility-scaled-fall-next-day-rebound.d2_three-day-stress-fall-rebound` (from F5, F2, F3, F6): The larger a coin's fall on a day, measured in units of its own 20-day daily volatility, the more the coin rises over the next 3 days. The rise is larger the further its 20-day volatility stands above its 60-day volatility.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
