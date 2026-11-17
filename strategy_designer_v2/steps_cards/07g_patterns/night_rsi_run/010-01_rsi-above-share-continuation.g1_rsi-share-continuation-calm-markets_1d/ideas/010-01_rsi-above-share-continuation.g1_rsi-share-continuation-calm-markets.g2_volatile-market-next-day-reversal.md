---
brief: 010_rsi-midline-regime-direction
source-idea: 010-01_rsi-above-share-continuation.g1_rsi-share-continuation-calm-markets
line: 7.g patterns
backtest: 010-01_rsi-above-share-continuation.g1_rsi-share-continuation-calm-markets_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 30-day volatility is high relative to its own recent history, the larger its last day's return measured against its 30-day volatility, the lower its return over the next 1 day.
Consequence: In volatile markets, lean against yesterday's move in proportion to its size, and refuse to chase large daily moves.
Why:
- F3: In the high-volatility regime, a coin's daily move scaled by its 30-day volatility reverses the next day. The bottom quintile of moves is followed by +0.63% (t 2.62, n 456) and the top quintile by -0.37% (t -2.14, n 472), falling steadily across the quintiles. In the calm regime the quintiles show no order (t -0.24 to 0.49), and pooled over all bars the slope t is -3.21 on 4834 one-day cases.
