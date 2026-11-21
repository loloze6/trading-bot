---
line: 7.d not profitable
backtest: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.b1_deeper-dip-larger-rebound_1h
idea tested: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.b1_deeper-dip-larger-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3728 USD
---
## Findings
- **F1:** The check fails on Calmar alone (0.60 against 0.75). The chained book's deepest fall is −33.0 % against a yearly return of +19.9 %, and that fall runs 217 days from w1 to w3, while holding the coins lost 65.9 % over the same stretch. Book returns were −6.6 %, −13.9 % and −8.0 % in w1, w2 and w3, and its deepest falls inside one window are −23.8 % (w3), −21.9 % (w14) and −20.6 % (w18), all windows where holding lost (−10 %, −49 %, −22 %).
- **F2:** The dips that rebound are the ones whose week is still rising. Across 1,887 recomputed cases, the unusual 72-hour return rises steadily with the coin's 7-day return:
- **F3:** The dip's own depth does not grade the rebound; the 30-day and 7-day trends do.
- **F4:** Losses cluster in dips taken far below the coin's 30-day high.
- **F5:** Dips in a quiet market pay less than dips in a volatile one.
- **F6:** Size is not the problem. The total move is +0.96 % per case, 5.0 times the 0.19 % cost of a trade, and the unusual move is 2.9 times that cost. The failure comes from deep falls in collapsing markets, not from costs.

## Ideas
- `018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.b1_deeper-dip-larger-rebound.d1_dip-in-rising-week-rebounds` (from F1, F2, F3): When a coin's 24-hour return, read at an hourly close, falls by several times its 30-day average absolute daily return while its 30-day return is positive, the coin rises over the next 3 days more than its normal drift, only while its 7-day return is positive, and the higher its 7-day return, the larger the rise.
- `018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.b1_deeper-dip-larger-rebound.d2_dip-near-monthly-high-rebounds` (from F1, F4): When a coin's 24-hour return, read at an hourly close, falls by several times its 30-day average absolute daily return while its 30-day return is positive, the coin rises over the next 3 days more than its normal drift, and the closer the coin's close is to its 30-day high, the larger the rise.
- `018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.b1_deeper-dip-larger-rebound.d3_volatile-dip-rebounds-more` (from F5, F6): When a coin's 24-hour return falls by several times its 30-day average absolute daily return while its 30-day return is positive, the coin rises over the next 3 days more than its normal drift, and the higher its 7-day volatility relative to its 60-day volatility, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
