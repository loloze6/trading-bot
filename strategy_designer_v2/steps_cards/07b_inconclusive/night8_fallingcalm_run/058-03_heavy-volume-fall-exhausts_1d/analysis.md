---
line: 7.b inconclusive
backtest: 058-03_heavy-volume-fall-exhausts_1d
idea tested: 058-03_heavy-volume-fall-exhausts
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.1909 USD
---
## Findings
- **F1:** The test's own result is on the side the idea rules out: heavy minus quiet 5-day return is -1.29 % with Welch t -0.98 (58 heavy against 408 quiet cases). In folds B and C it is -0.48 % with t -0.20 (25 heavy against 243 quiet), and the idea's size is only +0.08 % of unusual move (t 0.13 over 305 days, strength 0.017).
- **F2:** Heavy volume is rare in a falling, calm market. Only 25 of 268 cases in B and C have a positive forecast, and 4 windows (w7, w16, w17, w18) have none at all. Calm declines are almost always quiet-volume declines, so the comparison rests on a handful of heavy cases.
- **F3:** The effect has no grade across the forecast. The 5-day mean return by forecast quintile goes -1.6 %, +0.7 %, +2.9 %, -1.5 %, -0.5 % from quietest to heaviest. By raw volume-ratio quintile it goes -1.0 %, +1.6 %, +0.8 %, -1.0 %, -0.4 %. The correlation between forecast and return is 0.014.
- **F4:** The sign changes from coin to coin and from year to year, with no stable subset:
- **F5:** No other horizon or depth of fall shows the effect clearly:
- **F6:** The brief's main claim does not show either. Quiet-volume cases fall about the same whatever the depth of the fall: -0.4 % (deepest third), -1.4 % (middle third) and +0.3 % (shallowest third) over 5 days. Deeper calm declines are not followed by more falling.

## Ideas
- No ideas: The test's result is on the side the idea rules out. No coin, period, horizon or depth of fall shows the heavy-volume exhaustion clearly (F1, F3, F4, F5), and the brief's own continuation is absent too (F6), so the theme's effect is not in the data.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
