---
line: 7.d not profitable
backtest: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b2_large-hourly-rise-continues-daylong_1h
idea tested: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b2_large-hourly-rise-continues-daylong
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3339 USD
---
## Findings
- **F1:** The book is close to holding the coin with leverage, and that is why it fails the Calmar test. Its daily returns correlate 0.85 with the coin's. Its mean allocation is 0.80, and it is long on 76–85 % of bars. Its 6334 long trades last 55 hours on average against a 24-bar hold. Its deepest fall of −67.8 % against a yearly return of 33.4 % gives a Calmar of 0.49, below the 0.75 required.
- **F2:** Each of the book's eight deepest falls is a fall of the coin, with the book still long throughout:
- **F3:** Over the cases, the move follows the coin's 7-day return. The two lowest quintiles of 7-day return have an excess of −0.01 % and −0.06 % (838 and 837 cases, t −0.07 and −0.49). The two highest have +0.21 % and +0.25 % (t 1.75 and 1.66). That is more than twice the +0.09 % of all 4454 cases (t 1.49).
- **F4:** On the book's bars, the same split holds for the coin's 30-day return. The two lowest quintiles of 30-day return earn 0.06 and −0.65 bp per bar, which is +1.8 % and −19.5 % of the book's total gain, while the book is still long on 77 % of their bars. The two highest earn 1.65 and 1.51 bp per bar, carrying 49 % and 45 % of the gain.
- **F5:** The forecast's size does not grade the move. 60 % of the cases (2672) sit in the forecast's top bin, where the excess is only +0.02 % (t 0.29). The supporting check is +0.0007 %. Overall, the unusual move of +0.09 % per case is 0.9 times the 0.11 % cost of a trade, and the strength is 0.021.
- **F6:** The book's gain is weakest in the middle range of short-term volatility. When 7-day hourly volatility is in the middle quintile of its ratio to 30-day volatility, the book earns −0.02 bp per bar and the cases' excess is −0.34 % (t −2.26). When that ratio is lowest, the cases' excess is +0.39 % (t 2.55), the highest of any quintile.

## Ideas
- `028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b2_large-hourly-rise-continues-daylong.d1_volume-surge-rise-in-uptrend` (from F1, F2, F3): After an hour in which the coin rises far more than its typical hourly move over the past 30 days, on volume above its average hourly volume over the past 30 days, the price keeps rising over the next 24 hours, only while the coin's 7-day return is positive. The higher that 7-day return and the larger that hour's rise in typical 30-day hourly moves, the larger the further rise.
- `028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b2_large-hourly-rise-continues-daylong.d2_surge-continuation-in-monthly-uptrend` (from F1, F2, F4): After an hour in which the coin rises far more than its typical hourly move over the past 30 days, on volume above its average hourly volume over the past 30 days, the price keeps rising over the next 24 hours, only while the coin's 30-day return is positive. The higher that 30-day return, the larger the further rise.
- `028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b2_large-hourly-rise-continues-daylong.d3_surge-breaking-a-calm-week` (from F5, F6): After an hour in which the coin rises far more than its typical hourly move over the past 30 days, on volume above its average hourly volume over the past 30 days, the price keeps rising over the next 24 hours. The rise is larger the quieter the coin's past 7 days have been against its past 30 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
