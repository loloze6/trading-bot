---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-04_postsettle-decline-after-downtrend.g1_us-open-rebound-after-falls
line: 7.g patterns
backtest: 017-04_postsettle-decline-after-downtrend.g1_us-open-rebound-after-falls_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: For a coin, the return over the 2 hours from 16:00 UTC follows the direction of its 3-day return, and the larger its 3-day move, the larger that 2-hour move in the same direction.
Consequence: In the late US afternoon a trader could side with a coin's 3-day trend, sized by the trend's size, rather than fade it.
Why:
- F2: From 16:00 UTC the coin continues its 3-day move rather than reversing it. The 2-hour return from the close of the 15:00 bar rises with the signed 72-hour return (pooled slope 0.0105, t = 7.3, n = 17018). It goes from −13.0 bp (t = −3.5) in the lowest quintile of 72-hour return to +20.3 bp (t = 6.4) in the highest. The slope is positive in 5 of 6 coins (t from 2.1 to 6.4; XRP −0.6) and holds from the 16:00 decision too (t = 4.5). It is weak from 2021 to 2024 (t between −0.1 and 1.8).
