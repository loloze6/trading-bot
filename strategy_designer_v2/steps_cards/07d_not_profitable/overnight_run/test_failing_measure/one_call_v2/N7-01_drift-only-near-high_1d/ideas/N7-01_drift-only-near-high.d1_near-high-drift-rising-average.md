---
brief: 002_moving-average-cross-trend-persistence
source-idea: N7-01_drift-only-near-high
line: 7.d not profitable
backtest: N7-01_drift-only-near-high_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a new 20-day closing high, while the close stays near that high and above its 20-day average, the coin rises more than its average over the following days, only while the 20-day average itself has risen over the last few bars.
Consequence: Refuse the near-high long when the 20-day average is flat or falling, which keeps the gain and removes the deepest part of the book's fall.
Why:
- F1: The Calmar failure comes from one fall: the book's deepest drawdown is -67.5%, running 1,160 days from w1 to its trough in w10. Over those 1,162 days the book's mean daily return was -0.00075, against +0.00297 over the remaining 1,736 days. No other fall is deeper than -43.7% (w11 to w13).
- F3: Measured on the book's daily returns, keeping only the days when the 20-day average had risen over the prior 5 bars lifts Calmar from 0.689 to 0.898. It cuts the deepest fall from -67.5% to -48.4%, keeps the Sharpe (0.99 against 0.96) and keeps most of the mean daily return (0.0013 against 0.0015).
