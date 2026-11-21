---
idea: 018-04_hourly-surge-multiday-continuation.d2_post-selloff-surge-fades
brief: 018_daily-condition-caught-on-the-hour
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: afc0f50f6fe7
---
Fidelity:
- Situation: 24-hour return, read at an hourly close, first reaches several times the 30-day average absolute daily return, upside -> replaced: no component divides the 24-bar return by the 30-day mean absolute 24-bar return; the nearest one uses an hourly standard deviation times sqrt(24).
- Comparison: the 7-day return before that day was a fall, and a deeper fall means a larger shortfall -> kept: VolatilityScaledReturnComponent (period 168, lag 24) is negative after a fall, and its size grows with the fall.
- Outcome: the price rises less than the coin's usual 5-day return over the next 5 days -> kept: graded short against holding the coin, with a horizon of 5 days (120 bars).
- Verdict transfer: no: a trigger built on a different usual-move scale would not test the idea's "several times its average absolute daily return" condition.
Reason: Each part comes from one coin's own closes, and a regime rule could hold the trigger. But no catalogue component gives the 24-bar return as a multiple of the mean absolute 24-bar return over 720 bars. The config cannot divide one component by another: rules compare raw values, and score_product divisors are constants.
