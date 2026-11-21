---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b3_plunge-continuation-in-downtrends
line: 7.d not profitable
backtest: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b3_plunge-continuation-in-downtrends_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return falls by a large multiple of its 30-day average absolute daily return while its 30-day return is negative, the price falls further over the next 4 days by more than the coin's usual 4-day drift, only while the 30-day fall is shallow, and the larger the 24-hour fall against its usual size, the larger the further decline.
Consequence: A trader would short a sharp plunge only in a coin in a mild monthly decline, and would refuse that short once the month's fall is deep.
Why:
- F2: The move the book bets on is the wrong way and smaller than a trade's cost. Over 2265 cases, the short-direction total move is -0.20 % at 4 days (t -0.99) and -0.39 % at 8 days, against a round trip of 0.19 %. The unusual move is +0.31 % only because the coins' normal drift is up.
- F3: The tested depth relation is reversed. In the deepest quintile of 30-day returns (-67 % to -27 %), short cases lose -1.71 % over 4 days (t -2.60, 318 cases) and -3.5 % over 8 days. The middle quintile (-16 % to -8 %) gains +1.10 % short (t 2.51, 317 cases).
- F4: Plunges of at least 1.5 usual daily moves, taken on price alone with one per 4-day cell, continue down only in mild 30-day falls. With the 30-day return between -22 % and -1 %, the unusual 4-day move is -0.93 % (t -1.89) and -0.92 % (t -2.14), 341 cases each, about 0.10 of a usual move. That makes a short-side total of about +0.42 %, about 2.2 times the cost.
