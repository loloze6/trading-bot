---
brief: 001_rsi-extremes-predict-next-move
source-idea: 001-01_rsi-high-extreme-reversal-down
line: 7.g patterns
backtest: 001-01_rsi-high-extreme-reversal-down_1h
instruments: BTC, ETH, BNB
bar: 1h
period: fold A
---
Idea: When a coin has fallen over the past 12 hours while its 24-hour volatility is low relative to its own recent median, it keeps falling over the next 12 hours more than its usual drift.
Consequence: A trader would short, or refuse to buy, a coin drifting down in a quiet market.
Why:
- F6: Volatility conditions this continuation. When 24h volatility is in its top tercile relative to its own recent median, bars after a 12h rise see +24.9 bp of 12-bar excess return, versus +5.4 bp in the low-volatility tercile. In the low-volatility tercile, falls continue (-16.9 bp). In absolute volatility terms, the top tercile shows +11.6 / +8.8 bp excess for BTC / ETH, against -8.5 / -9.1 bp in the middle tercile.
- F7: The book is flat when the coin drifts down and short when it rises. On flat bars the coin returns -1.37 bp next bar and -8.9 bp of 12-bar excess. Moderate shorts (allocation -0.5 to -0.1, 5,691 bars) sit before +18.0 bp of 12-bar excess. The largest shorts (< -0.95, 250 bars) sit before -20.8 bp, but pay 4.6 bp per bar in fees.
