---
line: 7.g patterns
backtest: 018-06_hourly-plunge-multiday-continuation.d1_hourly-plunge-next-day-rebound_1h
idea tested: 018-06_hourly-plunge-multiday-continuation.d1_hourly-plunge-next-day-rebound
step 5: rejected
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3858 USD
---
## Findings
- **F1:** When a coin's 24-hour return, read on the 24-hour grid, is a drop of at least 3 times its 30-day mean absolute 24-hour return, the next 24 hours end above the coin's normal drift. Over 376 independent cases on 6 coins the mean strength is 0.378 (t 4.6) and the unusual move is +1.87 %. That is about 10 times this backtest's 0.19 % cost of a buy and a sell.
- **F2:** Past about 3 multiples the rebound is graded, and its strength climbs much faster than the drop's size:
- **F3:** The deep-drop rebound is positive on all 6 coins: strength 0.16 on LTC to 0.50 on XMR, t 0.8 to 2.6, about 53 to 72 cases each. It is not stable over time. In the first half of the windows it is 0.069 (t 0.9, 194 cases); in the second half it is 0.706 (t 4.9, 182 cases).
- **F4:** The tested forecast was fully long from 2 multiples onward, so most of its 8426 cases were mild drops. Drops of 0 to 1 multiple even end below drift: strength -0.039, t -2.8, 4968 cases. This explains the tested idea's measured strength of 0.020 and its unusual move of 0.6 times the cost.
- **F5:** Among deep drops, those whose last 24 hours were most volatile against the past 30 days rebound most. In the top third of the 24-hour/720-hour volatility ratio the strength is 0.691 (t 3.6, 117 cases, +3.47 %), against 0.26 to 0.30 in the lower two thirds.
- **F6:** A close in the top 3 % of the 30-day range is followed over 7 days by strength 0.318 (t 2.1, 91 cases, +4.9 % unusual). This rests mostly on XRP (0.809) and the second half (0.338, t 3.2 against 0.030). Per-coin Spearman of range position against strength is only 0.00 to 0.07, so it is not distinct from chance across the many angles looked at.
- **F7:** The volatility ratio alone, the 72-hour drop multiple, and the book's weekday and year splits show no pattern beyond chance. The largest bins reach t 1.7 to 2.8, with mixed signs between neighbouring bins.

## Ideas
- `018-06_hourly-plunge-multiday-continuation.d1_hourly-plunge-next-day-rebound.g1_extreme-plunge-convex-rebound` (from F1, F2, F3, F4): When a coin's 24-hour return, read at an hourly close, is a drop far beyond its usual daily moves, measured in multiples of its 30-day average absolute 24-hour return, the price rises over the next 1 day by more than the coin's normal drift. The rise grows much faster than the multiple, so the most extreme drops are followed by rebounds several times larger than those after moderate ones.
- `018-06_hourly-plunge-multiday-continuation.d1_hourly-plunge-next-day-rebound.g2_violent-plunge-stronger-rebound` (from F1, F5): When a coin's 24-hour return, read at an hourly close, is a drop of several times its 30-day average absolute 24-hour return, the price rises over the next 1 day by more the higher that 24-hour stretch's hourly volatility stands against its 30-day hourly volatility.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
