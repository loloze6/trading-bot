---
line: 7.g patterns
backtest: 026-04_thinner-weekend-larger-reversal.d1_large-thin-weekend-moves-reverse_1h
idea tested: 026-04_thinner-weekend-larger-reversal.d1_large-thin-weekend-moves-reverse
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4287 USD
---
## Findings
- **F1:** A large fall reverses over the next day. On a non-overlapping 24-hour grid, the bottom decile of the past 24-hour return (counted in the coin's usual 24-hour moves) is followed by a drift-removed 24-hour return of +0.84 % (t 5.3, 1581 cases). The next decile shows +0.21 % (t 1.6), and deciles 3 to 9 sit between -0.25 % and -0.03 %. The effect is graded and holds only on the falling side. Its +0.84 % is about 4.4 times the 0.19 % cost of a trade.
- **F2:** A sharp single hour gives the same one-sided pattern. When the 1-hour return is in its bottom decile (counted in the coin's 720-hour volatility), the drift-removed return over the next 24 hours is +0.68 % (t 4.5, 1595 cases), against -0.05 % to -0.21 % for deciles 2 to 9. Over the next 6 hours the bottom decile gives +0.15 % (t 3.7, 6446 cases). That 6-hour rebound is positive on all six coins (t 0.7 to 2.4) and in 6 of 8 years.
- **F3:** The bars rise at 21:00 and 22:00 UTC. The 1-hour return is +0.055 % (t 6.9) at 21:00 and +0.044 % (t 5.8) at 22:00, out of 24 hours. Over the two hours together it is positive on every coin (t 3.0 to 4.6), on every weekday (t 2.0 to 4.0), and in 7 of 8 years (2022: -0.02 %, t -1.5). Each hour's move is well below the 0.19 % cost of a trade.
- **F4:** Saturday is the strongest day. The coin's mean daily return is +0.45 % (t 5.5, 2484 coin-days), positive on all six coins (t 1.4 to 2.9) and in 7 of 8 years. Friday and Saturday together beat the other days with Welch t 4.9. This is a calendar condition with no grading, so no idea is written on it.
- **F5:** The weekend reversal the brief proposes is not in the bars. The slope of the drift-removed Monday-Tuesday 48-hour return on the weekend's move is +0.0021 (t 1.5, 2227 cases). That is no stronger than for other days of the week (slopes -0.0014 to +0.0015). Split by thinness, the slope runs +0.0053 (t 2.5), -0.0018 (t -0.6) and -0.0074 (t -2.25) from the least to the most thin weekend tercile. So thinner weekends lean towards continuation, opposite to the idea, but at a t that does not stand out after this many angles.
- **F6:** The book loses its fees on Sunday. Its mean return on Sundays is -0.046 % (t -12.4), while every other weekday is between -0.045 % and +0.005 % with no |t| above 1.4. The entry fee at Sunday's close is the one reliable component of the book's -0.018 % mean daily return. The forecast's move, -0.03 % unusual per case, is about -0.1 times the cost.

## Ideas
- `026-04_thinner-weekend-larger-reversal.d1_large-thin-weekend-moves-reverse.g1_large-daily-falls-rebound` (from F1, F2): The larger a coin's fall over the past 24 hours, measured against its usual 24-hour moves, the larger its rise over the next 24 hours.
- `026-04_thinner-weekend-larger-reversal.d1_large-thin-weekend-moves-reverse.g2_hourly-plunges-rebound-next-day` (from F2, F1): The larger a single hour's fall in a coin, measured against its usual hourly moves, the larger the coin's rise over the next 24 hours.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
