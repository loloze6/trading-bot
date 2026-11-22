---
line: 7.g patterns
backtest: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e1_choppy-declines-keep-falling_1d
idea tested: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e1_choppy-declines-keep-falling
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.5322 USD
---
## Findings
- **F1:** Measured over all coins on the 5-day grid, the 30-day net move divided by the 30-day high-low range, kept with its sign, grades the next 5 days' unusual move in the trend's direction (slope of strength on the signed ratio 0.113, t 4.35, 5434 cases); on rising coins alone the slope is 0.227 (t 2.95, 2723 cases).
- **F2:** The cleanest rises keep rising, by much more than a trade costs. The three top deciles of the signed ratio (0.375 to 0.99) are followed by unusual moves of +1.28 % (t 2.56), +1.86 % (t 2.08) and +1.09 % (t 1.76) over 5 days, with total moves of +2.06 %, +2.68 % and +1.89 %. That is 9 to 12 times the 0.22 % cost, against a total of +0.13 % for the tested short cases.
- **F3:** The effect is larger over 10 days. On the 10-day grid the top quintile of the signed ratio (0.54 to 0.98) is followed by an unusual move of +3.13 % (t 3.00, 536 cases, strength 0.173) and a total move of +4.49 %; the quintile from 0.19 to 0.54 shows +0.80 % (t 1.07).
- **F4:** The clean-rise continuation (ratio above 0.4) holds in most coins and most years, but not all. Its mean unusual move is positive in 17 of 19 coins (median +1.12 %). By year it is positive in 2020 (+2.70 %, t 3.29), 2021 (+5.42 %, t 2.52), 2023 (+1.47 %, t 2.43) and 2024 (+1.85 %, t 2.71), and negative in 2018 (−11.95 %, 13 cases) and 2022 (−3.27 %, t −2.94).
- **F5:** The tested short side only works in the middle of the falls. Choppy falls (signed ratio −0.35 to 0) are followed by −1.84 % (t −4.25) and −1.16 % (t −2.58) over 5 days. The cleanest falls (ratio below −0.656) are followed by +0.13 % (t 0.25), so steep, clean declines stop continuing.
- **F6:** The book does not capture any of this. Its mean daily return is −0.0000596. The position's mean gain per bar is −0.0000531, made of −0.000108 lost by being short a coin that rises on average and only +0.000055 of timing. Every trade is a short (3225 trades, mean net −2.10 %, median −1.12 %), and trades held 20 to 60 days lose −7.22 % net on average (438 trades).
- **F7:** Other angles did not give a pattern I could tell from chance across this many cuts, nor one stable by year: weekday (alternating signs, t up to 4.3, but the 19 coins share the same days), the previous day's return (+0.91 % after the lowest quintile, t 2.82), relative volatility (+0.83 % in the top quintile, t 2.23), and the 5-day past return (no cell above |t| 1.6). The high-volatility and big-down-day cells change sign between years.

## Ideas
- `023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e1_choppy-declines-keep-falling.g1_clean-rises-keep-rising` (from F1, F2, F3, F4, F6): In a coin that has risen over the past 30 days, the larger its 30-day net rise is against its 30-day high-low range (the cleaner the rise), the further it keeps rising, beyond its normal drift, over the next 10 days.
- `023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e1_choppy-declines-keep-falling.g2_clean-falls-stop-falling` (from F5, F1): In a coin that has fallen over the past 30 days, the larger its 30-day net fall is against its 30-day high-low range (the steeper and cleaner the fall), the more it rises back, relative to its normal drift, over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
