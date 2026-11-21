---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.b1_deeper-dip-larger-rebound
line: 7.b inconclusive
backtest: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.b1_deeper-dip-larger-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, falls by several times its 30-day average absolute daily return while its 30-day return is positive, the coin rises over the next 3 days more than its normal drift. The deeper the 24-hour fall in multiples of its 30-day average absolute daily return, and the larger its 30-day return, the larger the rise.
Consequence: A sharp one-day drop inside a strong month-long rise is a reason to buy for a few days, sized up with both the depth of the drop and the strength of the rise.
Why:
- F1: The idea grades as it predicts when the fall is measured in its own unit, but not in the test's forecast. The fall is the raw 24-hour return in multiples of the 30-day mean absolute daily return. By that raw multiple, the unusual 72-hour move falls steadily across the quintiles, deepest to shallowest: +1.55 % (t 3.58, 488 cases), +0.63 %, +0.47 %, +0.25 %, −0.13 %. The deeper half beats the shallower half by +1.38 % (Welch t 3.74). Rank correlation of the raw multiple with the move is −0.077 (p 0.0001), and a more negative multiple means a deeper fall. By the test's forecast, the quintiles show no order: +0.87 %, +0.47 %, +0.68 %, +0.01 %, +0.74 %, with rank correlation −0.004. So the supporting check failed (−0.23 %) because of how the forecast was built, not because the effect is ungraded: it standardises over 500 hours, cubes with a pivot, and is read at forecast rises of 2 points, which scrambles the ranking of depth.
- F4: The effect is mixed by period, and drowned in bear years whose 30-day rises are brief. The 2018 cases lose −2.93 % (t −4.32, 180 cases) and the 2022 cases lose −1.08 % (t −2.14). 2020, 2021 and 2025 gain +1.12 %, +2.33 % and +1.22 %.
- F5: The rebound grows with the strength of the 30-day rise as well as with the depth of the fall. By 30-day-return quintile, the unusual move rises from −0.53 % in the weakest (mean 30-day return +1.3 %) to +1.67 % (t 3.14) and +0.98 % in the two strongest. Rank correlation is 0.060 (p 0.009). Deep falls inside the stronger-than-median rises earn +1.84 % (t 4.17, 548 cases). Shallow falls inside the weaker rises earn −0.48 %.
