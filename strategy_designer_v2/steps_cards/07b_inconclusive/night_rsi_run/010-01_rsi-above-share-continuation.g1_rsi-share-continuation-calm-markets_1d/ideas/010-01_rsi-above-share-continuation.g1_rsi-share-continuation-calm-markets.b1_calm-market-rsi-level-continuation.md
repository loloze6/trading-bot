---
brief: 010_rsi-midline-regime-direction
source-idea: 010-01_rsi-above-share-continuation.g1_rsi-share-continuation-calm-markets
line: 7.b inconclusive
backtest: 010-01_rsi-above-share-continuation.g1_rsi-share-continuation-calm-markets_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's 14-day RSI at the close, the higher its return over the next 7 days, while the coin's 30-day volatility of daily returns is low relative to its own history.
Consequence: In calm markets, lean with the current RSI reading over the coming week rather than with how long RSI has sat above its midpoint, and give it little weight when volatility is high.
Why:
- F5: The RSI level itself, not the share of days above 50, carries the only clear sign, and only in the calm regime. In calm bars the 7-day forward return rises with the 14-day RSI (t 2.52, n=368), compared with t -0.35 (n=351) in high-volatility bars. In calm bars the same slope is t 1.04 at 14 days and t 1.67 at 30 days. The coin's 30-day return points the same way at 7 days in calm bars (t 1.77, n=303).
- F4: The volatility condition does not bring the effect out. The raw RSI share has a 14-day slope t of 0.43 in the calm regime (n=101) and -0.32 outside it (n=91). By volatility-rank tercile it is 0.57, -1.72 and -0.37, with no gradient.
- F1: The tested slope is essentially zero at the plan's horizon, with a pooled t of 0.004 and a correlation of 0.0003 over 191 non-overlapping 14-day cases. It is also near zero at the neighbouring horizons, with t 0.98 at 7 days (n=414) and t 0.68 at 30 days (n=88).
