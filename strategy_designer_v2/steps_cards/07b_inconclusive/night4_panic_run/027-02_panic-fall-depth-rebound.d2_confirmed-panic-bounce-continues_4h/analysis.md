---
line: 7.b inconclusive
backtest: 027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues_4h
idea tested: 027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2133 USD
---
## Findings
- **F1:** Step 5's main measure is on the side the idea predicts but short of the bar: slope +0.000655 with t 1.24 over 797 independent cases, and the supporting check passed (+0.72 % mean excess for the 471 positive-forecast cases). My rebuild agrees: slope +0.000688, t 1.28, 814 cases, Spearman 0.04. The effect is small: its strength is 0.057 of a usual 14-day move of 17.66 %.
- **F2:** The test measured the idea where it is still forming. The slope on the forecast turns from negative to positive as the horizon lengthens: −0.000736 (t −4.43, 921 cases) over 1 day, −0.000371 (t −1.83) over 2 days, +0.000213 (t 0.62) over 7 days, +0.000688 (t 1.28) over 14 days, and +0.00245 (t 2.84, 756 cases) over 21 days.
- **F3:** Over 21 days the excess return rises with the bounce across the four upper forecast quintiles: −6.8 %, −2.6 %, +2.9 % and +5.2 % (mean forecasts −6.0, +2.2, +8.0, +17.0). The exception is the deepest continued-fall quintile (forecast −17.7), at −2.0 %.
- **F4:** Over 14 days the effect is mixed in its form.
- **F5:** Over 14 days the effect is also uneven across coins and years, which leaves the six default coins too few to show it clearly.
- **F6:** The slope is clearer when the coin was rising over the 30 days before (t 2.45, 302 cases) than when it was falling (t 0.35, 279 cases). This is the pattern the brief names as refuting its theory, so I build no idea on it.

## Ideas
- `027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues.b1_panic-bounce-more-coins` (from F1, F5): Among 24-hour stretches where a coin's range is several times its 30-day average and the coin fell, the larger the coin's rise over the 24 hours after the stretch, the higher its return over the following 14 days.
- `027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues.b2_panic-bounce-three-week-horizon` (from F2, F3): Among 24-hour stretches where a coin's range is several times its 30-day average and the coin fell, the larger the coin's rise over the 24 hours after the stretch, the higher its return over the following 21 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
