---
line: 7.g patterns
backtest: 058-02.b2.b1_calm-range-continuation-more-coins_1d
idea tested: 058-02.b2.b1_calm-range-continuation-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3948 USD
---
## Findings
- **F1:** The level of the close in its 20-day high-low range continues over the next 5 days, but mostly outside the tested profile. On every bar in folds B and C, the top fifth of range positions was followed by a 5-day excess return of +2.92 % (t 2.29, cases of one day taken together, 325 cases). The second-lowest fifth was followed by -1.64 % (t -2.02). The slope is positive in both folds: fold B 0.050 (t 1.87, 826 cases, 118 days) and fold C 0.065 (t 1.70, 796 cases, 138 days).
- **F2:** By trend, the raw range-position slope is largest in choppy markets and absent in falling ones. Choppy: 0.212 (t 2.69, 152 cases, 68 days). Rising: 0.107 (t 2.29, 377 cases). Falling: 0.034 (t 0.73, 437 cases). Inside choppy, calm and agitated slopes are equal: 0.185 (t 2.41, 98 cases) and 0.184 (t 1.27, 54 cases). So calmness adds nothing, contrary to the brief's contrast.
- **F3:** In choppy markets, 5-day excess returns rise steadily from the lowest to the highest fifth of range position: -9.3 %, -4.4 %, -2.0 %, +2.5 %, +5.5 % (t -1.47, -2.18, -1.55, +1.33, +1.02; about 30 cases each). This is the opposite of the brief's reversion. The cases are few.
- **F4:** The raw range position predicts better than the tested forecast. In the recorded choppy calm profile, the raw range-position fifths ran from -3.8 % (t -3.02) to +3.8 % (t 1.70) over 5 days, about 42 cases each. Yet the standardised forecast's slope had t 0.87. Standardising against its own past 60 values appears to remove the level that carries the effect.
- **F5:** The book's gain comes from its long side only. Its 396 long trades averaged +2.18 % before fees (+2.08 % after); its 428 short trades averaged -0.06 % (-0.16 % after). The book returned +3.6 % a year, with a Sharpe of 0.36, which is 0.20 below holding the coins.
- **F6:** Outside the profile, very large one-day rises carry on. The top fifth of the one-day move scaled by its 20-day swing was followed by a +1.90 % 5-day excess return (t 2.40, 267 cases). In choppy markets the slope was 0.035 (t 2.22, 152 cases). Given how many angles I looked at, this is not strong enough to stand alone.

## Ideas
- `058-02.b2.b1.g1_choppy-range-position-continuation` (from F1, F2, F3, F4): In a choppy market, the higher a coin's close sits within its 20-day high-low range, the larger its rise over the next 5 days, and the lower it sits, the larger its fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
