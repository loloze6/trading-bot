---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b2_large-hourly-rise-continues-daylong
line: 7.d not profitable
backtest: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b2_large-hourly-rise-continues-daylong_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin rises far more than its typical hourly move over the past 30 days, on volume above its average hourly volume over the past 30 days, the price keeps rising over the next 24 hours, only while the coin's 7-day return is positive. The higher that 7-day return and the larger that hour's rise in typical 30-day hourly moves, the larger the further rise.
Consequence: A trader would buy surging-volume rising hours only when the coin is already up over the past week, leaning more as the week's gain grows, and stay out of them inside a falling week.
Why:
- F1: The book is close to holding the coin with leverage, and that is why it fails the Calmar test. Its daily returns correlate 0.85 with the coin's. Its mean allocation is 0.80, and it is long on 76–85 % of bars. Its 6334 long trades last 55 hours on average against a 24-bar hold. Its deepest fall of −67.8 % against a yearly return of 33.4 % gives a Calmar of 0.49, below the 0.75 required.
- F2: Each of the book's eight deepest falls is a fall of the coin, with the book still long throughout:
- F3: Over the cases, the move follows the coin's 7-day return. The two lowest quintiles of 7-day return have an excess of −0.01 % and −0.06 % (838 and 837 cases, t −0.07 and −0.49). The two highest have +0.21 % and +0.25 % (t 1.75 and 1.66). That is more than twice the +0.09 % of all 4454 cases (t 1.49).
