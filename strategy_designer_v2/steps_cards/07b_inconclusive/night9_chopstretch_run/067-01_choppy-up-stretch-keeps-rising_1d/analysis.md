---
line: 7.b inconclusive
backtest: 067-01_choppy-up-stretch-keeps-rising_1d
idea tested: 067-01_choppy-up-stretch-keeps-rising
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4363 USD
---
## Findings
- **F1:** The test's result is zero, not short of the bar. Over all folds the slope t is 0.73 (408 grid cases, 187 dates) and the unusual move per case is -0.05 % (t -0.09, 717 cases on 536 days), -0.016 of a usual move. The total move is -0.2 times the 0.19 % cost of a trade. More data would not help, since all four folds were already used.
- **F2:** Only the side below the average carries. In folds B and C at 5 days, closes below the 20-day average are followed by a further fall of +2.68 % in the forecast's direction (t 2.17 with one day's cases together, 145 cases on 91 days). Closes above the average are followed by -0.19 % (t -0.16, 142 cases).
- **F3:** At 10 days the short side's +3.32 % (t 1.36, 77 cases) also exceeds the long side's +0.72 % (t 0.30, 66 cases). So the plan's two-sided test mixed a side that carries with one that does not.
- **F4:** The short side is steady across the data's grid and its coins, but not across its years.
- **F5:** The grading is weak on both sides.
- **F6:** The effect is absent at longer horizons.

## Ideas
- `067-01.b1_choppy-down-stretch-keeps-falling` (from F2, F3, F4, F6): In a choppy market, the further a coin's close stands below its 20-day average, measured in units of its 20-day standard deviation of daily returns, the more the coin falls over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
