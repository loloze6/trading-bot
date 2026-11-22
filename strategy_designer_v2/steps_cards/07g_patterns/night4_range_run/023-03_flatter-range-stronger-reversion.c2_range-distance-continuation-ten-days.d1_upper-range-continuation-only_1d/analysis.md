---
line: 7.g patterns
backtest: 023-03_flatter-range-stronger-reversion.c2_range-distance-continuation-ten-days.d1_upper-range-continuation-only_1d
idea tested: 023-03_flatter-range-stronger-reversion.c2_range-distance-continuation-ten-days.d1_upper-range-continuation-only
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3957 USD
---
## Findings
- **F1:** The next day's excess return rises the larger the day's fall measured in the coin's own 30-day daily volatility: on down days the slope of next-day excess return on the vol-scaled move is -0.00415 with t -6.0 (6332 days), and the bucket means grow with the fall, +0.08 % (t 1.1, 4755) for falls under 1, +0.29 % (t 1.6, 753) for 1 to 1.5, +0.70 % (t 2.5, 383) for 1.5 to 2, +0.54 % (t 1.9, 316) for 2 to 3 and +1.60 % (t 2.4, 137) beyond 3 volatilities.
- **F2:** The rebound has no mirror on up days, where the slope is -0.00022 with t -0.34 (6572 days), and up days beyond 3 volatilities are followed by -0.24 % (t -0.40, 143).
- **F3:** The rebound after a fall beyond 1.5 volatilities is positive in all 6 coins (XMR +1.53 % t 3.8, XRP +1.46 % t 2.5, LTC +0.65 %, ZEC +0.61 %, ETH +0.24 %, BTC +0.18 %) and in all 8 years (2020 +2.10 % t 2.9, 2025 lowest at +0.15 %), and it lasts beyond one day, with +0.86 % excess over the next 3 days (t 2.9, 826 cases, not fully independent).
- **F4:** The tested idea's gain sits in only part of the book: forecast>0 grid cases beat forecast-0 cases by 3.4 points in ETH, 2.0 in XRP and 4.0 in ZEC but by about 0 in LTC (-0.09 % vs +0.08 %) and XMR (-0.01 % vs +0.01 %), and the book's best 2 % of days carry 141 % of its mean daily gain.
- **F5:** Within the upper range, the response is not graded. Only the close at the 30-day closing high stands out, with +4.69 % excess over 10 days (t 2.3, 137 cases). Even that rests mainly on XRP (+22.9 %, 18 cases), while the 0.7 to 0.9 band of the range is followed by -1.75 % (t -2.1, 210).
- **F6:** The next-day excess return depends on the weekday of the close. Thursday closes are followed by +0.26 % (t 2.7) and Friday closes by +0.30 % (t 3.7), positive in all 6 coins and in 6 of 8 years. Monday closes are followed by -0.27 % (t -2.7) and Wednesday closes by -0.29 % (t -2.6), about 2460 days each.

## Ideas
- `023-03_flatter-range-stronger-reversion.c2_range-distance-continuation-ten-days.d1_upper-range-continuation-only.g1_rebound-after-outsized-daily-falls` (from F1, F2, F3): The larger a coin's one-day fall, measured against its own daily volatility over the past 30 days, the more the coin rises back over the next 1 to 3 days.
- `023-03_flatter-range-stronger-reversion.c2_range-distance-continuation-ten-days.d1_upper-range-continuation-only.g2_new-monthly-high-continuation` (from F5, F4): The closer a coin's daily close comes to a new 30-day closing high, measured by how many of the past 30 days' closes it exceeds, the more the coin rises over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
