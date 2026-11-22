---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue
line: 7.d not profitable
backtest: 026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Over Monday and Tuesday, a coin keeps moving in its weekend's direction (Saturday 00:00 to Monday 00:00 UTC). The more volatile the weekend's hours were compared with the coin's previous week, the larger that continuation.
Consequence: After a turbulent weekend a trader may follow the weekend's direction for two days, long after a rise as well as short after a fall, and should not fade it.
Why:
- F1: The book earns almost nothing against simply holding the coins. Its mean daily return is 5.2e-05 against about 0.0007–0.0016 for holding each coin, for example BTC 0.00118 and ZEC 0.00155. Its Sharpe is 0.20 against holding's 0.55. In the rising windows it lags far behind holding: w11 book −0.00082 a day against holding +0.01256, and w16 −0.00067 against +0.00454.
- F4: The weekend's volatility against the prior week is what carries the continuation.
- F5: The same turbulence effect appears after weekend rises.
- F6: The result rests on a few windows.
