---
brief: 012_liquidation-flush-partial-rebound
source-idea: 012-02_volume-burst-fall-reversal
line: 7.g patterns
backtest: 012-02_volume-burst-fall-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 5-day return measured in its usual daily moves, the larger its return in the same direction over the next 7 days.
Consequence: A coin that has moved strongly over five days is a reason to trade in the direction of that move for the following week, and a reason to refuse fading it.
Why:
- F2: The coin's 5-day return measured in usual moves (5-day return over the 20-day daily standard deviation times √5) predicts the coin's next 7-day excess return with slope 0.0119 (t 4.23, n 2011 non-overlapping cases), the opposite of reversal; the slope is positive at every horizon from 2 to 14 days (t 2.31 to 4.23) and for all six coins (XRP t 3.28, the others t 0.89 to 1.79).
