---
line: 7.b inconclusive
backtest: 058-02.b1.g1.b1.b2.b2_agitated-downtrend-sharp-fall-rebound_1d
idea tested: 058-02.b1.g1.b1.b2.b2_agitated-downtrend-sharp-fall-rebound
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3933 USD
---
## Findings
- **F1:** The tested slope is on the predicted side everywhere but clear nowhere. On folds B and C (782 positive-forecast bars, 305 days), the slope of next-day excess return on the forecast is +0.00144 with a day-clustered t of 2.08. Every coin has a positive slope, with t from 0.67 (TRX) to 2.19 (ADA). Every year has a positive slope, with t from 0.70 (2018) to 1.69 (2020). This matches step 5's full-data result: slope t 1.78 on 2,872 bars over 832 days.
- **F2:** The grading rests on a handful of extreme falls. The 16 in-profile falls beyond 3 usual swings were followed by a mean excess next day of +8.6 %. Without them, the slope drops to t 1.13 (642 bars, 244 days). Clipping the next-day returns at their 2 % and 98 % points keeps t at 2.01.
- **F3:** The rebound behaves more like a step than a slope. By forecast quintile, the next-day excess is -0.57 % (t -1.1) for the smallest falls, then +1.20 %, +1.10 %, +1.83 % and +2.28 % (t 2.7 to 3.9). Any real fall rebounds by about 1 to 2 %, so a linear slope on the forecast is a noisy way to read it.
- **F4:** The profile matters. In falling agitated markets, falls of 1 to 2 usual swings are followed by +1.5 % to +1.9 % the next day (125 cases). Outside the profile, the same falls are followed by only +0.6 % to +0.8 % (699 cases). The mean excess on positive-forecast bars is +1.17 % (t 2.86).
- **F5:** The one-day horizon is where the effect shows best. On non-overlapping grids, the slope t is 2.08 at 1 day, 1.27 at 2 days, 0.31 at 3 days and 0.81 at 5 days. Neither a longer horizon nor a deeper 60-day downtrend (t 0.8 to 1.3 in each depth band) gives a clearer reading.
- **F6:** The rebound comes on broad sell-off days, not on a coin's own fall. When only one coin is in a position that day, the mean excess is -0.23 % (149 days). When more than six are, it is +2.46 % (24 days). An idea must read one coin's own bars, so this cannot become a condition.

## Ideas
- No ideas: The result is on the predicted side in every coin and every year, but it is too small and too dependent on about 16 extreme falls to clear the bar (F1, F2). The test already used every coin and fold available on daily bars, so there is no more data to add. Neither a horizon, a trend depth nor a profile in these findings isolates a part of the data where the graded effect shows clearly (F5); where it does concentrate, broad sell-off days, cannot be written as a one-coin idea (F6).

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
