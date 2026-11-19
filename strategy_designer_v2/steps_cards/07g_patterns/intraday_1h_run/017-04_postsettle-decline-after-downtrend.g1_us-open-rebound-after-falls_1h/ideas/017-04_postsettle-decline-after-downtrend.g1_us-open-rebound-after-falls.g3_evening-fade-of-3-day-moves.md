---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-04_postsettle-decline-after-downtrend.g1_us-open-rebound-after-falls
line: 7.g patterns
backtest: 017-04_postsettle-decline-after-downtrend.g1_us-open-rebound-after-falls_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: For a coin, the return over the 2 hours from 19:00 UTC runs against its 3-day return: the larger its 3-day rise, the lower that return, and the larger its 3-day fall, the higher it is.
Consequence: A second daily fade window could be stacked with the 12:00 rebound, so that each round trip's fee is set against more of the move.
Why:
- F4: Outside the tested 11:00–13:00 hours, there is a second window where the coin runs against its 3-day move. The 2-hour return from the close of the 18:00 bar has slope −0.0094 on the signed 72-hour return (t = −6.9, n ≈ 17000), and from the 19:00 bar the slope is −0.0072 (t = −5.2). This is as strong as the tested hours (t of −7.8 and −9.0 at the 11:00 and 12:00 decisions).
- F1: The tested rebound is real but the fees eat it. Gross position gain is 0.000227 a day and fees are 0.000527 a day, so the book loses 0.00030 a day. Almost all fees are paid on the 11:00 and 13:00 bars, about 2.4 bp each, which is one full round trip every day.
