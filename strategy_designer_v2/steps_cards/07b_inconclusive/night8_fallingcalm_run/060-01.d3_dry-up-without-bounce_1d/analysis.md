---
line: 7.b inconclusive
backtest: 060-01.d3_dry-up-without-bounce_1d
idea tested: 060-01.d3_dry-up-without-bounce
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2197 USD
---
## Findings
- **F1:** Step 5's main measure points the way the idea predicts but falls short of the bar: the mean short-side excess 5-day return is +0.90 % with t 1.11 on 445 short cases over 191 days. The size has the same sign: +0.62 %, t 1.16 over 419 days, a strength of 0.057, which is the usual size of a real idea. So the effect is ordinary in size, and this data has too few cases to tell it from 0.
- **F2:** The effect grows with the forecast, as the idea says, but is loud only in its strongest cases. In folds B and C the top third of |forecast| gives +4.17 % (t 1.75, 83 cases), against +0.84 % and +0.73 % for the low and middle thirds (85 and 82 cases). Step 5's split of the larger half minus the smaller half is also positive, at +1.78 %.
- **F3:** In falling markets the idea's situation carries the effect and the other cells do not. Shrinking volume while still sliding gives +3.50 % short-side excess over 5 days (t 1.93, 140 cases). Shrinking volume after a bounce gives -1.09 % (t -0.54, 78), growing volume while sliding -1.55 % (t -0.58, 107) and growing volume after a bounce -0.46 % (t -0.29, 76). This matches the brief's claim that the dry-up, not the fall alone, carries the continuation.
- **F4:** The effect is mixed across periods and diluted by the market's own moves:
- **F5:** The plan's horizon is not the wrong place to look. On the same cases the excess return grows with the horizon: +0.03 % at 1 day (t 0.05), +0.73 % at 3 days (t 0.87), +1.91 % at 5 days (t 1.51) and +2.77 % at 10 days (t 1.62), measured on the 5-day grid. No other horizon gives a clean, clearly stronger answer. Cutting to the strongest cases would leave far fewer than the 140 to 250 cases already too few for t 2, so the problem is the number of cases.
- **F6:** The test used only the six default coins, while 13 more coins have daily bars in fold A and fold D and in part of folds B and C. Adding them is the only way to add independent cases to an effect of strength 0.057 that sits on the predicted side at t 1.1.

## Ideas
- `060-01.d3.b1_dry-up-slide-all-coins` (from F1, F3, F4, F6): In a falling market, the more a coin's trading volume over the past 30 days has shrunk against the 30 days before, the larger its fall over the next 5 days, and the larger still the lower its 5-day return, the continuation vanishing after a 5-day bounce.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
