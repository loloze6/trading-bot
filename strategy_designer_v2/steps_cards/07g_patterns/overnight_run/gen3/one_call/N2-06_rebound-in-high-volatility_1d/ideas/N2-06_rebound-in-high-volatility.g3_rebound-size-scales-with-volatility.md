---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-06_rebound-in-high-volatility
line: 7.g patterns
backtest: N2-06_rebound-in-high-volatility_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a large one-day drop, the next-day rebound in a coin is larger in size when its recent volatility is high in its own history, even though rebounds are no more frequent.
Consequence: A trader would size rebound longs up in high-volatility periods rather than take more of them.
Why:
- F5: The volatility regime changes the size of the rebound but not its frequency, which is the step 5 result (z=0.10). Bars closing near their low are followed by +0.86% in high-volatility bars (t=3.00, n=419) against +0.10% in quiet bars (t=0.48, n=516), while the up shares are about the same (56.6% vs 57.0%). The most extreme drops (z<−3) are followed by +3.7% in high volatility (t=2.32, n=48) against −0.09% in quiet bars (n=31).
