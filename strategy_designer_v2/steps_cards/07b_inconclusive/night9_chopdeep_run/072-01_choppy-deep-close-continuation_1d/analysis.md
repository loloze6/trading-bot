---
line: 7.b inconclusive
backtest: 072-01_choppy-deep-close-continuation_1d
idea tested: 072-01_choppy-deep-close-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3175 USD
---
## Findings
- **F1:** Step 5's measure is essentially zero: the slope on the standardised forecast is +1.7e-5 with a clustered t of 0.10 on 4219 bars over 1901 days. The size is an unusual move of -0.08 % per case (t -0.61, 991 days), a strength of -0.008. Measured instead on the raw depth in folds B and C, on the 1-day non-overlapping grid, the slope is -9.3 bp per usual-move unit of depth with t -1.42 (1484 cases). So the 60-day standardisation and the 1-day horizon together hide most of what the raw depth carries.
- **F2:** The effect grows with the horizon. On non-overlapping grids in folds B and C, the slope of the coin's return in excess of its drift on the raw depth is:
- **F3:** The effect sits in the deepest closes. Over 1 day, the top depth quintile (mean depth 6.1 usual moves) is followed by -0.67 % in excess of drift (t -1.71), while the other quintiles lie between -0.02 % and -0.18 %. Over 3 days, the top quintile gives -2.60 % (t -3.09, 99 cases), against -0.10 % for the shallowest.
- **F4:** Over 1 day, the effect is uneven across coins and years. BTC has a slope of -18.6 bp (t -2.05) while ZEC is opposite at +21.1 bp (t 0.86). One year carries it (2020: -56.9 bp, t -3.49), with 2018 and 2021 slightly positive (t 0.72 and 0.64). The next-day reading is drowned by the market's own moves (usual 1-day move 4.78 %).
- **F5:** Over 5 days, the slope is negative on every one of the six coins (from -20 bp for LTC to -236 bp for XRP). It is negative on both up-close days (-177 bp, t -3.22, 139 cases) and down-close days (-22 bp, t -0.58, 148 cases). Down-close days still show a mean excess return of -2.55 %. So the multi-day effect is not confined to one kind of day, though it is graded more clearly after up days.
- **F6:** Over 5 days, the mean move in excess of drift across in-profile cases is -1.52 %. That is about eight times the 0.19 % a trade cost, whereas over 1 day the total move (-0.20 %) only equals that cost.

## Ideas
- `072-01.b1_choppy-deep-close-five-day` (from F1, F2, F3, F5, F6): In a choppy market, the further a coin's close sits below its 20-day high, measured in units of the standard deviation of its daily returns over the last 20 days, the larger its fall over the next five days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
