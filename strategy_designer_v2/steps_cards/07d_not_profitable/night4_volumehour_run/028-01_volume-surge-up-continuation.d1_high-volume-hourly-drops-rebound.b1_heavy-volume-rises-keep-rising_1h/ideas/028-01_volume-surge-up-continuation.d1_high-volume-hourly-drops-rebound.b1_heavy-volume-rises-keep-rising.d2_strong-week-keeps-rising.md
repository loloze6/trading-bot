---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-01_volume-surge-up-continuation.d1_high-volume-hourly-drops-rebound.b1_heavy-volume-rises-keep-rising
line: 7.d not profitable
backtest: 028-01_volume-surge-up-continuation.d1_high-volume-hourly-drops-rebound.b1_heavy-volume-rises-keep-rising_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 7-day return against its hourly volatility over those 7 days, the more the coin rises over the next 24 hours.
Consequence: A trader would lean long a coin in proportion to the strength of its past week's rise, and stand aside when the week was weak, which is when the tested book lost most.
Why:
- F4: The effect sits only in cases where the coin's 7-day return is large against its hourly volatility. In that top fifth (n 664) the unusual 24-hour move is +0.53 % (t 3.25, strength 0.13, 4.8 times the cost). The other four fifths are between −0.14 % and +0.06 % (all t < 0.5 in absolute value or negative).
- F5: The same holds on the raw 7-day return and on each coin separately.
- F6: The Calmar fails because the book stays long through falling markets.
