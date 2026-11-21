---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high
line: 7.d not profitable
backtest: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, first reaches several times its 30-day average absolute daily return on the upside, the price keeps rising over the next 5 days by more than the coin's usual 5-day return, only while the close stands near its 30-day high and the coin's 1-year return is positive: the closer the close to its 30-day high and the larger its 1-year return at that hour, the larger the rise.
Consequence: A trader would take near-high surges only inside a coin's year-long uptrend, and refuse them during multi-month bear markets, where the book's deepest fall was made.
Why:
- F1: The Calmar fails because of one long fall. The book's deepest fall is 56.8 % and runs over 1215 days from w1 to w11. Holding the coins lost 43.2 % over the same stretch. Against that fall, the book's yearly return of 32.6 % gives a Calmar of 0.57.
- F2: The book's gain sits almost entirely in the later windows. In w11 to w24 the 1405 cases have an unusual 5-day move of +1.00 %, and the positions' summed hourly gain is 19.0. In w1 to w10 the 983 cases have −0.59 %, and the summed gain is only 1.35, even though exposure there is higher (0.65 against 0.56) while the coins' summed log return is −5.76.
- F3: The cases lose in the coins' bear years. The unusual move is −1.02 % in 2018 (285 cases) and −1.49 % in 2022 (312 cases). It is +2.74 % in 2020 and +1.18 % in 2021.
- F4: In w1 to w10, surges that come while the 30-day high has risen over the past week are followed by falls. These 206 cases have an unusual move of −1.79 % (t −2.83). Cases with a falling 30-day high in the same windows have +0.54 %.
- F7: A stop would not save the book. After the first 24 hours, the fifth of cases that fell most on their first day (below −2.9 %) still rise +0.73 % over the next 4 days (t 1.4). So the falls come from long bear spans, not from surges that fail at once.
