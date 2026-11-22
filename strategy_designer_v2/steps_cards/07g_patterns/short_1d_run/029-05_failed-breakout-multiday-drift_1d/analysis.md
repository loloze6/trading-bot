---
line: 7.g patterns
backtest: 029-05_failed-breakout-multiday-drift_1d
idea tested: 029-05_failed-breakout-multiday-drift
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3876 USD
---
## Findings
- **F1:** Over 8 days a coin moves against its last daily return, scaled by its 20-day volatility. Regressed on that scaled return, the 8-day unusual move has a slope of -0.0165 with t -4.57 over 1691 independent cases. The lowest quintile is followed by +2.87 % (t 3.20) and the fourth quintile by -2.30 % (t -3.64).
- **F2:** This reversal holds in every coin and in both halves of the windows. Top-minus-bottom quintile differences run from -1.9 % (LTC) to -9.0 % (ZEC), with Spearman rho from -0.087 to -0.188. In w1-12 the extreme quintiles have t +3.36 and -3.95; in w13-24, +1.40 and -1.80.
- **F3:** The failures the book shorts are followed by rises, not falls. Over 8 days from the failure close the unusual move is +4.56 % (t 2.71, 131 cases); from 2 days later it is +3.80 % (t 1.90, 129 cases). The book's own cases average -0.36 % short-side (t -0.52), and its Sharpe is -0.40.
- **F4:** Inside the quintile of the largest down days relative to volatility, a failure adds to the rebound. Failures are followed by +7.43 % (t 2.61, 57 cases), against +1.96 % (t 2.16, 285 cases) for other days in that quintile.
- **F5:** Shallower failures rebound more than deeper ones, the reverse of the tested grading. The shallower depth half is followed by +6.10 % (t 2.27, 66 cases), the deeper half by +3.00 % (t 1.48, 65 cases).
- **F6:** Down days on heavy volume rebound most. A down day in the highest tercile of volume against its 20-day mean is followed by +3.04 % over 8 days (t 2.94, 294 cases), against +0.96 % (t 1.14) in the lowest tercile. An up day in the lowest volume tercile is followed by -1.73 % (t -2.57).
- **F7:** The book's short exposure does not follow the reversal. The share of bars held short stays between 25 % and 30 % in every quintile of the scaled daily return, so the shorts come no more after up days than after down days.
- **F8:** Daily returns differ by weekday: Saturday averages +0.45 % (t 5.53, 2484 days) and Friday +0.33 % (t 3.51). This is one angle among many I looked at and is not graded.

## Ideas
- `029-05_failed-breakout-multiday-drift.g1_volatility-scaled-daily-return-reversal` (from F1, F2, F7): The larger a coin's daily rise in units of its 20-day volatility, the larger its fall over the next 8 days, and the larger its daily fall in those units, the larger its rise over the next 8 days.
- `029-05_failed-breakout-multiday-drift.g2_failed-breakout-rebound-bounce` (from F3, F4, F5): After a coin closes back below its old 20-day high within 3 days of breaking above it, it rises over the next 8 days, and the larger the failure day's fall in units of its 20-day volatility, the larger that rise.
- `029-05_failed-breakout-multiday-drift.g3_heavy-volume-selloff-rebound` (from F6, F1): The heavier a coin's volume on a down day, relative to its 20-day average volume, the larger its rise over the next 8 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
