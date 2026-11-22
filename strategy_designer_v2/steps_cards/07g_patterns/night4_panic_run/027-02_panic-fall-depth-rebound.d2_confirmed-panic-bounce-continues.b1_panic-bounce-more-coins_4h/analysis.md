---
line: 7.g patterns
backtest: 027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues.b1_panic-bounce-more-coins_4h
idea tested: 027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues.b1_panic-bounce-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4804 USD
---
## Findings
- **F1:** Among the 492 panic stretches (24-hour range at least 3 times its 30-day mean, coin down; first one per 84-bar cell), a deeper 24-hour fall is followed by a higher 14-day excess return. The pooled slope of excess return on the 24-hour return is -0.325 (t -2.45). The deepest quartile (mean fall -22 %) earns +5.9 % excess (t 3.11, 123 cases), against -1.3 %, +0.2 % and +2.0 % for the shallower quartiles.
- **F2:** The depth effect in F1 is fragile. Averaged by day (171 panic days) its slope t falls to -1.65. Measured in units of the coin's own volatility, the slope is +0.003 (t 0.34, 455 cases). The slope is negative in each year from 2018 to 2023 (t -2.38 in 2021, -2.39 in 2022) but positive in 2024 (+0.22) and 2025 (+0.11). It is negative in only 65 % of the 17 coins.
- **F3:** Panic stretches as a whole earn a 14-day excess of +1.7 % over the coins' normal drift (t 1.67, 492 cases). The excess is not graded by the panic's range multiple: by quartile it is -1.4 %, +4.3 %, +4.1 % and -0.2 %. It is not graded by the prior 7-day return either: +5.8 %, +1.1 %, -4.2 % and +5.8 %.
- **F4:** The 4-hour bar opening at 16:00 UTC returns +0.10 % on average. It is positive in 18 of 19 coins (t across coins 8.96), and t 3.30 over 2,920 days when averaged across coins. The bar opening at 00:00 UTC returns +0.075 % (17 of 19 coins positive, t 4.81 across coins, t 2.02 over days). Every other 4-hour bar is within ±0.02 % (all |t| < 1.5). Both effects are less than half a trade's 0.22 % cost.
- **F5:** Fridays are the strongest day. The cross-coin daily return is +0.68 % (t 3.39 over 417 days); every other weekday is between 0.00 % and +0.27 % (t ≤ 1.11).
- **F6:** On the non-overlapping 84-bar grid (2,142 cases), only the top quintile of the 7-day return (mean +24.5 %) is followed by a positive 14-day excess: +3.4 % (t 2.50). The other four quintiles are all between -0.9 % and -1.7 %, so the relation is not graded below the top.
- **F7:** The book earned 0.014 % a day against 0.139 % a day for holding the coins, over 2,898 window-days. Its trades lost on average in 2018 (-16.4 %, 39 trades) and 2022 (-4.9 %, 112 trades), and earned most in 2024 (+10.1 %, 203 trades). This is the same year pattern as the grid's excess returns (2018 -7.2 %, 2022 -6.1 %).

## Ideas
- `027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues.b1_panic-bounce-more-coins.g1_deeper-panic-falls-rebound-more` (from F1, F2, F3): Among 24-hour stretches where a coin's range is several times its 30-day average and the coin fell, the deeper the coin's fall over those 24 hours, the higher its return over the following 14 days.
- `027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues.b1_panic-bounce-more-coins.g2_weekly-strength-continues-fortnightly` (from F6): The larger a coin's 7-day return, the higher its return over the following 14 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
