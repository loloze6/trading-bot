---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high.b2_surge-in-rising-month
line: 7.d not profitable
backtest: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high.b2_surge-in-rising-month_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, first reaches several times its 30-day average absolute daily return on the upside, the price keeps rising over the next 10 days by more than the coin's usual 10-day return, only while the coin's 30-day return is positive: the smaller that 30-day return is in units of the coin's 30-day volatility, the larger the rise.
Consequence: A trader would hold surges that begin a rising month and refuse those that come after a month already far extended, which gave little of the move and took part in the shared falls.
Why:
- F6: An overextended month carries little of the move. By the 30-day return in units of 30-day volatility, the 10-day return falls from +5.9 % in quintile 2 through +3.4 % and +1.1 % to +0.3 % in the top quintile (about 147 trades each). The weakest-month quintile also shows only +0.3 %.
- F1: The check fails on Calmar (0.62 against 0.75) because of shared, deep falls. The book's deepest fall is 57 % over 80 days, from w16 to w17, while the coins' daily returns summed to −41 %. Five more falls run from 34 % to 54 % (w12–w14 −54 %, w6–w10 −42 %, w1–w3 −40 %). Every window's own deepest fall is 14 % to 51 %.
- F2: The falls come from the book being long on many coins while they fall together. On days with all 6 coins long (1430 days) the book's daily standard deviation is 3.7 % and its worst day is −18 %; with 5 coins long the worst day is −22 %; with 1 to 3 coins long the worst day is −2.6 % to −5.2 %. Inside falls deeper than 20 % the coins averaged −0.20 % a day and the book −0.12 % a day, with 4.0 coins long on average.
