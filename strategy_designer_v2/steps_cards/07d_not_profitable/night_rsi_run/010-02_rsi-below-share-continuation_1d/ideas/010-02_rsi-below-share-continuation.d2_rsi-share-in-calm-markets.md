---
brief: 010_rsi-midline-regime-direction
source-idea: 010-02_rsi-below-share-continuation
line: 7.d not profitable
backtest: 010-02_rsi-below-share-continuation_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: The larger the share of the past 30 days that a coin's 14-day RSI has spent below its midpoint of 50, the lower the coin's return over the next 14 days, and the more so the lower the coin's 30-day realised volatility.
Consequence: Lean harder on the RSI-share signal in calm markets and less in turbulent ones, where its short side has lost money.
Why:
- F2: The short side carries almost none of the book's gain: short coin-days earn a mean of 0.000189 per day (n=2866) against 0.001857 for long coin-days (n=2793), with similar spread (std 0.0245 against 0.0270).
- F4: Shorts held in the highest third of the coin's 30-day realised volatility lose 0.00028 per day (n=866) and earn 0.00097 in the lowest third (n=622); longs earn 0.00295 per day in the lowest-volatility third (n=799) against 0.00092 in the highest (n=549), so the signal pays most in calm markets.
