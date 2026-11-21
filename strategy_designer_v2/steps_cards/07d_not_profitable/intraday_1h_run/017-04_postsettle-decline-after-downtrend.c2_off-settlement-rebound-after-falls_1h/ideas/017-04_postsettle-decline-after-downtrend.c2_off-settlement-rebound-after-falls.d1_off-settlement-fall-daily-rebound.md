---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-04_postsettle-decline-after-downtrend.c2_off-settlement-rebound-after-falls
line: 7.d not profitable
backtest: 017-04_postsettle-decline-after-downtrend.c2_off-settlement-rebound-after-falls_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: For a coin with a strong 3-day run down, the return over the next 24 hours from closes away from the funding settlement times is positive, and the deeper the 3-day fall, the larger that rebound.
Consequence: A trader should hold a deep-fall rebound through the next day instead of closing it at each settlement hour, so that one fee pays for a move several times larger.
Why:
- F1: The book loses because fees are about five times what the positions earn: its mean gross gain is 0.000016 per bar against a fee of 0.000077 per bar (net about -0.00006 per bar in every coin, from -0.000054 in XRP to -0.000072 in LTC), so its mean daily return is about -0.0015 (-0.00132 to -0.00174 by coin) while holding the coins gains +0.0007 to +0.0016 a day.
- F2: The fees come from the clock gate rather than the signal: turnover is about 0.23 of the book at hours 1, 5, 9, 13, 17 and 21, when the 4-hour off-settlement gate opens and shuts. Each of those hours costs about 0.00025 in fees, while the gross gain in the open hours ranges from -0.00007 to +0.00019. Every holding is opened and closed within a 4-hour block, at a fee of 0.00108 per unit traded.
- F3: The 2-hour rebound is real but too small for a round trip of that cost. On the 50,986 active grid cases the excess 2-hour return rises from -0.000095 in the lowest forecast quintile to +0.000793 in the top one. Trades gain 0.117% gross but only 0.017% net, with a median length of 3 hours, and only 48.8% of trades are positive after fees against 54.2% before.
- F5: Starting from off-settlement closes, the 24-hour excess return after falls of 1.5 to 2 standard deviations is +0.0072 (n 405) and after deeper falls +0.0031 (n 352), while shallow falls give -0.0012 to -0.0033. The rebound at 48 hours is gone (top-quintile t 0.65, weighted t 0.16), so it plays out within about a day.
