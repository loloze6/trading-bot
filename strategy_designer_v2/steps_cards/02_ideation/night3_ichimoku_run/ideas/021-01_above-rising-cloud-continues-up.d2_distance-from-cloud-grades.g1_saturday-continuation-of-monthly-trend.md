---
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
source-idea: 021-01_above-rising-cloud-continues-up.d2_distance-from-cloud-grades
line: 7.g patterns
backtest: 021-01_above-rising-cloud-continues-up.d2_distance-from-cloud-grades_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's return on Saturday, from Friday's daily close to Saturday's, is larger the larger the coin's 26-day return at Friday's close.
Consequence: A trader would lean long into Saturday in proportion to a coin's 26-day rise, and lean away from coins that have fallen over the past 26 days.
Why:
- F1: A coin's Saturday daily return, minus its own mean daily return, rises with its 26-day return up to Friday's close: slope 0.021 per unit of 26-day return, t 7.0, on 1949 Saturdays across the six coins. This is the strongest pattern among the roughly 40 angles examined, so it stands out after allowing for how many were looked at.
- F2: Saturday is the best day of the week. The mean raw daily return is +0.45 % (t 5.5, 2484 days), against -0.18 % to +0.33 % on the other days. Saturday's excess return over each coin's mean is positive on all 6 coins (t 0.35 for BTC up to 2.58 for LTC) and in 6 of 8 years. The effect is smaller but still positive in the later half of the windows: +0.18 % in w13 to w24 against +0.36 % in w1 to w12.
- F3: Saturday is also the quietest day. Its mean absolute return is 2.46 %, against 3.26 % to 3.71 % from Monday to Friday. The Saturday excess of 0.2 % to 0.5 % is about one to two and a half times the 0.19 % round-trip cost this backtest applied, though the per-coin cost runs from about 0.10 % for BTC to 0.31 % for XMR (F1 of the earlier runs).
