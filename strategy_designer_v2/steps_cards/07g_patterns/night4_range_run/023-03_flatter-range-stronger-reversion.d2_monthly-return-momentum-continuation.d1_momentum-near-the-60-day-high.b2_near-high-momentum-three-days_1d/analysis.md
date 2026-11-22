---
line: 7.g patterns
backtest: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.b2_near-high-momentum-three-days_1d
idea tested: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.b2_near-high-momentum-three-days
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3888 USD
---
## Findings
- **F1:** Over the next 3 days a coin follows its own past 3 days only when it has been calm. On non-overlapping 3-day cases, regressing the standardised excess return on the 3-day return scaled by the 20-day daily volatility gives slope 0.067 with t 3.70 (n 1716) in each coin's lowest-volatility tercile, against t 0.80 and 0.84 in the middle and highest terciles (n 1715 and 1716).
- **F2:** Inside the calm tercile the continuation is graded. The mean excess 3-day return rises from −0.73 % (t −2.18, n 348) in the most-down quintile of the scaled 3-day return to +0.74 % (t 1.99, n 342) in the most-up quintile.
- **F3:** The calm-tercile continuation holds in both halves of the record and in most coins, so it is not one period. The slope's t is 2.35 in w1–w12 (n 983) and 2.86 in w13–w24 (n 733); by coin it is 3.57 for ETH, 2.16 for XRP, 1.78 for BTC, 0.92 for ZEC and 0.78 for LTC, and −0.37 for XMR (n 286 each).
- **F4:** The same grading shows when calm is measured against the coin's own recent history. With 20-day volatility divided by its 120-day median, the slope on the scaled 3-day return is t 2.26 in the lowest tercile, 0.76 in the middle and −0.33 in the highest (n about 1091 each). The 20-day mean deviation in volatility units gives t 3.09 in the calm tercile and 0.83 and 1.44 in the others.
- **F5:** The book's gain comes from its longs alone. The position's gain on long bars sums to +13.31 (mean +0.129 % a bar, 10343 bars) and on short bars to −0.34 (mean −0.007 %, 5086 bars). On the 3-day grid, cases short after a falling month earned −0.22 % (n 1260), against +0.67 % for cases long after a rising month (n 2053).
- **F6:** The brief's range reversion does not show in these bars. The slope of the excess return on position in the 30-day range is positive (continuation), not negative. In the flattest third of months it is +0.019 with t 0.22 (n 1428).
- **F7:** The book loses relative to holding when the coins rise hard. Its sums lag holding's in the strong windows (w11 +0.36 against +1.49; w10 +0.16 against +0.48). By year its mean daily return is below holding's in every rising year, for example 2021 at 0.117 % against 0.409 %.
- **F8:** Weekday and the last day's return show nothing that stands apart from noise. The mean excess return by weekday spans −0.40 % to +0.52 % on about 820 cases each, and no quintile of the 1-day return reaches |t| 1.

## Ideas
- `023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.b2_near-high-momentum-three-days.g1_calm-market-short-term-continuation` (from F1, F2, F3, F4): The larger a coin's 3-day return measured in units of its own daily volatility over the past 20 days, the larger its move in the same direction over the next 3 days, and the more so the calmer its past 20 days have been.
- `023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.b2_near-high-momentum-three-days.g2_quiet-stretch-keeps-going` (from F1, F4, F6): The calmer a coin's past 20 days relative to its own past 4 months, the larger its move over the next 3 days in the direction of its distance from its 20-day mean, measured in units of its daily volatility.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
