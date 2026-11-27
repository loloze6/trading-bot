---
line: 7.g patterns
backtest: 074-01.b1.b1.b1.b1.g1_falling-drop-bounce-fade_1d
idea tested: 074-01.b1.b1.b1.b1.g1_falling-drop-bounce-fade
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4534 USD
---
## Findings
- **F1:** In falling markets (60-day return below -10 %), the next day after an up day depends on how wide the day was: after narrow up days the next day's unusual move is +0.04 % (t 0.11, 504 cases on 192 days), after mid-width up days -0.96 % (t -2.67, 426 cases on 190 days), and after wide up days -0.95 % (t -1.98, 366 cases on 152 days).
- **F2:** In rising markets the wide up days do not fade: the next day's unusual move after them is +0.65 % (t 1.34, 521 cases on 220 days), against -0.95 % in falling markets. This is the brief's own contrast between markets.
- **F3:** Among falling-market up days with a range above their 20-day mean, the next day's fall sits almost entirely in the deepest quartile of the prior 5-day fall. That quartile has -2.72 % (t -2.84, 108 cases on 42 days); the other quartiles have -0.95 % (t -1.41), +0.09 % (t 0.14) and -1.07 % (t -1.44). The fall does not grow steadily with depth, which matches step 5's failed check on the larger half of the forecast.
- **F4:** Within those same falling wide up days, grouping by the size of the day's gain gives -1.99 % for the smallest-gain quartile (t -2.81, 108 cases on 65 days). The other quartiles give -0.75 %, -0.69 % and -1.23 % (t -1.23, -0.96, -1.43), so this is not a steady gradient either. Grouping by where the day closed in its range gives only a weak order: low third -0.85 % (t -1.19), middle -1.26 % (t -2.00), high -1.39 % (t -2.13).
- **F5:** The fade is used up within one day: over the next two days the unusual move after falling wide up days is -0.63 % (t -1.08, 425 cases on 170 days), smaller than the one-day -0.95 %.
- **F6:** No other angle stood out against the number of angles examined:

## Ideas
- No ideas: The only patterns that stand out (F3, F4) belong to the tested falling-market wide-bounce fade, which the map already holds in the falling short cells (the 074-01 family), and they are not graded. No other angle out of the roughly sixty cells examined gives a pattern that can be told apart from chance.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
