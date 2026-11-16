---
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.b2_large-rise-continues-five-days_1d
idea tested: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.b2_large-rise-continues-five-days
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.4969 USD
---
## Findings
- **F1:** Large down days are followed by a next-day rebound. Among down days, the slope of next-day excess return on the 20-day-volatility-scaled one-day move is -0.00391 (t=-4.55, n=7529), so bigger falls see bigger rebounds. Days scaled below -2 earn +0.74% next day (t=2.32, n=425), and days between -2 and -1 earn +0.55% (t=4.06, n=1511). The slope is negative in all six coins (XMR t=-3.85, XRP t=-2.33, ZEC t=-2.00). By year it is strong in 2018, 2020 and 2021 (t=-2.04, -4.30, -4.03) but near zero in 2022 and 2024.
- **F2:** Coins rise more on Fridays and Saturdays. The mean daily coin return is +0.33% on Fridays (t=3.51) and +0.45% on Saturdays (t=5.53), against -0.12% on Tuesdays and -0.18% on Thursdays. Fri+Sat minus other days gives Welch t=4.95. Fri+Sat beats the other days in 63.2% of coin-windows (t=5.31, n=144). Every coin's Fri+Sat mean is positive (t 1.87 to 3.76), and 7 of 8 years are positive.
- **F3:** The continuation the idea found shows up on days 2 to 5, not on day 1. After up days, the next-day excess slope on the scaled move is flat (t=1.14, n=7675). Small rises scaled 0 to 0.5 and 0.5 to 1 are followed by negative next-day excess returns (-0.19%, t=-2.34; -0.26%, t=-2.73). Over days 2 to 5 the slope is positive (0.0076, t=2.04, n=1422). Rises scaled 1 to 2 return +1.39% over days 2 to 5, against +0.38% after rises scaled 0 to 0.5.
- **F4:** The book loses on timing. Its mean bar gain is 0.000116, of which 0.000282 is the market's own rise and -0.000168 is timing. Positions of 0.16 and 0.50 are held after small up days, whose next-day returns are -0.08% and -0.16%. After down days the position is about 0, although the next day returns +0.69% after days scaled below -1.
- **F5:** The 20-day vol-scaled return predicts 5-day excess return when pooled (slope t=2.45, n=2843), but almost all of it comes from XRP (t=3.09). The other coins sit between -0.24 and 1.08, so this is not a pattern of single coins.

## Ideas
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.b2_large-rise-continues-five-days.g1_large-fall-next-day-rebound` (from F1, F4): The larger a coin's one-day fall relative to the standard deviation of its daily returns over the past 20 days, the larger its rise over the next 1 day.
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.b2_large-rise-continues-five-days.g2_delayed-continuation-after-rises` (from F3, F4): The larger a coin's one-day rise relative to the standard deviation of its daily returns over the past 20 days, the larger its rise from one day after that rise to five days after it.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
