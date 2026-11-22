---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b2_large-hourly-rise-continues-daylong
line: 7.d not profitable
backtest: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b2_large-hourly-rise-continues-daylong_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin rises far more than its typical hourly move over the past 30 days, on volume above its average hourly volume over the past 30 days, the price keeps rising over the next 24 hours, only while the coin's 30-day return is positive. The higher that 30-day return, the larger the further rise.
Consequence: A trader would keep this long-only continuation trade for months in which the coin has risen, and refuse it through the long declines that make up the book's deepest falls.
Why:
- F1: The book is close to holding the coin with leverage, and that is why it fails the Calmar test. Its daily returns correlate 0.85 with the coin's. Its mean allocation is 0.80, and it is long on 76–85 % of bars. Its 6334 long trades last 55 hours on average against a 24-bar hold. Its deepest fall of −67.8 % against a yearly return of 33.4 % gives a Calmar of 0.49, below the 0.75 required.
- F2: Each of the book's eight deepest falls is a fall of the coin, with the book still long throughout:
- F4: On the book's bars, the same split holds for the coin's 30-day return. The two lowest quintiles of 30-day return earn 0.06 and −0.65 bp per bar, which is +1.8 % and −19.5 % of the book's total gain, while the book is still long on 77 % of their bars. The two highest earn 1.65 and 1.51 bp per bar, carrying 49 % and 45 % of the gain.
