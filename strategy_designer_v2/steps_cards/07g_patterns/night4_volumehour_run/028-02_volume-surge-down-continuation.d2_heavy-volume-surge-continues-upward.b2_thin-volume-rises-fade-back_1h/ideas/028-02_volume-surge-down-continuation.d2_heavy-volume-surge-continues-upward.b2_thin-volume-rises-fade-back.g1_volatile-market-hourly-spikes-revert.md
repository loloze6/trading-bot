---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward.b2_thin-volume-rises-fade-back
line: 7.g patterns
backtest: 028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward.b2_thin-volume-rises-fade-back_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's hourly volatility over the past 7 days is high, an hour that moves far more than its typical 30-day hourly move is followed by a move in the opposite direction over the next two to six hours, and the larger the hour's move relative to its typical move, the larger the reversal.
Consequence: In a volatile market, a large hourly move is a reason to lean against it for a few hours rather than follow it.
Why:
- F1: When the coin's past 7-day hourly volatility is in its top fifth, hours that move more than twice their typical 30-day hourly move are followed by moves the other way. Against the hour's direction the unusual return is -0.36 % over 2 hours (t -4.98), -0.30 % over 4 hours (t -2.97) and -0.40 % over 6 hours (t -3.53), on 1093 non-overlapping cases. This is about three times the 0.11 % cost of a trade.
- F2: The reversal in F1 is graded and holds only in high volatility. The slope of the unusual 4-hour return on the hour's scaled move is -0.00072 per typical move in the top volatility fifth (t -4.13, n 6420), against slopes between -0.00006 and +0.00016 (all |t| < 1.4) in the other four fifths. The top-fifth slope is negative in all four coin × half splits: BTC w1-12 t -1.98, BTC w13-24 t -3.29, ETH w1-12 t -1.54, ETH w13-24 t -1.73.
- F3: The reversal in F1 shows on both sides. After large falls in high volatility the unusual 4-hour return against the fall is -0.37 % (t -2.28, n 547). After large rises it is -0.22 % (t -1.92, n 546).
