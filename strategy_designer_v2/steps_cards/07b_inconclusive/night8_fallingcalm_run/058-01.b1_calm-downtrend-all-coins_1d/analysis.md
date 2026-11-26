---
line: 7.b inconclusive
backtest: 058-01.b1_calm-downtrend-all-coins_1d
idea tested: 058-01.b1_calm-downtrend-all-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3659 USD
---
## Findings
- **F1:** Inside the falling-calm profile, the graded effect is absent: in folds B and C, the slope of the 5-day excess return on the 30-day fall is +0.012 (t 0.11, 206 cases on 69 days), against the idea's predicted negative sign. Step 5's own slope over all folds was negative but tiny (t -0.61, 981 cases on 271 days).
- **F2:** A deeper fall is not followed by more falling. Across quartiles of the 30-day fall, the 5-day excess returns run, from deepest to shallowest, -0.17 % (mean fall -36 %), -1.25 %, -4.75 % and +2.30 %. Across quartiles of the short size, they swing between +1.21 % and -2.65 % with no order.
- **F3:** The calm downtrend is not where the continuation lives. Cases with a negative 30-day return outside the profile end lower than inside it: -1.79 % (t -1.49, 452 cases) against -0.96 % (t -0.91, 265 cases). Falling-agitated markets show the opposite slope on the fall (+0.257, t 1.67).
- **F4:** The brief's volume split points the predicted way but cannot be told from zero.
- **F5:** The short cases' mean excess changes sign by year and coin, so what little there is comes from the period, not the situation.
- **F6:** Longer horizons give no clearer answer. The in-profile short cases' mean excess is -0.76 % at 10 days (t -0.40, 158 cases) and -3.0 % at 20 days (t -0.64, 81 cases). The correlation of the 30-day fall with the excess return stays between -0.19 and +0.03.

## Ideas
- No ideas: The theme's effect is not in the data. The test already used every coin and fold available. Within the falling-calm profile, a deeper 30-day fall is not followed by more falling at 5, 10 or 20 days (F1, F2, F6), and the continuation is no stronger there than outside it (F3). Even the brief's quiet-volume condition shows only a sign with t -0.91 (F4), and the residual changes sign by year and coin (F5).

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
