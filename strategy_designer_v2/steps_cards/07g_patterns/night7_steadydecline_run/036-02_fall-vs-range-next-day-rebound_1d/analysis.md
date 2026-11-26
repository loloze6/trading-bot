---
line: 7.g patterns
backtest: 036-02_fall-vs-range-next-day-rebound_1d
idea tested: 036-02_fall-vs-range-next-day-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3875 USD
---
## Findings
- **F1:** Across all coin-days in folds B and C, the next-day excess return falls as the close moves up the day's range. Closes in the lowest fifth of the day's high-low range are followed by +0.52 % (t 2.04, 613 days, hit 59 %), closes in the second fifth by +0.28 %, and closes in the top fifth by -0.34 % (t -1.66, hit 42 %). Where a day closes in its range carries next-day information whatever the size of the fall.
- **F2:** Among falls of at least one 30-day mean range (344 cases), what follows depends on where the day closed. Falls closing in the middle third of the day's range are followed by +2.08 % (t 3.00, 64 days, hit 73 %) and those in the lowest third by +1.39 % (t 1.33). Falls that closed in the top third, recovering off their low within the day, are followed by -0.23 % (t -0.29, hit 53 %). The rebound belongs to falls that did not already recover during the day.
- **F3:** Among the same outsized falls, those that came after the weakest 5-day returns (lowest tercile) are followed by +2.49 % (t 2.13, 46 days, hit 69 %). The middle tercile is followed by -0.07 % (t -0.10) and the top tercile by +0.76 % (t 1.06). An outsized fall that ends a several-day decline rebounds most.
- **F4:** The outsized falls' next-day rebound grows with the coin's 30-day swing, terciles taken within each coin: +0.02 % in the calmest third (t 0.02, 52 days), +0.67 % in the middle (t 1.23) and +2.68 % in the most agitated third (t 1.91, 61 days). By 60-day trend, rising markets give +1.31 % and falling ones +1.56 %, while choppy markets give only +0.19 % on 35 cases.
- **F5:** The rebound is not limited to falls beyond one mean range, and it is graded. Falls of 0.5 to 1 range are followed by +0.74 % (t 2.28, 305 days), 1 to 1.5 ranges by +0.38 %, 1.5 to 2 ranges by +1.24 % and 2 to 2.5 ranges by +3.48 % (t 2.11). Small up days of 0 to 0.5 range are followed by -0.36 % (t -1.98). Measured against the 30-day standard deviation of daily returns the gradient is the same: +0.48 %, +1.20 % and +3.80 % for falls of 1–2, 2–3 and over 3 standard deviations.
- **F6:** Every coin shows the outsized-fall rebound, from BTC +0.57 % to XRP +1.55 %, each with t between 1.0 and 1.6. Every year from 2018 to 2021 shows it too, from +0.29 % to +2.25 %. The size per case (+0.4 % to +2.5 % in the stronger subsets) covers the 0.19 % cost of a trade several times over. I looked at about a dozen angles, so only F1 to F3 stand out with t near or above 2, and none stands out strongly.

## Ideas
- `036-02.g1_outsized-fall-weak-close` (from F2, F1, F5): The further a coin's one-day fall exceeds its average daily high-to-low range over the past 30 days, the larger its rise over the next day. This holds more strongly the closer the day closes to its low rather than recovering toward its high.
- `036-02.g2_outsized-fall-after-decline` (from F3, F5): The further a coin's one-day fall exceeds its average daily high-to-low range over the past 30 days, and the lower its 5-day return ending that day, the larger its rise over the next day.
- `036-02.g3_agitated-outsized-fall-rebound` (from F4, F6): In an agitated market, the further a coin's one-day fall exceeds its average daily high-to-low range over the past 30 days, the larger its rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
