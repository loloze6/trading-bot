---
brief: 013_anchoring-to-recent-high
source-idea: 013-05_longer-stall-bigger-breakout
line: 7.d not profitable
backtest: 013-05_longer-stall-bigger-breakout_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes above its prior 30-day closing high, the more days of the past 20 days it spent closing just under that high, the larger its return over the next 10 days.
Consequence: Taking the stall-under-the-high setup on a 30-day high instead of a 52-week high keeps the anchoring situation but puts the book in the market several times as often, which is what its daily mean lacks.
Why:
- F1: The book fails on mean daily return, 0.000232 against the 0.0005 floor. The cause is how rarely it is in the market: only 2.64% of all bars are in the trending regime (close above the prior 365-day closing high), and 2.61% of bars hold a position. The share by coin runs from 1.0% (XRPUSD) to 4.9% (BTCUSD).
- F2: When it is in, the situation pays. On the 439 trending bars the coin's next-day return beats its own mean by 0.99% a day (t = 3.27), and the mean allocation there is 0.94. The edge is real but present on too few days to lift the book's daily mean.
- F4: A close above a shorter recent high carries the same follow-through and happens far more often. 7.4% of bars close above their prior 30-day closing high, against 2.6% for the 365-day high. On a non-overlapping 10-bar grid the next-10-bar excess return is +5.39% above the 30-day high (n = 132, t = 2.59) and +4.16% above the 20-day high (n = 163, t = 2.36). In daily excess return it is +0.32% (t = 2.07) for the 30-day high and +0.73% (t = 2.93) for the 60-day high.
