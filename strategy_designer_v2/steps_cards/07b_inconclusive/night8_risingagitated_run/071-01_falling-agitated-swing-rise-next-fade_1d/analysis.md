---
line: 7.b inconclusive
backtest: 071-01_falling-agitated-swing-rise-next-fade_1d
idea tested: 071-01_falling-agitated-swing-rise-next-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3595 USD
---
## Findings
- **F1:** The tested slope is on the wrong side of the idea and indistinguishable from zero (slope +0.00015 per unit of forecast, day-clustered t 0.49, 1326 cases on 633 days). In folds B and C, in-profile up days show no grading by scaled rise. By quintile of the rise in 20-day swings (mean 0.08 to 1.62), the next-day excess return is -1.32 %, -0.18 %, -2.05 %, -1.05 % and +0.32 %. The largest rises are followed by a gain, not the largest fall (slope +0.0066, corr +0.067, n 542).
- **F2:** Ungraded, the brief's fade is there. In-profile up days are followed by a mean next-day excess return of -0.86 % (day-clustered t -2.03, 542 cases on 225 days). In-profile down days are followed by +1.37 % (t 5.45, n 560). Step 5's own size agrees: unusual move +0.61 % in the short's direction, t 2.38 over 445 days. So the result is unclear because the fade is a level effect of being an up day, not one that grows with the rise.
- **F3:** The effect lives in the falling, agitated profile. Outside it, up days in every scaled-rise quintile are followed by excess returns between -0.28 % and +0.02 % (t between -1.39 and +0.10, about 597 cases each). Inside it, the mean is -0.86 %.
- **F4:** Among in-profile up days, the fade grows with the coin's fall over the 5 days before the up day, at least across the lower three quintiles of that fall:
- **F5:** The graded giveback seen across all in-profile days comes from reversal on both sides of zero, not from the size of up days. On all in-profile days, the next-day excess return falls with the signed scaled return (slope -0.0116, corr -0.186, n 1102). But the graded part is carried by down days, which rebound more the larger the fall (slope +0.016 per swing unit, corr +0.189, n 560). The brief, short only, does not name that side.
- **F6:** The fade is spread across coins and years rather than held by one part:

## Ideas
- `071-01.b1_post-plunge-up-day-next-fade` (from F1, F2, F3, F4, F6): In a falling, agitated market, an up day is partly given back over the next day, and the steeper the coin's 5-day return was before that up day, the larger the next day's fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
