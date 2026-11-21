---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d1_volatile-settlement-move-reverses
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d1_volatile-settlement-move-reverses_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The deeper a coin's fall over its past 24 hours, measured against its usual 24-hour move, the larger its rise over the next 24 hours, while its 24-hour volatility is above its 30-day average. Inside that regime, the rebound grows with the depth of the fall and with how high the volatility is.
Consequence: A trader would buy deep 24-hour falls in volatile markets and hold for a day, where the move per case is several times a round trip, and would refuse to fade 24-hour rises.
Why:
- F1: Large 24-hour falls in volatile markets reverse over the next 24 hours, at about six times the cost of a trade. The cases are the largest third of 24-hour falls, in the highest third of 24-hour volatility against its 720-hour mean, with one case per 24-hour grid cell. Their next 24 hours carry an unusual move of +106 bps and a total move of +121 bps, against a cost of 19 bps. The strength is 0.21 of a usual move, with t 6.4 on 1539 cases. In the same high volatility, the middle third of falls gives t 2.0 and +53 bps total, and the smallest third gives t -0.4.
- F2: The F1 rebound holds on every coin and in every year. On each of the 6 coins its strength is 0.09 to 0.32 and its total move is +55 to +204 bps, with t above 2 on 5 coins. In each of the 8 years its strength is 0.06 to 0.58 and its total move is +51 to +314 bps, with t of 2 or more in 4 years and t 1.99 in 2019.
- F3: Among 24-hour falls in high volatility, the deeper the fall, the larger the next 24-hour rebound. The correlation of fall size with the unusual move that follows is 0.106 on about 2600 cases, a t of about 5.4. For 24-hour rises the same correlation is 0.029, and rises give a smaller reversal: the largest third in high volatility gives 0.080, with t 2.85 and +23 bps total.
- F6: The book's losses come from its shorts. 16476 short trades average -0.84 % before fees, against +0.10 % for 16244 longs, and the median short is negative in every one of the 8 years (-0.33 % to -0.86 %). Fading rises into settlement loses, while fading falls breaks about even before fees.
