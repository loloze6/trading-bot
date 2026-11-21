---
line: 7.g patterns
backtest: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation_1h
idea tested: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4321 USD
---
## Findings
- **F1:** Over a coin's past 7 days, the larger its return, the larger its unusual move over the next 2 weeks. Pooled slope of 2-week excess return on 7-day return is 0.179 (t 3.71, 1004 independent cells). For the 7-day move in units of usual volatility the slope is 0.023 (t 3.58). Over the next 7 days the slope is 0.087 (t 2.83). The slope is positive on all 6 coins (0.04 to 0.29) but strong only on ZEC (t 2.20), and in years it is positive in 5 of 8 (t 2.01 in 2020, 2.65 in 2025) and negative in 2021 to 2023.
- **F2:** Sorted into quintiles per coin, the 7-day return separates the next 2 weeks much more than the tested 30-day return does. By 7-day quintile, the 2-week excess runs from −3.17 % (t −2.87, 203 cells) at the bottom to +5.29 % (t 2.14, 203 cells) at the top, a total move of +6.87 % against a cost of 0.19 %. By 30-day quintile, no quintile's excess goes past ±1.6 % (all |t| ≤ 1.13). The 30-day slope over 2 weeks is weaker than the 7-day one (14-day return slope t 1.64).
- **F3:** The larger a coin's 1-day fall against its usual 1-day move, the larger its rebound over the next 1 to 7 days. Over the next 24 hours the slope is +0.89 % excess per unit of fall (t 6.54, 1969 independent cases); over 3 days it is +0.85 % (t 3.66); over 7 days, +0.94 % (t 2.59). Falls beyond 2 usual moves gain +2.06 % excess over 3 days (t 2.90, 122 cases), and falls of 1 to 2 usual moves gain +1.02 % (t 2.30, 375 cases).
- **F4:** The rebound after falls of more than one usual move is positive over 3 days on all 6 coins, from +0.07 % on XMR to +2.97 % on XRP. Its total move is +1.78 %, about 9 times the 0.19 % cost of a trade. It is not steady across years: −1.39 % in 2018 and about zero in 2022 to 2024, against +4.4 % and +7.1 % in 2020 and 2021.
- **F5:** The tested forecast is almost always saturated, so it barely grades. Of 568 positive grid cells, 502 have a forecast above 2.5. Their 2-week excess is +1.38 % (t 1.28). Trades entered in the top forecast quartile have a median net gain of +3.6 %, against −0.55 % in the bottom quartile, but their means are equal (12.7 % each).
- **F6:** Hour-of-day effects stand out statistically but are far below the cost of a trade. Excess hourly returns at 20 and 21 UTC are +4.8 and +3.7 bps (t 5.98 and 4.85), and at 13 UTC −4.2 bps (t −4.46). Each is under a quarter of the 19 bps round trip.
- **F7:** Thursday's daily excess return is negative on all 6 coins, from −14 to −40 bps, but it is unstable across years. It is positive in 2021 and 2024, and is −156 bps in 2019.
- **F8:** The book's gain comes mostly from losing less than the coin in falling years, not from timing in rising ones. Its daily return is −19.4 bps in 2018 against −34.7 for the coin, and −4.6 against −18.0 in 2022. In 2021 it earns about half the coin's return (20.6 against 40.9 bps).

## Ideas
- `018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.g1_weekly-rise-two-week-continuation` (from F1, F2, F5): A coin's 7-day return predicts its next 2 weeks: the larger the rise over its past 7 days, measured against its usual 7-day move, the further it rises over the next 2 weeks above its usual 2-week drift.
- `018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.g2_daily-plunge-three-day-rebound` (from F3, F4): A coin that has fallen over its past 24 hours rebounds over the next 3 days above its usual 3-day drift, and the larger that fall against its usual 1-day move, the larger the rebound.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
