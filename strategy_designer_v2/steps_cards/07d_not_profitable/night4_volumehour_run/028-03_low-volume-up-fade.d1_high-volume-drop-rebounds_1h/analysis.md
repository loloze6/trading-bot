---
line: 7.d not profitable
backtest: 028-03_low-volume-up-fade.d1_high-volume-drop-rebounds_1h
idea tested: 028-03_low-volume-up-fade.d1_high-volume-drop-rebounds
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3519 USD
---
## Findings
- **F1:** The book gains before costs but fees take more than twice that gain: its mean gain per bar is +0.38 bp (t 3.31 over 140042 bars) against a mean fee of 0.82 bp, with turnover of 0.155 of the book per bar. Its 25808 trades earn +0.093 % each before fees and −0.007 % after, against a trade cost of 0.11 %.
- **F2:** The fees are spent mostly where the forecast is weak.
- **F3:** The rebound is large only after the most extreme falls on a volume surge. On the non-overlapping 2-hour grid, the unusual 2-hour move by size of fall (in 30-day hourly standard deviations) is:
- **F4:** The extreme-fall rebound recurs across years. After hourly falls deeper than 5 standard deviations on volume over 3 times its mean, the unusual 2-hour move is positive in 7 of 8 years, from +8 bp in 2024 to +221 bp in 2020. The only negative year is 2019, at −40 bp.
- **F5:** The rebound is a two-hour effect, and positions held longer lose.
- **F6:** Over a day, falls on ordinary volume show a recovery larger than a trade's cost, but it is weak on independent cases.

## Ideas
- `028-03_low-volume-up-fade.d1_high-volume-drop-rebounds.d1_extreme-volume-drops-rebound` (from F1, F2, F3, F4, F5): After an hour in which the coin falls far more than its typical hourly move over the past 30 days, on volume several times its average hourly volume over the past 30 days, the price recovers part of that fall over the next two hours, with the recovery growing steeply with the depth of the fall in typical hourly moves, so that most of it comes after falls of many typical moves. The higher that hour's volume against its 30-day average, the larger the recovery.
- `028-03_low-volume-up-fade.d1_high-volume-drop-rebounds.d2_hourly-drops-recover-over-day` (from F3, F6): After an hour in which the coin falls far more than its typical hourly move over the past 30 days, the price recovers over the next 24 hours, more the deeper that fall in typical hourly moves.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
