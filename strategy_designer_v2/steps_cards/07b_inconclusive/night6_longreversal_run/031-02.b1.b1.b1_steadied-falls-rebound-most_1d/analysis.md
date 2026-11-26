---
line: 7.b inconclusive
backtest: 031-02.b1.b1.b1_steadied-falls-rebound-most_1d
idea tested: 031-02.b1.b1.b1_steadied-falls-rebound-most
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4070 USD
---
## Findings
- **F1:** The test's result goes against the idea, not just short of the bar: on 89 non-overlapping 30-day cases inside a deep 90-day fall, the slope of excess return on the forecast is -0.0042 (t -1.33), and on the raw 30-day return it is -0.23 (t -1.68, 59 cases), so steadied falls did worse than falls still accelerating.
- **F2:** The steadied side carries the wrong sign: the 19 long cases (30-day return up) had a mean excess of -6.1 % over the next 30 days (t -2.11), or -9.1 % with t -2.75 when the cases of one day are taken together, but those 14 cases fall on only 5 days. The 70 short cases (still falling) had +4.0 % (t 1.15), a modest rebound rather than continued falling.
- **F3:** The response is not graded either way: by quartile of the 30-day return inside the regime, the excess return is -0.7 %, +7.7 %, +8.4 % and -7.8 % (about 22 cases each). The deepest recent falls and the rising months both earn nothing, and only the middle earns.
- **F4:** The effect is not stable over time: the still-falling cases earned +7.8 % excess up to 2022 (23 cases) and -4.5 % from 2023 (22 cases), and by year the regime's mean excess ranges from -9.1 % (2025) to +19.4 % (2023).
- **F5:** The idea's size cannot be told from zero: the unusual move is +0.89 % per case (t 0.26, 110 days), 0.040 of a usual 29.3 % move. The regime's overall excess is +1.9 % with t 0.38 on 35 days, while the total move in the trade's direction is -1.77 %, against a 0.22 % trade cost.
- **F6:** Outside a deep 90-day fall, the 30-day return leans the other way, toward continuation: across 628 cases the slope of next-30-day excess return on the 30-day return is +0.090 (t 2.38). The bottom quintile (mean 30-day return -24 %) went on to an excess of -8.6 % (t -3.92, 126 cases).

## Ideas
- `031-02.b1.b1.b1.b1_monthly-losers-keep-falling` (from F6, F2): While a coin's 90-day return stands above minus its usual 90-day move, the lower its 30-day return, the further its price falls below its normal drift over the next 30 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
