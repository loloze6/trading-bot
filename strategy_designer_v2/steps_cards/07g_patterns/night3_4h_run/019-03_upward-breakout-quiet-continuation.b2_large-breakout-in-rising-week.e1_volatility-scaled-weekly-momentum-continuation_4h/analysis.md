---
line: 7.g patterns
backtest: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e1_volatility-scaled-weekly-momentum-continuation_4h
idea tested: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e1_volatility-scaled-weekly-momentum-continuation
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4316 USD
---
## Findings
- **F1:** The vol-scaled 7-day momentum grows larger at longer horizons, enough to cover the cost of a trade. Over 18 bars (3 days) the unusual move is +0.28 % per case (strength 0.030, t 3.3, 5724 cases), which is about 1.5 times the 0.19 % round trip. Over 72 bars (12 days) it is +0.88 to +0.93 % (strength 0.043 to 0.045, t 3.2 to 3.5, 1260 to 1404 cases), about 4.6 times the cost. Over 108 bars (18 days) it is +1.50 % (strength 0.050, t 2.4 to 2.8, 720 cases), about 8 times the cost.
- **F2:** At the 12-day horizon both ends of the forecast carry the effect. The lowest forecast quintile is followed by -3.05 % excess (t -3.6, 281 cases) and the highest by +3.11 % (t 2.5, 281 cases). On the raw vol-scaled 7-day return the extremes are -1.86 % (t -2.0) and +2.99 % (t 2.5, 252 cases each). The three middle quintiles show no order (-1.9 % to +1.0 %).
- **F3:** At the tested 3-day horizon the effect sits mostly in the weakest weeks. The lowest forecast quintile is followed by -0.74 % (t -3.1, 1145 cases). The highest is only +0.35 % (t 1.2), and the fourth +0.43 % (t 1.6).
- **F4:** The 3-day momentum fades over time. Its directional strength is 0.083 in 2018 and 0.089 in 2019 (t 1.7 and 2.4, about 678 cases each), but 0.004 to 0.034 in every year from 2020 to 2025 (all t below 0.8). At 12 days it is negative in 2022 (-0.18, t -2.5, 156 cases).
- **F5:** The brief's premise is not seen here. The quietest fifth of 30-bar ranges, relative to their 180-bar average, is followed by an absolute 3-day move of 0.68 usual moves. The widest-range fifth is followed by 0.75, and the middle fifths by 0.64 to 0.68. After the quietest fifth, the last bar's direction predicts only +0.056 usual moves (t 1.8, 944 cases).
- **F6:** There is a time-of-day pattern, but it is too small to trade. The 4h bar starting at 16 UTC rises by +0.038 of a bar's usual move (t 5.2, about 17500 bars), positive on all 6 coins (t 1.4 to 2.9). The bar starting at 20 UTC falls by -0.036 (t -4.6), a fall seen in 2018 to 2022 (t -2.0 to -5.4) and absent from 2023 on. At about 0.04 of a roughly 2 % bar move, this is under 10 bps, below the 19 bps round trip.
- **F7:** There is a weekday pattern in excess daily returns, but it is not stable. Saturday is +0.34 % (t 4.1, 2484 cases) and Friday +0.21 % (t 2.2). Friday is positive in 2019, 2020 and 2023 and negative in 2022 (t -2.2), and it stands out on LTC alone (t 2.2). Among the roughly 20 angles examined, this one does not hold up across years.
- **F8:** The book beats holding only in falling years. It earned +0.05 % a day in 2018 while the coins lost 0.35 %, and +0.08 % in 2022 against -0.18 %. In the rising years 2020, 2021 and 2023 to 2025 it lagged the coins by 0.2 to 0.35 % a day. It lost money on XMR (-0.04 % a day while XMR rose 0.11 %).

## Ideas
- `019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e1_volatility-scaled-weekly-momentum-continuation.g1_vol-scaled-momentum-twelve-day-hold` (from F1, F2, F4): The larger a coin's 7-day return, measured in units of its own 4h volatility, the more the coin rises over the next twelve days.
- `019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e1_volatility-scaled-weekly-momentum-continuation.g2_weak-week-downside-continuation` (from F3, F2, F8): The more negative a coin's 7-day return, measured in units of its own 4h volatility, the more the coin falls over the next three days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
