---
line: 7.b inconclusive
backtest: 033-03_downside-break-continues-falling_1d
idea tested: 033-03_downside-break-continues-falling
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3530 USD
---
## Findings
- **F1:** In folds B and C, closes below the 20-day low were not followed by a fall: the 53 cases (22 days) had a mean excess 5-day fall of -1.27 % (t -0.44) and a 1-day excess fall of -2.77 % (t -2.06), so the coins bounced instead. The small positive main measure (+0.78 %, t 0.67) must therefore come from folds A and D.
- **F2:** The downside effect is not graded the way the idea predicts. In folds B and C, the deepest quartile of breaks had an excess fall of -2.7 % and the shallowest +1.4 %. The year results flip sign: +1.7 % in 2018 (27 cases) and -11.3 % in 2021 (12 cases, only 2 days). The test was inconclusive because the effect is mixed, not because it is too small.
- **F3:** The mirror case, closes above the 20-day high, carries a clear drift. Its 66 cases (39 days) had a mean excess rise of +5.10 % over 5 days (t 2.31), +8.43 % over 10 days (t 2.70) and +7.96 % over 20 days (t 2.59). It held on 5 of 6 coins (LTC -0.3 %), but it was not larger for deeper breaks (shallow half +5.9 %, deep half +4.3 %).
- **F4:** Across all grid bars, the place of the close in its 20-day range relates to the next 5 days only at the top. The correlation is 0.127, and the top decile had an excess rise of +3.44 % (t 2.38, 143 cases, 67 days), the ninth +2.03 %. The bottom deciles are mixed: the lowest -0.38 % (t -0.16), the third -3.16 % (t -2.70).
- **F5:** The top-of-range drift depends on the market's trend. In the top quintile of range position, the excess rise over 5 days was +5.00 % (t 2.69, 108 cases, 50 days) in a rising market (60-day return above +10 %), against +0.83 % (t 0.58, 145 cases, 61 days) in a choppy one. Over 10 days the whole top quintile reached +4.67 % (t 2.77).

## Ideas
- `033-03.b1_upper-range-drifts-higher` (from F3, F4): The higher a coin's daily close sits within its 20-day high-to-low range, the more the coin rises over the next 10 days, most of all when the close is above the 20-day high.
- `033-03.b2_rising-market-range-top-continuation` (from F4, F5): In a rising market, the higher a coin's daily close sits within its 20-day high-to-low range, the more the coin rises over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
