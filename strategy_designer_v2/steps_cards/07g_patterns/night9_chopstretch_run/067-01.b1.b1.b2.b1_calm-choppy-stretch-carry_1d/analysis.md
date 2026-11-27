---
line: 7.g patterns
backtest: 067-01.b1.b1.b2.b1_calm-choppy-stretch-carry_1d
idea tested: 067-01.b1.b1.b2.b1_calm-choppy-stretch-carry
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4205 USD
---
## Findings
- **F1:** The tested stretch did not carry in any way a book could use: the slope's t is 1.22, the unusual move is +0.25 % per case over 10 days (t 0.41, 566 days), and that is 1.1 times the 0.22 % cost of a trade; on folds B and C the book's 547 trades split into longs at +4.0 % net and shorts at −2.4 % net (median −2.8 %), so the short side of the carry lost money.
- **F2:** Measured as the raw stretch, not standardised over 60 values, the move in a choppy market (60-day return within ±10 %) looks graded over the next 10 days: −11.4 % excess in the lowest tercile (t −2.73, 26 cases on 14 days), −4.3 % in the middle (t −1.07) and +7.4 % in the top (t 1.63, 26 cases on 13 days); only the lowest tercile passes |t| ≥ 2, on very few days.
- **F3:** By side, the choppy-market carry over 10 days below the average is +9.8 % calm (t 2.20, 17 days) and +10.2 % agitated (t 2.58, 8 days); above the average it is +5.8 % calm (t 1.67) and +1.0 % agitated (t 0.11, 6 cases), so neither side is firm and the agitated cells are tiny.
- **F4:** The strongest raw pattern, the next day after the lowest quintile of one-day moves in units of the 20-day swing, earns +0.70 % excess with a bar-level t of 4.82 (1,653 cases); counted per day it falls to +0.69 % (t 1.27) in rising markets, +0.57 % (t 1.13) in falling ones and −0.13 % (t −0.19) in choppy ones, and the falling agitated long rebound is already held 16 times on the map.
- **F5:** The 20-day return quintiles over the next 10 days look like momentum, −1.2, −3.2, −1.0, +2.5, +4.2 % (top t 2.27, 161 cases, not counted per day); the Wednesday next-day loss of −0.49 % (t −2.80) rests on 2019 alone (t −2.72; 2018 −0.79, 2020 0.02, 2021 −0.27). Neither stands out from the more than sixty cells examined.

## Ideas
- No ideas: Across stretch, one-day moves, 20-day returns, volatility level, profile, side, weekday and year, no pattern counted per day beats |t| ≈ 2.7 on more than a few dozen cases, which does not stand out from the more than sixty cells looked at; the one firmer-looking effect (F4) disappears once each day's cases are counted together and repeats a family the map already holds.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
