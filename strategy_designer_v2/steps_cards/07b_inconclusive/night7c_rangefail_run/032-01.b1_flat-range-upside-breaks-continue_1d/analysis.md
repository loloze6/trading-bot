---
line: 7.b inconclusive
backtest: 032-01.b1_flat-range-upside-breaks-continue_1d
idea tested: 032-01.b1_flat-range-upside-breaks-continue
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3291 USD
---
## Findings
- **F1:** The tested result is on the predicted side but short of the bar: the mean unusual 20-day move is +6.77 % with t 1.57 over 113 cases on 101 days. In the folds shown (B, C) it is +4.0 %, t 1.13, over 61 cases on 52 days, so the cases are too few for a move of this size, whose spread is about 21 % of price over 20 days.
- **F2:** The move shows mostly in the first days after the break rather than at the plan's 20-day horizon. In folds B and C the mean unusual move is +2.3 % at 3 days (t 1.69, 96 cases), +4.9 % at 5 days (t 2.53, 87 cases on 73 days), +4.0 % at 10 days (t 1.49) and +4.0 % at 20 days (t 1.13). At 40 days it fades to +0.6 % (t 0.10).
- **F3:** The grading the idea names, a narrower 60-day range giving a larger rise, is present when range width is measured directly as the 60-day high over the 60-day low. Breaks from ranges narrower than the median gain +16.3 % at 20 days (t 2.83, 24 cases), while wider ranges give −3.1 % (t −0.93, 24 cases); the correlation of range width with the 20-day move is −0.28.
- **F4:** At 5 days the same grading runs step by step across range-width quartiles: +9.4 %, +8.8 %, +4.0 % and −0.1 % from narrowest to widest (about 18 cases each). Narrower-than-median ranges give +9.1 % (t 2.74, 36 cases), wider ones +1.9 % (t 0.84).
- **F5:** The plan's forecast, the break divided by the range's mean depth below its high, does not carry this grading. Its correlation with the 20-day move is −0.01, and the forecast's quartiles at 20 days run +8.5 %, −3.2 %, +8.9 % and +2.2 % with no order. So the supporting check passed only narrowly (+0.68 %), and the size of the forecast does not track the size of the move.
- **F6:** The effect is uneven across coins and years, which adds to its variance. At 20 days XRP gives +22.5 % (7 cases) and ETH and ZEC about +5 %, while LTC (−2.4 %) and XMR (−1.2 %) give nothing. 2020 gives +16.7 % (t 2.75, 23 cases) and 2021 gives −7.7 % (t −1.55, 23 cases).

## Ideas
- `032-01.b1.b1_flat-range-breaks-more-coins` (from F1, F6): In a coin whose price has gone nowhere over the past 60 days, a daily close above the prior 60-day high is followed by a further rise over the next 20 days. The narrower and flatter the 60-day range it broke out of, the larger that rise.
- `032-01.b1.b2_tight-range-breaks-rise-fast` (from F2, F3, F4, F5): In a coin whose price has gone nowhere over the past 60 days, a daily close above the prior 60-day high is followed by a further rise over the next 5 days. The narrower its 60-day high-to-low range as a share of price, the larger that rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
