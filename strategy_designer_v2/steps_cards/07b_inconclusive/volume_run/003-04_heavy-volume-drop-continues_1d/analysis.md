---
line: 7.b inconclusive
backtest: 003-04_heavy-volume-drop-continues_1d
idea tested: 003-04_heavy-volume-drop-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.1947 USD
---
## Findings
- **F1:** The test's measure is on the side the idea predicts but short of the bar: across 286 independent signal events the mean excess 5-day return is -0.0089 with t = -1.51, only 52% of events negative, and the median-split check passes at -0.0086.
- **F2:** The effect is graded as the idea says but carried by the strongest cases. The third with the most negative forecasts has a mean excess 5-day return of -0.0190 (t = -2.01, n = 95), the middle third -0.0114 (t = -0.95), and the weakest third +0.0034 (t = +0.37).
- **F3:** Both parts of the forecast grade the same way:
- **F4:** The effect varies a lot by period and coin, which drowns it in the pooled test:
- **F5:** The move shows at the plan's horizon and not earlier. The excess return is positive at 1 day (+0.0062, t = +1.52) and 2 days (+0.0045, t = +1.21), turns negative only from 3 days, and is deepest at 5 days (-0.0089), then fades at 10 days (-0.0054, t = -0.72).
- **F6:** Among all sharp falls (≥2 usual moves) regardless of volume, the 5-day excess is negative at both ends of volume:

## Ideas
- `003-04_heavy-volume-drop-continues.b1_heavy-volume-drop-more-coins` (from F1, F2, F4): When a coin falls sharply over one day on volume well above its own 30-day average daily volume, it keeps falling over the next 5 days. The larger the fall and the heavier its volume against that average, the larger the further loss.
- `003-04_heavy-volume-drop-continues.b2_strongest-heavy-volume-drops-continue` (from F2, F3, F5): When a coin falls sharply over one day on volume well above its own 30-day average daily volume, it keeps falling over the next 5 days, only for the largest falls on the heaviest volume against that average. The larger the fall and the heavier its volume against that average, the larger the further loss.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
