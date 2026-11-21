---
line: 7.g patterns
backtest: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b1_hourly-plunge-rebound-19-coins_1h
idea tested: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b1_hourly-plunge-rebound-19-coins
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.5101 USD
---
## Findings
- **F1:** The rebound after a 24-hour drop is a high-volatility effect. On the 48-hour non-overlapping grid, drops of at least 2 multiples of the 30-day average absolute daily return gave +3.24 % unusual move in the coin's own top volatility tercile (t 4.49, 239 cases, strength 0.45). The middle tercile gave +0.19 % (t 0.44, 361 cases) and the bottom tercile −0.23 % (t −0.79, 414 cases).
- **F2:** The same split holds when volatility is measured against the coin's own past, using its 30-day average absolute daily return over its 180-day mean. Drops of at least 2 multiples gave +2.26 % over 48 hours in the top tercile (t 4.76, 233 cases), +0.02 % in the middle (t 0.03) and −0.32 % in the bottom (t −0.68). Over 96 hours the top tercile gave +4.21 % (t 3.28, 114 cases).
- **F3:** Inside high volatility the rebound is graded. The slope of 48-hour strength on the size of the drop is 0.32 (t 3.59) in the top volatility tercile, 0.19 (t 3.30) in the middle and 0.05 (t 1.58) in the bottom.
- **F4:** The high-volatility rebound is broad but not steady.
- **F5:** The rebound is far larger than the cost of a trade. In the top volatility tercile the total 48-hour move per case is +2.6 % to +3.2 % against a 0.22 % round trip, 12 to 15 times the cost. Over all drops of at least 2 multiples the unusual move is +0.56 %, 2.5 times the cost.
- **F6:** Unconditional drops are not graded. Across all volatility levels, drops of 2 to 3 multiples gave −0.10 % over 48 hours (t −0.35, 669 cases), while drops beyond 3 multiples gave +2.3 % to +2.4 % (t 3.3 to 3.6, 345 cases). Most of the tested idea's edge therefore sits in a few large, high-volatility drops.
- **F7:** The book earned 0.04 % a day against 0.15 % for holding (daily sd 1.6 % vs 5.7 %). Its trades held up to 2 days averaged +2.9 % net (6,753 trades). Trades held 3 to 5 days averaged −3.8 % (1,913) and 5 to 10 days −3.3 % (1,649). Holding past the 2-day horizon when the forecast stays on cost the book.
- **F8:** Large 24-hour rises in the coin's low-volatility tercile gave +1.07 % over 48 hours (t 3.63, 530 cases, 15 of 19 coins). The result is not robust:
- **F9:** Large 24-hour rises when the 30-day return is negative gave −0.89 % over 48 hours (t −2.37, 319 cases). Hour of day (block 04–08 UTC: +2.7 %, t 2.47, 110 cases) and past 7-day return quintiles showed nothing graded. Given the number of angles looked at, none of these stands out from chance.

## Ideas
- `018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b1_hourly-plunge-rebound-19-coins.g1_high-volatility-plunge-two-day-rebound` (from F1, F2, F3, F4, F5, F6): When a coin's average absolute daily return over the last 30 days is high relative to its own level over the past 6 months, a 24-hour drop measured in multiples of that average is followed by a rise over the next 2 days above the coin's usual 2-day drift. The larger the drop in multiples and the higher the coin's recent volatility relative to its past, the larger the rise.
- `018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b1_hourly-plunge-rebound-19-coins.g2_high-volatility-plunge-four-day-rebound` (from F2, F3, F5, F7): When a coin's average absolute daily return over the last 30 days is high relative to its own level over the past 6 months, a 24-hour drop measured in multiples of that average is followed by a rise over the next 4 days above the coin's usual 4-day drift. The larger the drop and the higher the relative volatility, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
