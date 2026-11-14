---
brief: 001_rsi-extremes-predict-next-move
source-idea: 001-01_rsi-high-extreme-reversal-down
line: 7.g patterns
backtest: 001-01_rsi-high-extreme-reversal-down_1h
instruments: BTC, ETH, BNB
bar: 1h
period: fold A
---
Idea: After a coin's 14-bar RSI rises to a high extreme, the coin gives back part of the move within the next few hours, before any continuation over longer horizons.
Consequence: A trader fading a high RSI reading would hold for only a few hours and would exit before the 12-hour horizon.
Why:
- F2: Trade P&L turns on holding time. Trades shorter than about 4 hours make money: mean duration 1.4 h, gross +0.35%, and mean duration 3.4 h, gross +0.21%. The longest quartile (mean 38.6 h) loses -2.55% gross, so the 60% gross win rate still gives a mean of -0.52% per trade.
- F3: Entry forecast size does not separate trades: |entry forecast| quartiles of 3.9, 8.5 and 17.6 all lose about the same gross (-0.51%, -0.48%, -0.55%, win rates 57–62%), and larger forecasts only shorten the trade (19.9 h vs 8.9 h).
