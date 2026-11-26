---
line: 7.g patterns
backtest: 060-01.d1_deep-dry-up-longer-fall_1d
idea tested: 060-01.d1_deep-dry-up-longer-fall
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4123 USD
---
## Findings
- **F1:** In a falling market the coin's 20-day excess return rises with its 30-day volume ratio rather than falling with the shrinkage, and nearly all of the effect sits in the growing-volume quarter: the slope is +0.122 (t 2.94, 99 non-overlapping cases), but only t 1.80 with the cases of one day taken together (24 days).
- **F2:** Across the falling-market volume quartiles the 20-day excess return is −6.8 % (deepest shrink), −8.0 %, −5.5 % and +7.9 % (most growth), with medians −19.0 %, −12.9 %, −7.7 % and +9.2 %; shrinkage beyond the middle adds no further fall, which is why the tested forecast's slope t is −0.015.
- **F3:** The falling-market slope of 20-day excess return on the volume ratio is positive in all six coins (BTC +0.04, ETH +0.23, LTC +0.14, XMR +0.17, XRP +0.14, ZEC +0.10) and in both folds (B +0.031, t 0.65 on 40 cases; C +0.132, t 2.38 on 59 cases).
- **F4:** The volume effect is not the past fall in disguise: in falling markets the volume ratio's correlation with the past 20-day return is −0.07, and with both in one regression the volume coefficient stays at +0.118 (t 2.86) while the past 20-day return's coefficient is −0.17 (t −1.14).
- **F5:** At a 10-day horizon the same falling-market relation is weaker, with slope +0.038, t 2.00 on 193 cases but t 0.86 with the cases of one day taken together (45 days), so it builds over weeks rather than days.
- **F6:** In falling agitated markets a larger down day in units of its 30-day swing is followed by a larger next-day excess return (slope −0.0158 per unit of z, t −3.09 over 215 days; mean +0.72 %). This is the rebound the profile map already holds 12 times in falling agitated long, so it is not a discovery.
- **F7:** Falling-market up days are followed by a negative next-day excess return (−0.71 % agitated, −0.36 % calm), but the size is not graded by the day's move (slopes t −0.49 and 0.21), so it is not a usable pattern.

## Ideas
- `060-01.d1.g1_falling-volume-growth-reversal` (from F1, F2, F3, F4, F5): In a falling market, the more a coin's trading volume over the past 30 days has grown against the 30 days before, the more the coin rises over the next 20 days: growing volume marks the point where the fall stalls and turns.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
