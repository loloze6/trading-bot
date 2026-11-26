---
line: 7.b inconclusive
backtest: 037-01_choppy-swing-scaled-fall-continues_1d
idea tested: 037-01_choppy-swing-scaled-fall-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3933 USD
---
## Findings
- **F1:** The test's main result is on the side the idea predicts but well short of the bar: the mean short-direction 5-day unusual move is +0.65 % (t 0.94, 776 cases on 288 days). The coins' normal drift of -0.80 % in the short direction turns the total move per case negative (-0.28 %), and the book lost money (Sharpe -0.08, -2.2 % a year). The test already used all four folds and all 19 coins, so no more data is available.
- **F2:** In folds B and C the 5-day continuation after a choppy-market fall is clearer than in the test as a whole: +2.87 % unusual move, t 2.20 on 187 cases over 99 days. Folds A and D must therefore carry little or none of it, so the effect is not spread evenly over periods.
- **F3:** In folds B and C the effect sits where the 5-day fall extends a longer fall. When the coin's 20-day return is also negative, the 5-day unusual move is +4.36 % (t 2.32, 118 cases on 64 days). When the 20-day return is positive it is +0.81 % (t 0.66, 53 cases on 38 days).
- **F4:** The effect is graded by the fall's size in swing units, as the idea claims, but noisily. By z-quartile of the 5-day return over the 20-day swing (folds B and C), the 5-day unusual move runs:
- **F5:** Agitation does not mark a home for the effect, so no profile beyond choppy is supported. Agitated cases show +6.56 % (t 2.23, 47 cases) and calm cases +2.94 % (t 2.15, 102 cases). Within calm, the deeper half carries the effect (+4.49 %, t 2.72), while the shallow half does not (+1.52 %, t 0.87).
- **F6:** The effect is broad across coins but thin. Without DOGE (+11.5 %, t 3.49 on 8 cases) the 5-day mean is +2.48 % with t 1.89. The six core coins give +2.27 % with t 1.77. Windows w8, w11 and w17 are negative.

## Ideas
- `037-01.b1_choppy-extended-fall-continues` (from F1, F2, F3, F4, F6): In a choppy market, the more of its own 20-day daily swings a coin's 5-day fall spans, the more the coin falls over the next 5 days, only while its 20-day return is also a fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
