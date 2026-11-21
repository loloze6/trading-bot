---
line: 7.g patterns
backtest: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds_1h
idea tested: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4048 USD
---
## Findings
- **F1:** Large 24-hour moves are followed by a rise over the next 72 hours in either direction. The top quintile of the absolute 24-hour return, in multiples of the coin's 30-day mean absolute 24-hour return, has a mean unusual 72-hour move of +1.36 % (t 4.30, 849 independent cases, strength 0.156), about 7 times the 0.19 % cost of a trade. The four lower quintiles are all between -0.49 % and -0.14 %, none with |t| above 1.85.
- **F2:** The rise follows sharp falls and sharp rises alike. The deepest seventh of 24-hour falls (below -1.2 usual daily moves) gives +1.09 % over 72 hours (t 3.27, 607 cases). The highest seventh of 24-hour rises (above 1.3) gives +0.87 % (t 2.35, 606 cases). The five middle sevenths run from -0.52 % to +0.11 %. Ranked over all 4243 cases, the absolute 24-hour move correlates with the unusual 72-hour move at Spearman rho 0.058 (p 0.0002).
- **F3:** After a sharp fall, the rebound keeps growing past the tested horizon. On the 611 deepest-fall cases the unusual move is +0.78 % over 24 hours (t 3.46), +1.12 % over 72 hours (t 3.36, strength 0.13) and +1.82 % over 168 hours (t 3.30, 589 cases).
- **F4:** Among falls, a deeper 24-hour fall is followed by a larger 72-hour move. The Spearman rho is 0.083 (p 0.00015, 2054 cases). Inside a positive 30-day return, the deepest quartile of falls gives +2.17 % (t 3.78, 238 cases, strength 0.26). Inside a negative 30-day return, the same quartile gives only +0.62 % (t 1.33, 276 cases).
- **F5:** The rebound after sharp falls is uneven over time, so it depends on the regime. By year, the deepest-fall cases give:
- **F6:** The tested forecast is barely graded in practice, which explains why the supporting check could not be run. On bars with a positive forecast, 53 % sit at the +20 cap and the median is 20. As a result, all 2803 cases tied at or below the median entry forecast.
- **F7:** The book's worst days are followed by recoveries. On its worst decile of days (mean -4.75 %, coin -5.67 %), the next day's coin return is +0.72 % and the book's is +0.65 %. Both are larger than after any of the middle eight deciles (at most +0.28 % and +0.19 %).

## Ideas
- `018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.g1_large-daily-shock-precedes-rise` (from F1, F2): When a coin's 24-hour return, read at an hourly close, is large in either direction in multiples of its 30-day mean absolute 24-hour return, the coin rises over the next 3 days more than its normal drift, and the larger that move, the larger the rise.
- `018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.g2_sharp-dip-week-long-rebound` (from F3, F4, F7): When a coin's 24-hour return, read at an hourly close, is a fall of several of its 30-day mean absolute 24-hour returns, the coin rises over the next 7 days more than its normal drift, and the deeper the fall in those multiples, the larger the rise.
- `018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.g3_graded-dip-in-uptrend` (from F4, F6, F5): When a coin's 24-hour return, read at an hourly close, is a fall measured in multiples of its 30-day mean absolute 24-hour return, the coin rises over the next 3 days more than its normal drift, and the rise is larger the larger the fall multiplied by the coin's 30-day return measured in multiples of its usual 30-day move, with a continuous scale whose values stay distinct up to the deepest falls.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
