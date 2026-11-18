---
brief: 006_range-compression-precedes-expansion
source-idea: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise
line: 7.d not profitable
backtest: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's average daily volume over the last 5 days against its 30-day average, the more its price rises over the next 3 days relative to its usual 3-day return, only while the coin's 30-day return is positive.
Consequence: A volume surge is a reason to lean long only in a coin that has risen over the past month; in a coin that has fallen over the month, the surge is no reason to be long.
Why:
- F1: The book's deepest fall, -0.42 on the chained daily book, sits in w14 to w16. Book and holding returns were w14 -0.31 vs -0.49, w15 +0.15 vs +0.06 and w16 +0.02 vs +0.36, with in-window falls of -0.42, -0.39 and -0.34. This fall against a mean daily return of 0.00058 is what sinks Calmar to 0.45.
- F2: The w14 loss came almost entirely from being long while the coin's 30-day return was negative. Those bars summed -1.66 over 326 active bars at a mean allocation of 0.45, against -0.28 over 53 bars when the 30-day return was positive. The pattern is not uniform: in w15 the negative-30-day bars summed +1.48.
- F3: On the 3-day grid, the volume-surge forecast predicts the excess return only when the coin's 30-day return is positive. There the slope t is 3.60 (2187 cases, 997 with forecast > 0) and the forecast-weighted mean excess is 0.0117. When the 30-day return is negative the slope t is 0.90 (2096 cases, 773 with forecast > 0) and the weighted mean excess is 0.0004.
- F4: Across all active bars, the mean daily gain is 0.00192 when the 30-day return is positive (3726 bars) and 0.00089 when it is negative (4927 bars). The book spends most of its time long in the state where its forecast carries no information.
- F5: The one losing state is a negative 30-day return combined with an up last day. It has a mean gain of -0.00134 and a mean next-day coin return of -0.0018 over 2337 active bars. The other three combinations of the two signs gain between 0.0017 and 0.0029.
