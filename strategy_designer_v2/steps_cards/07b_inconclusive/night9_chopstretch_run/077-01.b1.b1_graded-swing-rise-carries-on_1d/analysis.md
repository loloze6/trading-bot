---
line: 7.b inconclusive
backtest: 077-01.b1.b1_graded-swing-rise-carries-on_1d
idea tested: 077-01.b1.b1_graded-swing-rise-carries-on
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3748 USD
---
## Findings
- **F1:** Step 5's main measure is positive but short of the bar: the slope of the 7-day unusual return on the forecast is +0.00107 with t 1.00, over 409 long cases on 157 days. The idea's size over all folds is +0.05 % per case (t 0.09, 473 days), only 0.2 times the 0.22 % cost of a trade. The test already used all 19 coins and all four folds, so there is no more daily data to add.
- **F2:** In the explored folds B and C the carry sits only in the largest swing-scaled rises. In the top forecast quartile (mean forecast 18.2, raw 1.47 swing units) the unusual 7-day move is +6.4 %, against −0.4 % in the third quartile (forecast 5.9) and −1.9 % in the two lower quartiles. On raw quintiles the top one (1.65 units) gives +7.6 % with 69 % of cases up, while the middle quintiles (0.09 and 0.52 units) give only +0.9 %. Moves of ordinary size carry nothing, as the brief says, and a linear long size spread over every rise dilutes the effect.
- **F3:** Taken in both directions, the large moves carry with a t near 2. Among in-profile 7-day cases whose swing-scaled move is in the upper half by size, the unusual move signed in the move's direction is +4.8 % (strength 0.28, t 2.05 on 40 days, 71 cases), against +2.9 % (t 2.09, 61 days) for all signed cases. The falling side carries too: the bottom quintile (−0.78 units) gives −3.2 % with 21 % of cases up.
- **F4:** On raw values the in-profile slope at 7 days is +0.050 (t 3.48, 143 cases), and outside the profile it is only +0.013 (t 1.31, 838 cases). At 3 days the in-profile slope is +0.007 (t 1.28) and at 14 days +0.059 (t 2.30, 66 cases). The plan's horizon and profile are where the effect is strongest.
- **F5:** The effect is uneven over time even in B and C. The yearly slope is −0.018 (t −0.51) in 2018, −0.020 (t −1.47) in 2019, +0.033 (t 2.27) in 2020 and +0.065 (t 4.53) in 2021. By coin, ETH (t 3.08) and XRP (t 2.53) carry it, while BTC (t 0.49) and XMR (t 0.59) do not. This mixing is why the result over all folds is unclear.

## Ideas
- `077-01.b1.b1.b1_extreme-swing-scaled-moves-carry` (from F2, F3, F4, F5): In a choppy, calm market, a coin whose 14-day return is large against its own daily swing over the past 30 days keeps moving the same way over the next 7 days. The carry grows faster than the swing-scaled move itself, so that ordinary moves carry almost nothing and the largest carry most.
- `077-01.b1.b1.b2_largest-swing-scaled-rises-carry` (from F1, F2, F4): In a choppy, calm market, a coin whose 14-day rise is large against its own daily swing over the past 30 days keeps rising over the next 7 days. The further rise grows faster than the swing-scaled rise, so that the largest rises carry most and ordinary ones almost nothing.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
