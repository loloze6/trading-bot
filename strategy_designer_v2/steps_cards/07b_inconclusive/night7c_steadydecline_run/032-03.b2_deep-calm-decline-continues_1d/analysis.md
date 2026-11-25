---
line: 7.b inconclusive
backtest: 032-03.b2_deep-calm-decline-continues_1d
idea tested: 032-03.b2_deep-calm-decline-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3303 USD
---
## Findings
- **F1:** Step 5's slope is on the side the idea predicts but too uncertain to show: slope +0.00098, t 0.68 clustered by day, supporting mean +0.74 %, 532 cases on 201 days. In folds B and C the slope on the forecast stays positive at every horizon (5, 10 and 20 days). Its day-clustered t is 1.86, 1.58 and 1.92, with 241, 241 and 222 cases falling on only 84 and 78 distinct days.
- **F2:** The grading shows in the 10-day short-side excess return by depth quartile in folds B and C, which rises in order: -1.7 %, +0.6 %, +2.5 %, +4.4 %. On the raw 28-day fall the same quartiles give -3.0 %, +0.3 %, +3.9 %, +5.8 %. The effect is present, but its scatter is wide against the coins' usual 10-day move of 14.49 %.
- **F3:** The effect is spread across the data rather than confined to one part of it, which points to too few independent days rather than a localised effect. By coin, 5 of 6 slopes are positive (t 0.76 to 1.65; LTC -0.72). By year, the raw-fall slope is positive in 2019, 2020 and 2021 (t 2.01, 1.73, 1.26) and flat in 2018 (t -0.17, 24 days).
- **F4:** Clustering by day is what removes most of the evidence, because the six default coins fall together. The raw-fall 10-day slope's t drops from 2.61 unclustered to 1.45 clustered (184 cases, 63 days). The size's t is only 0.73 across 398 days for an unusual move of +0.56 % (strength 0.051).
- **F5:** The thin-volume condition carries the effect. Among all 28-day falls in folds B and C, the 10-day slope on the depth of the fall is 0.230 (t 2.61, 184 cases) in thin volume against 0.067 (t 0.62, 110 cases) outside it.
- **F6:** The market's own rise works against the book. The coins' normal drift in the short's direction is -1.28 % per 10 days, so the total move per case is -0.72 %, which is -3.8 times the 0.19 % trade cost. The book's Sharpe is -0.25 even though the unusual move is positive.
- **F7:** The effect shows most clearly at 5 days. On the raw 28-day fall in thin volume, the 5-day slope has clustered t 2.47 (184 cases, 63 days), against 1.45 at 10 days and 0.91 at 20 days.

## Ideas
- `032-03.b2.b1_deep-calm-decline-more-coins` (from F1, F2, F3, F4): Among coins whose volume over the past 28 days is below their own usual volume, the larger the fall over those 28 days, the larger the further fall over the next 10 days.
- `032-03.b2.b2_deep-calm-decline-five-days` (from F2, F5, F7): Among coins whose volume over the past 28 days is below their own usual volume, the larger the fall over those 28 days, the larger the further fall over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
