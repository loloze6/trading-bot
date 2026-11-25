---
line: 7.d confirmed, not profitable
backtest: 036-01_swing-scaled-fall-next-day-rebound_1d
idea tested: 036-01_swing-scaled-fall-next-day-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4438 USD
---
## Findings
- **F1:** The rebound lives only in falls larger than one of the coin's own daily swings, while the book spent most of its exposure on small falls. Falls of more than one 20-day swing are followed by a next-day excess return of +0.76 % to +3.66 % per bin: (-1.5,-1] +0.76 % t 3.24 n 676; (-3,-2] +1.09 % t 2.88 n 205; below -3 +3.66 % t 2.68 n 48. Falls of under half a swing earn -0.03 % (t -0.22, n 2308), yet the book held a position on 79 % of them. Falls of half to one swing earn +0.33 % (t 2.21, n 1447) over the coin's drift, while the book held 0.38 on 98 % of them.
- **F2:** On folds B and C, with a cost of 0.22 % per round trip, a book that holds only on falls beyond one swing beats both the tested position and holding on the failed measures. Sized by how far the fall exceeds one swing (half the swings beyond one, capped at 2), it reaches Sharpe 0.99, yearly +19.7 %, deepest fall -11.6 %, Calmar 1.69, in a position 10 % of the time. Replaying the book's own position gives Sharpe 0.98, deepest fall -32.0 %, Calmar 0.85; holding the coins gives Sharpe 0.79, Calmar 0.41.
- **F3:** The rebound after falls beyond one swing needs the coin's swings to be widening, measured as 10-day over 60-day swing. Where that ratio is under 0.8 (narrowing), it earns -0.22 % (t -0.73, n 279). From 0.8 to 1 it earns +0.49 % (t 1.17). From 1 to 1.25 it earns +1.27 % (t 2.60), and above 1.25 it earns +1.67 % (t 3.25, n 194).
- **F4:** The widening-swings condition is not an effect of its own. On all bars, widening swings alone earn +0.10 % (t 0.59) and +0.04 % (t 0.19), against +1.27 % to +1.67 % with the fall. Measured on the day before the fall, it still separates the cases: falls of 1 to 2 swings earn +1.36 % (t 3.78, n 246) when swings were already widening, against +1.02 % (t 1.82) otherwise. This fits the theory that forced sellers (stops, margin calls) cluster when swings are expanding.
- **F5:** Keeping the replayed position only while swings are widening cuts the deepest fall from -32.0 % to -12.4 % and raises Calmar from 0.85 to 1.10, at Sharpe 1.01. The book's deepest falls came in w9 (-30.0 %), w14 (-22.9 %) and w16 (-22.8 %), and 144 of its 199 worst 2 % position-days followed falls beyond one swing.
- **F6:** The effect does not live in one market profile. Falls beyond one swing earn +0.63 % (t 2.17) in falling markets, +0.46 % (t 0.97) in choppy ones and +0.88 % (t 2.25) in rising ones, by 60-day trend. By 30-day swing rank they earn +1.11 % (t 2.26) on calm ranks for 1-2 swing falls, so the profile's agitation does not isolate it the way the short-term widening does.
- **F7:** The tested idea's size per case is small because most cases are small falls. The unusual move is +0.09 % (t 0.66), 0.4 times the 0.22 % cost, while falls beyond one swing carry an unusual move of +0.76 % to +3.66 %, 3 to 16 times the cost. The effect held in 2018 (+0.66 %), 2020 (+1.30 %) and 2021 (+2.19 %), and vanished in 2019 (-0.03 %, n 252).

## Ideas
- `036-01.d1_beyond-one-swing-fall-rebound` (from F1, F2, F7): The more a coin's one-day fall exceeds one of its own daily swings (the standard deviation of its daily returns over the past 20 days), the more the coin rises over the next day.
- `036-01.d2_widening-swings-fall-rebound` (from F3, F4, F5, F6): While a coin's daily swings over the past 10 days are wider than over the past 60 days, the more of its own daily swings (the standard deviation of its daily returns over the past 20 days) its one-day fall spans, the more the coin rises over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
