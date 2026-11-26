---
line: 7.b inconclusive
backtest: 064-01_rising-agitated-volume-shrink-rises_1d
idea tested: 064-01_rising-agitated-volume-shrink-rises
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3539 USD
---
## Findings
- **F1:** The test's result is on the side the idea predicts but short of the bar. The slope t is +1.58 on 718 profile grid bars, and the 211 cases with a positive forecast had a mean excess 5-day return of +1.29 %. The size is an unusual move of +1.71 % per case, 0.161 of the coin's usual 5-day move of 10.60 %, but how sure it is stays low: t 1.39 over 158 days. In folds B and C the slope of the excess 5-day return on the forecast is t +1.33 (n 393).
- **F2:** The idea's own grading, the raw 30-day volume shrinkage, sorts the profile's 5-day moves in order. Its slope on the 5-day return is t +2.13 (n 140). By quintile of the volume change, the most-shrunk fifth (log ratio −0.61) has a mean excess 5-day return of +3.2 % and the most-grown fifth (+1.21) has −3.4 %, with the 20-day return going from +26.7 % to −7.0 %. The plan's forecast standardises the ratio over its last 60 values, which blurs this grading. Its slope on the same returns was only t +1.33.
- **F3:** The relation lives in the rising agitated market, as the brief says. Outside the profile, in rising markets (60-day return above +10 %), the shrinkage slope is t +0.68 (n 178), and over all grid bars it is t +0.25 (n 812). Inside the profile it is t +2.13.
- **F4:** The effect grows with the horizon. On non-overlapping grids in the profile, the raw shrinkage slope is t +2.97 at 10 days (n 68) and t +2.04 at 20 days (n 32). For the plan's forecast, it is t +1.10 at 10 days (n 199) and t +2.29 at 20 days (n 97). On these few cases, though, part of the move falls after the plan's 5 days.
- **F5:** The evidence is thin and mixed, and the shortfall comes from too few cases.
- **F6:** Cost is not what stops the book. The total move per case of +2.34 % is 12.1 times the 0.19 % cost of a trade, and the unusual move is 8.9 times that cost. The book's weak Sharpe of 0.29 and yearly return of +1.3 % come from being in a position on only 8 % of coin-days with an effect that is not yet sure.

## Ideas
- `064-01.b1_volume-shrink-rises-more-coins` (from F1, F2, F3, F5): In a rising, agitated market, the more a coin's total volume over the last 30 days has shrunk against the 30 days before, the larger its rise over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
