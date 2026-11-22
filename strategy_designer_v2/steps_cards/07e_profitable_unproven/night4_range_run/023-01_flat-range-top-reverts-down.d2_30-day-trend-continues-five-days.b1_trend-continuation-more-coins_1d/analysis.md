---
line: 7.e profitable but not proven
backtest: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins_1d
idea tested: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4773 USD
---
## Findings
- **F1:** The book's whole gain comes from its long bars: summed bar gains are 31.15 on 11,162 long bars against -0.001 on 11,722 short bars, and closed trades give +34,583 % long against -6,140 % short; on the short side, a timing gain of +9.18 is cancelled by -9.18 from shorting a rising market.
- **F2:** The market's own rise explains only 9.2 % of the summed bar gain (timing 90.8 %), but the book earns only when coins rise: its mean daily return is +0.17 % and +0.23 % on the two highest coin-return quintiles of days and -0.05 % to +0.01 % on the other three; its top 1 % of days carry 101 % of its summed daily return, and its 10 best days carry 48 %.
- **F3:** The long-side gain sits in rising years: long-bar gain is +7.91 (2020), +5.36 (2021), +7.71 (2023) and +11.50 (2024), against -1.14 (2018) and -2.07 (2022). Three windows, w21, w6 and w19, give +18.0 of the 31.1 total bar gain.
- **F4:** After a 30-day rise, the unusual 5-day move in the rise's direction is +0.09 % (t 0.26, 2,002 cases) once w21, w6 and w19 are left out, and it changes sign by year: +4.72 % (2021, t 3.45), -6.15 % (2018, t -4.17), -2.09 % (2022, t -3.18), -1.87 % (2025, t -2.72). The tested continuation after rises is mostly three bull windows.
- **F5:** Inside the trending regime, the long side carries the idea's measured effect at every horizon: the unusual move in the forecast's direction is +0.23 % over 1 day (t 3.09, 6,124 cases), +0.87 % over 3 days (t 3.27), +1.31 % over 5 days (t 2.65, strength 0.10) and +2.46 % over 10 days (t 2.58, strength 0.14). The short side gives +0.21 % over 5 days (t 0.64, 1,117 cases).
- **F6:** The strongest continuation in the data is on bars the book never trades: coins that fell over 30 days outside the trending regime fall a further 1.43 % beyond their drift over the next 5 days (t 5.48, 1,593 cases, strength 0.11) and 2.10 % over 10 days (t 4.17). After a 30-day fall, the further fall over 5 days is +0.97 %, +1.84 % (t 4.6), +0.77 % and +0.14 % (t 0.30) from the lowest to the highest quartile of net-move-to-range. It holds with w21, w6, w19 and w20 left out (+1.13 %, t 5.11, 2,293 cases) and in 6 of 8 years.
- **F7:** After a 30-day fall, the further fall grows with the size of the fall up to the middle-to-upper quintiles of |30-day return| (+0.83 %, +0.96 %, +1.96 % t 4.65, +1.69 % t 4.05), then turns into a rebound of -0.80 % (t -1.38) in the deepest quintile. The overall slope of the unusual move on the 30-day return among falls is -0.064 (t -3.88, 2,711 cases).

## Ideas
- `023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e1_choppy-declines-keep-falling` (from F6, F7, F1): In a coin that has fallen over the past 30 days while its 30-day net move stayed small against its 30-day high-low range, the choppier that fall (the smaller the net move relative to the range), the further the coin keeps falling, beyond its normal drift, over the next 5 days.
- `023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e2_clean-rises-extend-ten-days` (from F5, F1, F3): In a coin whose 30-day rise covers a large share of its 30-day high-low range, the larger that rise, the further the coin keeps rising, beyond its normal drift, over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
