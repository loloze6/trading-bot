---
line: 7.b inconclusive
backtest: 033-01_range-position-drift-follows_1d
idea tested: 033-01_range-position-drift-follows
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3440 USD
---
## Findings
- **F1:** In folds B and C the tested measure is clearly on the idea's side: the slope of the drift-removed 5-day return on the forecast is +0.00120 with t 4.52 over 1,710 grid cases, and the signed unusual move is +1.24 % per case with a day-clustered t of 2.40 over 305 days. The inconclusive verdict therefore comes from folds A and D, where the main measure is -0.00015, against +0.00053 over all folds (t 3.17, 3,419 cases).
- **F2:** The effect is graded through the range in folds B and C. The drift-removed 5-day return rises from -1.75 % (t -2.37) in the bottom fifth of the forecast to -1.04 %, -0.39 %, +1.28 % and +1.89 % (t 2.58) in the top fifth, with 342 cases per fifth. It holds on both sides: long +1.31 % (t 2.94, 812 cases) and short +1.18 % (t 2.91, 898 cases).
- **F3:** The effect is strongest when the close is at the 20-day high. Those 172 cases are followed by +3.28 % beyond drift (t 2.72), against +0.75 % to +0.81 % in the two bins just below it and -0.90 % (t -0.87, 183 cases) at the 20-day low.
- **F4:** Much of the slope comes from whole windows that trend, not from the bar-by-bar position. Across the 72 coin-windows, the window's mean 5-day return regresses on its mean forecast with t 11.3. Measured against each window's own mean return instead of the coin's all-window drift, the slope falls to +0.00057 (t 2.19), and on the raw range position to +0.00038 (t 1.82). The effect is therefore exposed to which way the market trended in a given set of years, which is consistent with it flipping on folds A and D.
- **F5:** The effect varies by period. Window slopes run from t -1.37 (w7) to t +2.81 (w15, w16), with 4 of 12 windows negative. By year, 2018 is flat (t 0.14) while 2019 (t 3.58) and 2020 (t 2.51) carry it, so the part of the data step 7 sees has a mixed stretch of its own.
- **F6:** The plan's 5-day horizon is where the effect peaks. The slope's t is 3.71, 4.15, 4.52 and 4.52 at 1, 2, 3 and 5 days, falls to 2.02 at 10 days, and turns negative at 20 days (t -0.58). The strength per usual move is also highest at 5 days (0.0097), so the test did not miss the effect by measuring at the wrong horizon.
- **F7:** The effect does not depend on the 60-day trend profile. The slope is positive with t of about 3.6 to 3.9 in falling (401 cases), choppy (127) and rising (318) markets, so no profile is singled out. Per case, the move covers a trade's cost: the total move is +0.52 %, 2.7 times the 0.19 % cost.

## Ideas
- `033-01.b1_range-position-more-coins` (from F1, F2, F4, F5, F6): The higher a coin's daily close sits within its own 20-day high-to-low range, the more the coin rises over the next 5 days. A close at the top of the range is followed by the largest rise, and a close at the bottom by the largest fall.
- `033-01.b2_beyond-range-close-drift` (from F2, F3, F6): The higher a coin's daily close sits against its high-to-low range of the 20 days before it, the more the coin rises over the next 5 days. A close above the top of that range is followed by the largest rise, and a close below its bottom by the largest fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
