---
line: 7.g patterns
backtest: 058-01.g2.b1.d3.b2_large-one-day-rises-fade_1d
idea tested: 058-01.g2.b1.d3.b2_large-one-day-rises-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4370 USD
---
## Findings
- **F1:** Outside the falling agitated profile, past moves scaled by the coin's 30-day swing continue over the next 5 days, and most clearly in falling calm markets: the Spearman correlation of the 10-day scaled return with the next 5-day unusual move is +0.24 (p 0.0001, 265 non-overlapping cases), and the 5-day one is +0.23 (p 0.0001). Cases with a 10-day scaled return above +1 end +5.60 % above drift (t 2.51 with the cases of one day together, 14 days, strength 0.46). Cases below -1 end -3.34 % (t -1.45, 30 days).
- **F2:** In choppy markets the same continuation shows: the 5-day scaled return correlates +0.34 with the next 5-day unusual move (p < 0.0001, 152 cases), and the 10-day one +0.29 (p 0.0002). Cases above +1 end +6.46 % above drift (strength 0.50, t 1.26, 13 days). Cases from -1 to 0 end -2.79 % (t -1.52, 39 days).
- **F3:** On every day outside the profile together, one-day moves continue over the next 5 days: one-day rises above 2 swings are followed by +8.37 % unusual (t 2.82, 40 cases), and one-day falls below -2 swings by -4.78 % (t -2.38, 19 cases). Inside the profile, rises of 1 to 2 swings are followed by -4.54 % (t -2.99, only 7 cases).
- **F4:** Inside falling agitated markets the sign reverses: the 10-day scaled return correlates -0.17 with the next 5-day unusual move (p 0.0075, 246 cases). This reversal is carried mainly by the falls. A 10-day scaled return below -1 is followed by +8.04 % (t 1.72, 17 days), and cases with z10 below -0.5 beat the other cases in every year from 2018 to 2021. The rises do not fade clearly: a 10-day scaled return above +1 is followed by -1.25 % (t -0.70, 12 days). The 10-day fall rebound is the long side the map already holds 12 times, so it is not a discovery.
- **F5:** The tested book barely moves on folds B and C. Its mean daily return per window lies between -0.026 % and +0.047 %. It loses in w13, w16, w17 and w18, and its gain comes from w8, w9 and w14. This fits a step 5 t of 1.84 and a leave-one-window-out Sharpe of -0.03.

## Ideas
- `058-01.g2.b1.d3.b2.g1_falling-calm-scaled-continuation` (from F1, F3): In a falling, calm market, the larger a coin's 10-day return against the standard deviation of its daily returns over the past 30 days, the larger its further move in the same direction over the next 5 days.
- `058-01.g2.b1.d3.b2.g2_choppy-market-scaled-continuation` (from F2, F3): In a choppy market, the larger a coin's 5-day return against the standard deviation of its daily returns over the past 30 days, the larger its further move in the same direction over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
