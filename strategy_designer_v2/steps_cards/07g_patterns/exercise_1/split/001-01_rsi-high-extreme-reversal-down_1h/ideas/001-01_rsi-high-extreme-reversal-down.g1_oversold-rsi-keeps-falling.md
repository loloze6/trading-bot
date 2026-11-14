---
brief: 001_rsi-extremes-predict-next-move
source-idea: 001-01_rsi-high-extreme-reversal-down
line: 7.g patterns
backtest: 001-01_rsi-high-extreme-reversal-down_1h
instruments: BTC, ETH, BNB
bar: 1h
period: fold A
---
Idea: When a coin's 14-bar RSI sits in its most extreme low readings, far below 50 after a one-sided fall, the coin keeps falling over the next 12 hours more than its usual drift.
Consequence: A trader would short a coin, or refuse to buy it, when its hourly RSI is at a low extreme, instead of fading the fall.
Why:
- F4: The extreme bars that follow a fall continue down, on the side the idea never trades. In the top decile of 50-RSI (RSI far below 50, raw mean 8.6), the 12-bar excess return is -24.0 bp pooled (non-overlapping t -2.0), with -20.3 bp for BTC and -27.7 bp for ETH. The opposite decile (RSI far above 50) shows +10.4 bp (+8.3 / +12.4 bp).
- F7: The book is flat when the coin drifts down and short when it rises. On flat bars the coin returns -1.37 bp next bar and -8.9 bp of 12-bar excess. Moderate shorts (allocation -0.5 to -0.1, 5,691 bars) sit before +18.0 bp of 12-bar excess. The largest shorts (< -0.95, 250 bars) sit before -20.8 bp, but pay 4.6 bp per bar in fees.
