---
line: 7.g patterns
backtest: 031-01.g1.g1.g2.g1_thursday-close-trend-into-weekend_1d
idea tested: 031-01.g1.g1.g2.g1_thursday-close-trend-into-weekend
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4053 USD
---
## Findings
- **F1:** The tested trend grading sits almost entirely on Saturday. On Friday-close bars, a coin's next-day (Saturday) return net of its mean, in units of its usual daily move, rises with its 14-day return scaled by its 20-day volatility: slope 0.132, t 3.29 with cases of one day clustered, 345 days, 2070 cases. This is the largest t among the slopes examined.
- **F2:** Regressing the 2-day return on the standardised 14-day return gives a positive slope only for windows that start on Friday (slope 0.077, t 2.22, 297 days) and on Saturday (0.060, t 2.09). The other five start days give t between 0.02 and 1.35.
- **F3:** Saturday carries most of the book's gain. Its mean daily book return on Saturdays is 0.199 % (n 2484) and on Fridays 0.075 %, while every other weekday lies between -0.038 % and +0.013 %.
- **F4:** Weekend days rise more than usual. A coin's return net of its mean is +0.060 usual daily moves on Saturdays (t 3.74, 2479 cases) and +0.051 on Fridays (t 2.61), against -0.066 on Thursdays (t -2.92) and -0.049 on Tuesdays (t -2.48).
- **F5:** The book's long trades gain and its short trades lose. Long trades average +1.86 % net (1613 trades) and short trades -1.25 % net (1649 trades), so the weekend's positive drift (F4) works against the trades taken after a 14-day fall.
- **F6:** The Saturday drift is not stable across years. The mean Saturday excess return is -0.005, -0.015 and -0.021 usual moves in 2018, 2022 and 2023, and +0.08 to +0.13 in the other five years. The book's mean daily return is negative in 2022 (-0.022 %) and 2025 (-0.067 %), which fits its failed Calmar (0.48).
- **F7:** Large one-day falls show only a weak next-day reversal, which does not stand out given the number of angles examined. In the most volatile third of days the slope of the next day's return on the size of the fall is -0.217 (t -2.16, 959 days). Over all days it is -0.063 (t -1.43, 1835 days). Up days show no grading (t 0.52).
- **F8:** Neither position in the 60-day range nor a new 60-day low grades the next 5 days clearly. The highest range quintile gives +0.075 usual moves (t 1.63) and the lowest -0.042 (t -0.91). New lows give +0.086 (t 0.74, 126 cases). These show no clear capitulation or bounce near lows on this data.

## Ideas
- `031-01.g1.g1.g2.g1.g1_saturday-carries-two-week-trend` (from F1, F2, F3): A coin's 14-day return, scaled by its recent daily volatility, at Friday's close (UTC) grades its move over the following Saturday: the larger its two-week rise relative to its volatility, the larger its Saturday gain; and the larger its two-week fall, the weaker its Saturday.
- `031-01.g1.g1.g2.g1.g2_weekend-trend-long-side-only` (from F4, F5, F2): The larger a coin's 14-day rise at Thursday's close (UTC), scaled by its recent daily volatility, the larger its gain over the following Friday and Saturday, while a 14-day fall of any size is followed by a Friday-and-Saturday move no weaker than the coin's usual one.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
