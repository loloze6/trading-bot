---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-03_low-volume-up-fade.d1_high-volume-drop-rebounds
line: 7.d not profitable
backtest: 028-03_low-volume-up-fade.d1_high-volume-drop-rebounds_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin falls far more than its typical hourly move over the past 30 days, on volume several times its average hourly volume over the past 30 days, the price recovers part of that fall over the next two hours, with the recovery growing steeply with the depth of the fall in typical hourly moves, so that most of it comes after falls of many typical moves. The higher that hour's volume against its 30-day average, the larger the recovery.
Consequence: Only the most extreme volume-backed hourly drops are worth buying for a two-hour rebound, because their recovery is several times a trade's cost; ordinary drops are a reason to stay out.
Why:
- F1: The book gains before costs but fees take more than twice that gain: its mean gain per bar is +0.38 bp (t 3.31 over 140042 bars) against a mean fee of 0.82 bp, with turnover of 0.155 of the book per bar. Its 25808 trades earn +0.093 % each before fees and −0.007 % after, against a trade cost of 0.11 %.
- F2: The fees are spent mostly where the forecast is weak.
- F3: The rebound is large only after the most extreme falls on a volume surge. On the non-overlapping 2-hour grid, the unusual 2-hour move by size of fall (in 30-day hourly standard deviations) is:
- F4: The extreme-fall rebound recurs across years. After hourly falls deeper than 5 standard deviations on volume over 3 times its mean, the unusual 2-hour move is positive in 7 of 8 years, from +8 bp in 2024 to +221 bp in 2020. The only negative year is 2019, at −40 bp.
- F5: The rebound is a two-hour effect, and positions held longer lose.
