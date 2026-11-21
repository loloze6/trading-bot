---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-02_presettle-rise-after-downtrend
line: 7.d not profitable
backtest: 017-02_presettle-rise-after-downtrend_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: For a coin with a strong 3-day run down, the return over the next 24 hours from 2 hours before each funding settlement time (00:00, 08:00 and 16:00 UTC) is positive, and the stronger the 3-day fall, the larger that rise.
Consequence: Hold a rebound bet after a deep 3-day fall for about a day instead of 2 hours, so that a move several times the round-trip fee pays for each entry.
Why:
- F1: The book loses because of fees, not because the signal is wrong. Before fees it earns almost nothing: the gross per coin-day ranges from -0.000245 (XRP) to +0.000458 (XMR), and most coins sit near 0. Fees cost 0.0014–0.0018 per coin-day. The daily book returns -0.00148 on average, while holding the coins returns +0.00119 (17381 coin-days).
- F2: Each pre-settlement trade is a round trip lasting about 2.5 hours. There are about 4900–5300 per coin, and each pays about 0.10 % in fees (for BTC, mean gross 0.038 % against mean net -0.062 %). The pooled mean gross trade return is indistinguishable from zero (t = -0.51).
- F3: The 2-hour move the forecast bets on is far smaller than that fee. In the deepest-fall forecast quintile (forecast about 19.3, 3-day change -9.4 %) the 2-hour return is only +0.050 % (t = 1.87, 5114 cases), and the lower quintiles range from -0.006 % to +0.029 %. This matches the verdict's slope t of 1.30 and mean-excess t of 0.36.
- F4: The same deepest-fall quintile rises more over the following 24 hours, by +0.198 % (t = 2.62 on overlapping episodes). Over the following 6 hours it gives back -0.026 %. Any rebound after a deep 3-day fall therefore sits on a horizon of about a day, not in the 2 pre-settlement hours.
