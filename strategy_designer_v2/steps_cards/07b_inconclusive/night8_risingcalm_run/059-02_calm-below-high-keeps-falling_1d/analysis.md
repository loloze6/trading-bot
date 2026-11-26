---
line: 7.b inconclusive
backtest: 059-02_calm-below-high-keeps-falling_1d
idea tested: 059-02_calm-below-high-keeps-falling
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3393 USD
---
## Findings
- **F1:** The test's main measure is on the predicted side over all folds (slope 0.000938, t 2.86, 1550 non-zero in-profile cases) but points the other way on check folds A and D (−0.000364), and the size is nil: the unusual move is +0.04 % per case (t 0.12, 813 days), 0.004 of a usual 10.60 % move. The result is therefore mixed across periods rather than too small, and all four folds are already used.
- **F2:** On the explored folds B and C the effect is clear over 3 to 10 days on calm bars. The forecast slope t is 3.65, 4.56 and 3.35 at 3, 5 and 10 days, and the recomputed raw depth slope t is 4.06, 5.87 and 4.24. It vanishes at 20 days (t 0.00).
- **F3:** The effect is graded but sits in the deep declines only (5-day excess return by raw depth in 30-day swings). Depth below −6 gives −4.94 % (28 cases), −6 to −4 gives −2.07 % (72), and −4 to −2.5 gives −2.72 % (103). Shallow depths of −1.5 to −0.5 give +1.69 % (192), so the mild cases rebound and cancel the short-side mean.
- **F4:** Part of the slope comes from bars at a new 14-day high, where the forecast is 0. These rise +3.22 % beyond drift over 5 days (132 cases), against −0.38 % for non-zero forecasts (774), Welch t 2.93. Among non-zero forecasts only, the 5-day slope falls to t 3.31.
- **F5:** Among non-zero forecasts the effect lives in a falling trend. The 5-day slope t is 3.17 there (203 cases, mean excess −1.76 %), against 1.24 in choppy (88, −1.16 %) and 1.46 in rising (140, +0.59 %). Calm declines inside a rising trend are bought rather than extended, which fits the check folds' rising years reversing the sign.
- **F6:** The effect is spread across coins and years, not carried by one of them. The 5-day non-zero slope is positive for all six coins (t 0.63 for ZEC to 1.91 for LTC) and in all four years 2018 to 2021 (t 1.13 to 2.24).
- **F7:** Outside the calm profile the past-14-day return predicts nothing at 5 days (slope t −0.79, against 3.99 on calm bars), so the calm condition itself is supported.

## Ideas
- `059-02.b1_falling-calm-declines-extend` (from F1, F3, F5, F6, F7): In a falling, calm market, the further a coin's close sits below its highest close of the past 14 days, measured in units of its own 30-day daily swing, the larger its fall over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
