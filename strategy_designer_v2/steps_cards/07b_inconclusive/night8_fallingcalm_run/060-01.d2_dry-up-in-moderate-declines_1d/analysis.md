---
line: 7.b inconclusive
backtest: 060-01.d2_dry-up-in-moderate-declines_1d
idea tested: 060-01.d2_dry-up-in-moderate-declines
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.4951 USD
---
## Findings
- **F1:** The test's own result is on the side the idea predicts but short of the bar: the short cases' mean unusual 5-day move is +0.91 % with t 1.70 over 487 cases on 377 days, and the strong-minus-weak check passed at +0.59 %. The effect is real-signed but too small for this sample to show clearly, and the data holds 13 more coins than the six tested.
- **F2:** In folds B and C, the same cases give a mean unusual move that grows with the horizon: +0.70 % at 5 days (t 0.83, 315 cases, 195 days), +1.63 % at 10 days (t 1.34, 306 cases) and +4.74 % at 20 days (t 2.31, 274 cases, 172 days). The plan's 5-day horizon reads the drift where it is still small against a usual 5-day move of 10.60 %.
- **F3:** In falling markets in folds B and C, shrunk volume behaves differently from grown volume at 5 days: +1.86 % after shrunk volume (t 1.33, 218 cases) against −1.10 % after grown volume (t −0.64, 183 cases). The most-shrunk third gives +3.95 % (t 1.90, 73 cases) against +0.31 % to +1.29 % for the other two thirds, as the brief's dry-up claim expects.
- **F4:** The fall-moderation part of the idea does not show at 5 days:
- **F5:** The effect is mixed across periods and coins, which drowns it in a small sample:
- **F6:** The book still lost money:

## Ideas
- `060-01.d2.b1_dry-up-moderate-declines-all-coins` (from F1, F3, F5): In a falling market, the more a coin's trading volume over the past 30 days has shrunk against the 30 days before, the larger its fall over the next 5 days, and more so the more moderate its 20-day fall has been, the continuation fading as the 20-day fall turns into a plunge.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
