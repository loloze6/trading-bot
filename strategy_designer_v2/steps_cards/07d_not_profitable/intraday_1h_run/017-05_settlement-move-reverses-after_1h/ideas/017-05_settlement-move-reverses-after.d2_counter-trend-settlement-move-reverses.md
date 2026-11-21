---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after
line: 7.d not profitable
backtest: 017-05_settlement-move-reverses-after_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Over the 2 hours after a funding settlement time, a coin gives back more of its 2-hour pre-settlement move the more that move runs against the coin's own 24-hour return.
Consequence: A trader would fade a pre-settlement move most firmly when it ran against the coin's past-day trend, and least when it extended that trend.
Why:
- F7: A pre-settlement move against the coin's 24-hour trend reverses more over 2 hours: 5.7 bps (t 5.8, n 21,605), against 2.4 bps (t 2.6) when it runs with the trend. In high volatility, though, the moves that run with the trend give back more over 8 hours: 19.3 bps (t 4.7), against 2.5 bps.
- F3: The reversal is real but small and slow. On the 51,888 settlement bars the forecast-signed forward return is 1.8 bps over 1 hour (t 3.6), 3.7 bps over 2 hours (t 5.6) and 5.6 bps over 8 hours (t 4.5). The mean absolute pre-settlement 2-hour move is 94 bps, and the slope of the 8-hour return on that move is only −0.086.
