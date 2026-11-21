---
line: 7.g patterns
backtest: 021-01_above-rising-cloud-continues-up.d2_distance-from-cloud-grades_1d
idea tested: 021-01_above-rising-cloud-continues-up.d2_distance-from-cloud-grades
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5402 USD
---
## Findings
- **F1:** A coin's Saturday daily return, minus its own mean daily return, rises with its 26-day return up to Friday's close: slope 0.021 per unit of 26-day return, t 7.0, on 1949 Saturdays across the six coins. This is the strongest pattern among the roughly 40 angles examined, so it stands out after allowing for how many were looked at.
- **F2:** Saturday is the best day of the week. The mean raw daily return is +0.45 % (t 5.5, 2484 days), against -0.18 % to +0.33 % on the other days. Saturday's excess return over each coin's mean is positive on all 6 coins (t 0.35 for BTC up to 2.58 for LTC) and in 6 of 8 years. The effect is smaller but still positive in the later half of the windows: +0.18 % in w13 to w24 against +0.36 % in w1 to w12.
- **F3:** Saturday is also the quietest day. Its mean absolute return is 2.46 %, against 3.26 % to 3.71 % from Monday to Friday. The Saturday excess of 0.2 % to 0.5 % is about one to two and a half times the 0.19 % round-trip cost this backtest applied, though the per-coin cost runs from about 0.10 % for BTC to 0.31 % for XMR (F1 of the earlier runs).
- **F4:** The 26-day return predicts the next 7 days only in calm conditions, so this is momentum inside a volatility regime:
- **F5:** The tested cloud-distance forecast is weak at its own 26-day horizon (t 1.58, 576 cases) and is no stronger than plain 26-day momentum (t 2.51, 432 cases). That momentum is itself unstable: t -0.56 in w1 to w12 and t 4.41 in w13 to w24. By coin, the cloud forecast's t runs from -0.98 for XRP to 2.01 for BTC.
- **F6:** The book lost through its shorts. Its 1953 short trades averaged -8.7 % after fees (median -6.6 %), against +14.9 % (median -1.2 %) on its 1017 longs. It lost in the bull years (mean daily book return -10.1 bps in 2020 and -9.6 bps in 2023, while the coins gained 42.3 and 15.0 bps). It earned 8.8 bps in 2018, when the coins fell 34.7 bps a day.

## Ideas
- `021-01_above-rising-cloud-continues-up.d2_distance-from-cloud-grades.g1_saturday-continuation-of-monthly-trend` (from F1, F2, F3): A coin's return on Saturday, from Friday's daily close to Saturday's, is larger the larger the coin's 26-day return at Friday's close.
- `021-01_above-rising-cloud-continues-up.d2_distance-from-cloud-grades.g2_calm-market-momentum-over-a-week` (from F4, F5): When a coin's 14-day volatility is low compared with its own past, its return over the next 7 days is larger the larger its 26-day return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
