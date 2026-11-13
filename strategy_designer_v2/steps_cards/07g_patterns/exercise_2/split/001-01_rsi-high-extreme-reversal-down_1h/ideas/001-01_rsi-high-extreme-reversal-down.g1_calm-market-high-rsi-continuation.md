---
brief: 001_rsi-extremes-predict-next-move
source-idea: 001-01_rsi-high-extreme-reversal-down
line: 7.g patterns
backtest: 001-01_rsi-high-extreme-reversal-down_1h
instruments: BTC, ETH, BNB
bar: 1h
period: fold A
---
Idea: When a coin's 24-hour volatility is in its lowest third and its 14-hour RSI sits at a high extreme, the price keeps rising over the next 12 hours by more than its usual drift.
Consequence: A trader should refuse high-RSI shorts in calm markets, and could treat a high reading there as a reason to lean long.
Why:
- F6: The extreme-RSI reading behaves differently depending on volatility (non-overlapping 12-bar blocks). In the lowest 24h-volatility tercile, extreme bars are followed by an excess +0.28% (t=1.96, n=157), which is continuation. In the middle tercile they are followed by -0.19% (t=-1.27, n=215), and in the high tercile by -0.14% (t=-0.77, n=226).
- F9: The book loses more as volatility rises. Mean absolute allocation goes from 0.42 in the lowest 24h-volatility quintile to 0.53 in the highest, and the book's mean hourly return worsens from -1.1 bp to -2.5 bp.
