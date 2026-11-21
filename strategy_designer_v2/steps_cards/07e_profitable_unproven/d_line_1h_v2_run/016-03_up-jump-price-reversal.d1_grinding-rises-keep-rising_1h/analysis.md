---
line: 7.e profitable but not proven
backtest: 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising_1h
idea tested: 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3718 USD
---
## Findings
- **F1:** Half of the book's summed bar gain comes from the market's own rise. Of a total gain of 16.51, 8.25 is the position held times each coin's mean hourly return and only 8.26 is timing. On daily returns the book has a beta of 0.23 to holding the coins and a correlation of 0.61 with it, and its mean daily return of 0.000706 is below holding's 0.001179.
- **F2:** The timing part is concentrated in one period and is not stable. 2020 alone gives 4.27 of the 8.26 timing gain, 2024 adds 2.54, and timing is negative in 2022 (-0.76) and 2025 (-0.73). Timing is also negative in 7 of 24 windows (w9 -1.26, w2 -0.83, w22 -0.79).
- **F3:** The gain rests on a few trades and on the coins other than LTC. The top 5% of the 2,192 trades carry 4,150 of the 5,720 summed net percent, which is 73%, and the win rate is only 0.56. LTC's timing gain is negative (-0.40), while XRP (2.54), ZEC (2.14) and ETH (2.03) carry most of it.
- **F4:** The tested grind measure adds little beyond the rise itself at any horizon. On rising grid bars the forecast's t is 0.20 at 24h (n=8,529), 1.52 at 72h (n=2,865) and 0.83 at 168h (n=1,156). The forecast is zero on about 67% of rising cases.
- **F5:** A different grind measure does carry the effect over all moves. Using the share of the past 72 hours that closed up, the next-72h excess return by quintile is -0.0025, -0.0037, -0.0026, +0.0002 and +0.0088. The top quintile's t is 2.80 (n=849 non-overlapping cases), so continuation shows where many hours step up.
- **F6:** The grind effect of the tested measure appears only when the coin's 30-day return is positive. There the forecast's t is 1.49 (n=1,321, mean excess +0.0035), against -0.09 when the 30-day return is negative (n=884). The largest 72h rises also continue: the top quintile of past 72h return gives +0.0060 excess, t=1.82.

## Ideas
- `016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising.e1_share-of-up-hours-continuation` (from F5, F4): The larger the share of a coin's hourly bars over the past 3 days that closed higher, the more the coin rises over the next 3 days.
- `016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising.e2_grind-continuation-in-uptrends` (from F6, F2): When a coin's 30-day return is positive, the smaller the share of its 3-day rise that came from its 3 biggest hourly gains, the more it rises over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
