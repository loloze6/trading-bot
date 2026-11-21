---
line: 7.g patterns
backtest: 018-05_hourly-plunge-loss-before-close.b1_plunge-in-uptrend-rebounds_1h
idea tested: 018-05_hourly-plunge-loss-before-close.b1_plunge-in-uptrend-rebounds
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4605 USD
---
## Findings
- **F1:** Volatility expansion is the strongest pattern outside the tested idea. On 72-hour grid cells, the top quintile of the ratio of 24-hour to 30-day hourly volatility is followed by an unusual 72-hour move of +0.96 % (strength 0.103, t 3.24, 1024 cases), against -0.42 % and -0.55 % (t -1.69 and -2.16) in the two lowest quintiles. In deciles the top decile gives +1.01 % (t 2.07) and the ninth +0.47 %.
- **F2:** The volatility-expansion rebound comes from expansions after a fall. When the 24-hour return is negative, the top volatility quintile gives +1.38 % unusual over 72 hours (strength 0.157, t 3.27, 415 cases). After a rise the same quintile gives only +0.13 % (t 0.26, 435 cases). The +1.38 % is 7 times the 0.19 % cost of a round trip.
- **F3:** The volatility-expansion rebound also needs the move to be large and the coin to be in a rising month. With a 24-hour move of at least one 30-day average move, the top volatility quintile gives +1.27 % (t 3.39, 597 cases); with a smaller 24-hour move, every quintile is zero or negative (top quintile -0.51 %, t -0.83). With a positive 30-day return the top quintile gives +1.20 % (t 2.64, 464 cases); with a negative one, +0.19 % (t 0.42, 386 cases).
- **F4:** The volatility-expansion pattern is concentrated in two coins and in the later windows. In the top quintile, XRP gives +2.03 % (t 2.21) and ZEC +2.25 % (t 2.28), and they are the only coins with a significant rank correlation (rho 0.094, p 0.012 and 0.014). BTC, ETH, LTC and XMR are each between -0.28 % and +0.34 % with t below 0.5. Windows w13-24 give +1.01 % (t 2.01); w1-12 give +0.41 % (t 1.13).
- **F5:** The tested rebound is graded by the depth of the plunge and does not grow past 3 days. With a positive 30-day return, 24-hour falls beyond 3 average moves give +5.49 % unusual (t 3.97, 28 cases), and falls of 1 to 2 moves give +1.44 % (t 2.36, 242 cases). Over all falls of at least one move in an uptrend, the unusual move is +1.90 % at 72 hours (t 3.71, 317 cases) and +1.47 % at 144 hours (t 2.17).
- **F6:** The rebound in rising months varies widely from window to window. For cells with a positive 30-day return, the unusual 72-hour move ranges from -4.83 % (w14, t -3.84) and -4.04 % (w7, t -2.37) to +3.43 % (w11, t 3.33) and +3.10 % (w18, t 3.54).
- **F7:** Hour of day shows clear but small effects, too small to pay. The one-hour unusual return is +4.8 bps at 20 UTC (t 5.98) and +3.7 bps at 21 UTC (t 4.85), and -4.2 bps at 13 UTC (t -4.46) and -3.4 bps at 02 UTC (t -4.65), about 17,400 hours each. Even two hours together (about 8.6 bps) stay below the 19 bps round trip, as F2 of the earlier runs found.
- **F8:** The book's extreme days are the coin's own large moves. Its worst 2 % of days (348) come with a mean coin return of -9.7 %, and its best 2 % with +10.5 %.

## Ideas
- `018-05_hourly-plunge-loss-before-close.b1_plunge-in-uptrend-rebounds.g1_volatility-burst-fall-rebounds` (from F1, F2, F3, F4): When a coin's volatility over the last 24 hours is high next to its own 30-day volatility and its 24-hour return is negative, the price rises over the next 3 days, and the higher that volatility ratio, the larger the rise.
- `018-05_hourly-plunge-loss-before-close.b1_plunge-in-uptrend-rebounds.g2_uptrend-plunge-with-vol-spike` (from F2, F3, F5): When a coin whose 30-day return is positive falls over 24 hours by more than its usual daily move, the price rises over the next 3 days, and the larger the 24-hour volatility next to its 30-day volatility, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
