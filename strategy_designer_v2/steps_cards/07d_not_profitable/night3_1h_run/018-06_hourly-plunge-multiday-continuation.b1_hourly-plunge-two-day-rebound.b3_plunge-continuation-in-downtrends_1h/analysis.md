---
line: 7.d not profitable
backtest: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b3_plunge-continuation-in-downtrends_1h
idea tested: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b3_plunge-continuation-in-downtrends
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4041 USD
---
## Findings
- **F1:** The book loses because it sits short in coins that rise. It is short 59 to 70 % of the bars, with a mean position of -0.35 to -0.51 of the book. That position costs it -0.0004 to -0.00075 per day from the coins' own rise (coins' mean daily return +0.07 % to +0.16 %). Its timing earns only -0.00003 to +0.0011 per day. Only BTC's book is positive (+0.036 %/day); ETH to ZEC run from -0.007 % to -0.093 %/day.
- **F2:** The move the book bets on is the wrong way and smaller than a trade's cost. Over 2265 cases, the short-direction total move is -0.20 % at 4 days (t -0.99) and -0.39 % at 8 days, against a round trip of 0.19 %. The unusual move is +0.31 % only because the coins' normal drift is up.
- **F3:** The tested depth relation is reversed. In the deepest quintile of 30-day returns (-67 % to -27 %), short cases lose -1.71 % over 4 days (t -2.60, 318 cases) and -3.5 % over 8 days. The middle quintile (-16 % to -8 %) gains +1.10 % short (t 2.51, 317 cases).
- **F4:** Plunges of at least 1.5 usual daily moves, taken on price alone with one per 4-day cell, continue down only in mild 30-day falls. With the 30-day return between -22 % and -1 %, the unusual 4-day move is -0.93 % (t -1.89) and -0.92 % (t -2.14), 341 cases each, about 0.10 of a usual move. That makes a short-side total of about +0.42 %, about 2.2 times the cost.
- **F5:** After the same plunges in deep 30-day falls (below -22 %), the coin rebounds. It rises +1.34 % over 4 days (unusual +0.82 %, t 1.28, strength 0.09, 341 cases) and +3.5 % over 8 days, about 18 times the cost. The rebound is stronger in w1-12 (unusual +1.40 %, t 2.15) than in w13-24 (+0.40 %, t 0.44).
- **F6:** Plunges in coins that rose over 30 days rebound, and more so the larger the plunge. The 4-day rise is +0.74 % (1106 cases), +1.77 % (283) and +3.90 % (50) for plunges of 1.5 to 2, 2 to 3, and more than 3 usual daily moves. With a 30-day return of +8 % to +23 %, the unusual 4-day move is +1.68 % (t 3.15, 341 cases, strength 0.18).
- **F7:** The book's trades last 215 to 256 hours on average, about twice the 4-day horizon. Those over 200 hours earn +5.03 % net (2403 trades). Those of 24 to 200 hours lose -4.75 % to -10.85 % net (3424 trades), so the loss sits in the shorts that end near the horizon.

## Ideas
- `018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b3_plunge-continuation-in-downtrends.d1_plunge-continuation-shallow-downtrends` (from F2, F3, F4): When a coin's 24-hour return falls by a large multiple of its 30-day average absolute daily return while its 30-day return is negative, the price falls further over the next 4 days by more than the coin's usual 4-day drift, only while the 30-day fall is shallow, and the larger the 24-hour fall against its usual size, the larger the further decline.
- `018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b3_plunge-continuation-in-downtrends.d2_capitulation-plunge-eight-day-rebound` (from F3, F5, F7): When a coin whose 30-day return is deeply negative falls by a large multiple of its 30-day average absolute daily return over 24 hours, the price rises over the next 8 days, and the deeper the 30-day fall, the larger the rise.
- `018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b3_plunge-continuation-in-downtrends.d3_uptrend-plunge-four-day-rebound` (from F1, F6): When a coin whose 30-day return is positive falls over 24 hours by a multiple of its 30-day average absolute daily return, the price rises over the next 4 days by more than the coin's usual 4-day drift, and the larger the 24-hour fall against its usual size, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
