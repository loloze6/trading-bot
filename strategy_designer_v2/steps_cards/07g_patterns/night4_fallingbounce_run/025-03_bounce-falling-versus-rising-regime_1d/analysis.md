---
line: 7.g patterns
backtest: 025-03_bounce-falling-versus-rising-regime_1d
idea tested: 025-03_bounce-falling-versus-rising-regime
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4018 USD
---
## Findings
- **F1:** In coins whose 90-day return is 0 or above, the 5-day excess return after an up day grows with the rise's size in usual 20-day moves: +2.18 % (t 2.25, 149 grid cases) for 1 to 2 moves, +3.67 % (t 2.32, 43) for 2 to 3, and +7.28 % (t 1.85, 27) above 3. The slope of the 5-day excess return on the rise over all up days is +0.0138 per usual move (t 3.08, 751 cases).
- **F2:** These rising-market rises of more than one usual move have a strength of 0.267 of the coin's usual 5-day move (t 3.64, 219 cases), about 2.8 % per case, roughly 15 times the 0.19 % cost of a trade. They are positive in all six coins (t from 0.38 for LTC to 2.21 for ZEC) and in 7 of 8 years (only 2022 is negative, with 6 cases).
- **F3:** The tested fade in falling markets (90-day return below 0) does not show, which is what sinks the book:
- **F4:** Rises of more than one usual move are followed by stronger 5-day excess returns when volatility is quiet:
- **F5:** Down days of more than one usual move are followed by a next-day excess rebound:
- **F6:** Weekday effects in next-day returns do not hold up as a pattern.

## Ideas
- `025-03_bounce-falling-versus-rising-regime.g1_sharp-rises-extend-uptrends` (from F1, F2, F3): In one coin whose 90-day return is positive, the larger the day's rise measured in usual daily moves of its last 20 days, the higher the coin's return over the next 5 days.
- `025-03_bounce-falling-versus-rising-regime.g2_quiet-market-breakouts-continue` (from F4, F1): In one coin, after a one-day rise of several usual daily moves, the lower its 20-day volatility relative to its 60-day volatility, the higher its return over the next 5 days.
- `025-03_bounce-falling-versus-rising-regime.g3_sharp-falls-rebound-next-day` (from F5): In one coin, the larger the day's fall measured in usual daily moves of its last 20 days, the higher its return over the next 1 day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
