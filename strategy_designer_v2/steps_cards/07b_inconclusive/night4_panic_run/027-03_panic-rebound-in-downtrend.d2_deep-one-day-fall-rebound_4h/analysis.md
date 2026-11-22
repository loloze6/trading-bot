---
line: 7.b inconclusive
backtest: 027-03_panic-rebound-in-downtrend.d2_deep-one-day-fall-rebound_4h
idea tested: 027-03_panic-rebound-in-downtrend.d2_deep-one-day-fall-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3376 USD
---
## Findings
- **F1:** Over the plan's 14 days the effect is absent rather than weak. On 1152 non-overlapping cases the slope of the excess return on the forecast is negative (t -0.87), and the 578 active cases show no gradient across forecast quartiles: -1.08 %, +0.74 %, -2.79 % and +0.00 % from shallowest to deepest, against +0.79 % for the 574 flat cases.
- **F2:** The same fall depth works at short horizons and fades with time. Its slope t is 7.95 over 1 day (16081 cases), 3.49 over 3 days (5292), 0.67 over 7 days (2154) and -0.17 over 14 days (1008), so the test measured the idea well after its move is spent.
- **F3:** Over 3 days, falls deeper than one usual 24-hour move end +0.96 % above the normal drift (t 3.61, 996 cases), a strength of 0.11 of the usual 3-day move (8.3 %). Their total move of +1.37 % is about 7 times the 0.19 % cost of a trade, and the unusual move alone about 5 times.
- **F4:** The panic shape, a fall with a wide range, carries the effect. Among falls, the 3-day excess return rises with the 24-hour range against its usual size: -0.69 % (t -2.10) in the narrowest-range quartile and +1.69 % (t 4.55, strength 0.19, 645 cases) in the widest. The range slope on falls has t 3.92 over 3 days and 2.92 over 7 days.
- **F5:** Over 14 days, the active cases are dominated by the market's own moves in some years: -7.6 % (t -3.20) in 2018 and -3.7 % (t -2.48) in 2022, against +5.0 % (t 1.51) in 2020. No coin is significant on its own (t from -1.49 for ETH to 0.45 for LTC).
- **F6:** Over 3 days the fall-depth effect is uneven but mostly positive. The slope t by coin runs from -0.05 for BTC to 2.42 for ZEC, with LTC at 2.25 and XRP at 1.84. By year it is positive in 7 of 8 years, with 2022 at -0.84 and 2025 at 3.89.

## Ideas
- `027-03_panic-rebound-in-downtrend.d2_deep-one-day-fall-rebound.b1_deep-fall-three-day-rebound` (from F1, F2, F3, F6): The deeper a coin's 24-hour fall against its usual 24-hour move, the higher its return above its normal drift over the next 3 days.
- `027-03_panic-rebound-in-downtrend.d2_deep-one-day-fall-rebound.b2_wide-range-fall-short-rebound` (from F2, F4): The wider a coin's 24-hour range against its usual 24-hour range while it fell over those 24 hours, the higher its return above its normal drift over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
