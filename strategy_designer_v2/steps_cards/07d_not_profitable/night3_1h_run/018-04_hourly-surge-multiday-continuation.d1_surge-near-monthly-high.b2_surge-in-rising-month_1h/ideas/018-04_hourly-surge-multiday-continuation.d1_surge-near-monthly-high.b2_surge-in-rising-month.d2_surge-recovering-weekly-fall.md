---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high.b2_surge-in-rising-month
line: 7.d not profitable
backtest: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high.b2_surge-in-rising-month_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, first reaches several times its 30-day average absolute daily return on the upside, the price keeps rising over the next 10 days by more than the coin's usual 10-day return, only while the coin's 30-day return is positive: the more the coin fell over the preceding 7 days, the larger the rise.
Consequence: A trader would favour surges that recover a down week inside a rising month and size down surges that extend an already rising week.
Why:
- F5: Surges that repair a falling week continue most. Trades entered with a negative 7-day return (−20 % to −0.65 %) returned +6.4 % over 10 days (215 trades). The other four 7-day-return quintiles returned −0.7 % to +3.1 %.
- F1: The check fails on Calmar (0.62 against 0.75) because of shared, deep falls. The book's deepest fall is 57 % over 80 days, from w16 to w17, while the coins' daily returns summed to −41 %. Five more falls run from 34 % to 54 % (w12–w14 −54 %, w6–w10 −42 %, w1–w3 −40 %). Every window's own deepest fall is 14 % to 51 %.
- F3: A stop would not help. The first 48 hours of a trade say nothing about the rest of its 10 days: the Spearman correlation of the 48-hour return with the following 8 days is 0.03 (p 0.25, 1474 trades). So the losses are not a fall that keeps going.
