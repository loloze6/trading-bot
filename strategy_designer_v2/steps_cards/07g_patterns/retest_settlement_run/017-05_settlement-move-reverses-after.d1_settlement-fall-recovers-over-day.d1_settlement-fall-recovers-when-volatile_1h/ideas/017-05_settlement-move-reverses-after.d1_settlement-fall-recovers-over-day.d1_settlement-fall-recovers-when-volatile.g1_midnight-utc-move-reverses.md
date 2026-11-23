---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d1_settlement-fall-recovers-when-volatile
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d1_settlement-fall-recovers-when-volatile_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The deeper a coin's fall over the 3 hours into the 01:00 UTC close, measured against its usual 3-hour move, the more it rises over the next 24 hours; the larger its rise over those 3 hours, the more it lags over the next 24 hours.
Consequence: A sharp fall across the UTC midnight is a reason to be long for the next day, sized by the fall, and a sharp rise across it is a reason to refuse a long.
Why:
- F1: The reversal after a settlement-time move is concentrated around 00:00 UTC and is absent at 16:00. The slope of the excess 24-hour return on the 2-hour fall, one case per day for each close hour, has t 5.2, 8.1 and 5.8 at close hours 0, 1 and 2, but only t 0.5 at hour 16, and stays within |t| 3.2 at every other hour.
- F2: At the 01:00 UTC close, the 3-hour move since 22:00 sorts the next 24 hours in a graded way. The deepest-fall decile gains +0.77 % in excess return (t 5.4, n 1653), the next +0.51 % (t 4.2), and the top-rise decile loses -0.42 % (t -3.2). The slope is positive in all six coins (t 2.3 to 5.9) and in 7 of 8 years; 2022 is the exception (t -0.2).
- F3: The tested book's forecast pays only at its extreme. Cases with forecast above 5 earn +0.15 % excess over 24 hours (t 2.6, n 8297), while the buckets from 1 to 5 are all negative (-0.14 % to -0.17 %). This matches the idea's whole size, an unusual move of +0.09 % per case, which is 0.4 times the 0.19 % cost of a trade.
