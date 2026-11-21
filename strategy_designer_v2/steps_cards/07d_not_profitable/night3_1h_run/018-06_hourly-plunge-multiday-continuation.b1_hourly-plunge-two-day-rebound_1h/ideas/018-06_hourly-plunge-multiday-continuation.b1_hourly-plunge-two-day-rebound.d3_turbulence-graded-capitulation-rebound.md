---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound
line: 7.d not profitable
backtest: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: After a coin's 24-hour return falls by a large multiple of its 30-day average absolute daily return, read at an hourly close, the price rises over the next 2 days by more than the coin's usual 2-day drift. The rise is larger the higher the coin's 7-day hourly volatility against its 30-day hourly volatility.
Consequence: A trader takes a 2-day long in a coin only after a plunge in a turbulent week, sized by the turbulence, and is out the rest of the time. This removes most of the drift exposure that carries this book's falls.
Why:
- F1: The book is long on 84 % of all bars (81 % in w12 to w16), so its falls are mostly the coins' own falls. Its deepest fall is -57.8 % over 480 days from w12 to w16, while holding the coins fell -80.5 % over the same stretch. That gives a Calmar of 0.21 and a Sharpe below holding's.
- F2: The rebound after a plunge depends on how violent the coin's last week has been against its last month. The measure is the 7-day to 30-day hourly-volatility ratio at the case bar; 6118 cases over 48 hours.
- F3: The book's gain sits almost entirely in high-ratio bars.
- F4: Outside w12 to w16 the volatility gradient is steep. Mean excess return rises from -0.17 % to -0.30 %, +0.07 %, +0.84 % (t 3.59) and +1.37 % (t 5.20, n 740) across the ratio fifths, and the Spearman of forecast against outcome rises from 0.01 to 0.10.
