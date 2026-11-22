---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b1_volume-surge-rise-more-coins
line: 7.g patterns
backtest: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b1_volume-surge-rise-more-coins_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The more a coin has fallen over its past 24 hours, measured in its usual 24-hour moves over the past 30 days, the more it rises over the next 24 hours; the more it has risen, the more it falls.
Consequence: A trader would buy a coin after a large 24-hour fall and hold it for a day, sized by the depth of the fall, and refuse to chase a coin that has just risen sharply over a day.
Why:
- F2: A coin's 24-hour move reverses over the next 24 hours, and more so the larger it was: the unusual 24-hour move, in usual moves, falls by 0.039 for each usual move of the past 24 hours (t -4.5, 15086 non-overlapping cases); the slope is negative in all six coins (t from -0.76 for BTC to -3.58 for XMR) and in 7 of 8 years.
- F3: The reversal in F2 sits mostly after falls: the decile with the largest 24-hour fall is followed by +0.83 % above drift over 24 hours (t 5.05, 1509 cases), and the decile with the largest rise by -0.31 % (t -2.24); the bottom quintile is positive in every coin (+0.31 % BTC to +0.78 % XRP); a 72-hour past move predicts nothing (slope +0.007, t 0.75).
- F1: The tested idea finds nothing in the bars: its 14681 cases end 24 hours later +0.01 % above drift (t 0.21), its top half does worse than its bottom half (-0.002 %), and the hours it bets on most (a rise of more than 4 usual moves on more than 4 times the usual volume) are followed by -0.15 % over 2 hours (t -0.98, 459 cases) and -0.65 % over 24 hours (t -0.56, 43 cases).
