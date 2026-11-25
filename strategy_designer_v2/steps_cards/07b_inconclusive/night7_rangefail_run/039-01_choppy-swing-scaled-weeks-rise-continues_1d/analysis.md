---
line: 7.b inconclusive
backtest: 039-01_choppy-swing-scaled-weeks-rise-continues_1d
idea tested: 039-01_choppy-swing-scaled-weeks-rise-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3669 USD
---
## Findings
- **F1:** The test's result points the way the idea predicts but stops short of the bar: the slope t is 1.91 on 429 grid days with a directional mean excess of +0.41 %. Its size is small: the unusual move is +0.67 % per case over 5 days (t 1.98 over 1171 days), 0.035 of the coin's usual 12.35 % move. All 19 coins and all four folds were already used, so there is no more 1d data to add.
- **F2:** In folds B and C, the effect sits in calm choppy bars and not in agitated ones.
- **F3:** The effect is uneven over time.
- **F4:** The grading is not smooth.
- **F5:** The two sides behave differently.
- **F6:** The horizon is roughly right but could be longer. In B and C the slope t is 1.44 at 1 day, 2.00 at 3 days, 2.11 at 5 days, 2.30 at 10 days and 1.44 at 20 days. Over 15 days in calm bars it is only 0.07.

## Ideas
- `039-01.b1_choppy-calm-swing-continuation` (from F1, F2, F6): In a choppy, calm market, the more of its own 20-day daily swings a coin's 20-day rise spans, the more it rises over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
