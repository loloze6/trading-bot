---
line: 7.g patterns
backtest: 018-05_hourly-plunge-loss-before-close.d2_ten-day-rebound-after-plunge_1h
idea tested: 018-05_hourly-plunge-loss-before-close.d2_ten-day-rebound-after-plunge
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3988 USD
---
## Findings
- **F1:** The coin's own 10-day return carries forward over the next 10 days. On non-overlapping 240-hour cases ranked within each coin, the top quintile of the prior 10-day return is followed by an unusual move of +3.0 % (t 2.52, 312 cases, strength 0.17). The second and third quintiles are followed by −2.3 % (t −3.11, 303 cases) and −1.8 % (t −2.34, 296 cases). Top quintile minus second quintile is about +5.3 % (Welch t ≈ 3.8). The top quintile's unusual move is about 16 times the 0.19 % cost of a trade.
- **F2:** The prior 30-day return shows the same carry-forward, more weakly. Its top quintile is followed by +2.8 % unusual over 10 days (t 1.96, 249 cases), its middle quintile by −1.7 % (t −2.13, 248 cases), and its bottom quintile by +0.6 % (t 0.59), so the carry-forward is not clean at the low end.
- **F3:** The tested idea's own situation points the other way, though not beyond chance. After a 24-hour fall of more than 2 usual daily moves that followed a 30-day rise, the next 10 days run −3.0 % against drift (t −1.56, 26 cases). After a 24-hour rise of the same size following a 30-day rise, they run +4.4 % (t 1.19, 57 cases).
- **F4:** The 24-hour return's sign also carries forward over the next 10 days. A 24-hour rise of up to one usual daily move is followed by +1.9 % unusual (t 2.21, 369 cases); a fall of up to one is followed by −1.4 % (t −2.06, 409 cases).
- **F5:** Ten-day outcomes depend heavily on the year. 2018 averaged −4.7 % unusual (t −3.64, 207 cases) and 2022 −2.6 % (t −2.80), against +3.0 % in 2020 (t 2.67). The book's mean daily return was likewise −0.22 % in 2018 and +0.44 % in 2020, close to holding (−0.35 % and +0.42 %).
- **F6:** The book's gain sits in rare large days and in skewed trades.
- **F7:** Coin by coin, the book's trades are mostly carried by ZEC. Its mean net trade is +44 % (166 trades) against +0.7 % to +9.4 % for the other five coins. Trades entered in the 00–06 UTC quarter average +21.7 % against about +4 % for the other quarters.
- **F8:** Several angles showed no pattern beyond chance across about ten groupings. These were 24-hour volatility terciles (−0.7 % to +0.8 %, |t| ≤ 1.17), weekday (|t| ≤ 2.04, only Saturday near 2), and whether the book was in or flat (t 0.26 and −0.42).

## Ideas
- `018-05_hourly-plunge-loss-before-close.d2_ten-day-rebound-after-plunge.g1_ten-day-return-carries-forward` (from F1, F2, F4): The larger a coin's own 10-day return, read at an hourly close, the more the coin rises over the next 10 days beyond its normal drift; a coin that fell over its last 10 days lags its drift over the next 10 days, by more the larger its fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
