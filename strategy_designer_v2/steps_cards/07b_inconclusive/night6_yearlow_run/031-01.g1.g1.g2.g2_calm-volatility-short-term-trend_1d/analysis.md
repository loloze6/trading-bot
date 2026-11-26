---
line: 7.b inconclusive
backtest: 031-01.g1.g1.g2.g2_calm-volatility-short-term-trend_1d
idea tested: 031-01.g1.g1.g2.g2_calm-volatility-short-term-trend
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2085 USD
---
## Findings
- **F1:** The 14-day trend predicts the next move in both regimes, and calm is only modestly steeper: on the 2-day grid the slope is 24.6 bp per z in calm (t 2.44, 3536 cases) against 16.2 bp outside calm (t 1.72, 2666 cases), and at 10 days it is 135 bp (t 2.30, 627 cases) against 95 bp (t 1.99, 488 cases). Both gaps carry a difference t of only about 0.5 to 0.6, which is why step 5's check (+0.000178, passed: False) falls short.
- **F2:** The slope does fall as volatility rises, in the direction the idea predicts, but each step is noisy: across the volatility-ratio quintiles at 2 days it is 40.9, 33.7 and 37.0 bp per z (t 1.79, 1.89, 2.58) in the three calmest fifths, and 15.2 and 14.1 bp (t 1.07, 1.04) in the two most volatile, with 1154 cases each.
- **F3:** In calm stretches the effect sits on the rise side only: after 14-day rises the calm slope is 71.5 bp per z (t 3.29, 1716 cases), after falls it is -20.3 bp (t -0.74, 1820 cases), and after rises outside calm it is only 13.4 bp (t 0.61, 1284 cases).
- **F4:** The calm effect is broad but thin per slice: the calm slope is positive on all six coins (6.8 to 42.1 bp, no t above 1.57, about 580 cases each) and in 6 of 8 years, while 2025 is negative (-38.2 bp, t -1.32), so six coins give too few cases to separate calm from non-calm.
- **F5:** The 2-day demeaned moves by decile of the standardised 14-day return show continuation at the top (+0.85 % and +0.42 % in the two highest deciles) but not at the bottom, where the lowest decile is followed by +0.28 %. This agrees with F3: large falls do not extend.
- **F6:** The idea's size is a strength of 0.053, with an unusual move of +0.35 % per 2-day case (t 2.15, 1383 days, 2811 cases), which is 1.8 times the 0.19 % cost of a trade.

## Ideas
- `031-01.g1.g1.g2.g2.b1_calm-trend-on-all-coins` (from F1, F2, F4): When a coin's 20-day volatility is low relative to its usual level, its 14-day return grades its move over the next 2 days more steeply: the larger the rise or fall, the larger the move in its direction.
- `031-01.g1.g1.g2.g2.b2_calm-rises-keep-rising` (from F3, F5): When a coin's 20-day volatility is low relative to its usual level, its 14-day rise grades its move over the next 2 days: the larger the rise, the larger the further rise that follows.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
