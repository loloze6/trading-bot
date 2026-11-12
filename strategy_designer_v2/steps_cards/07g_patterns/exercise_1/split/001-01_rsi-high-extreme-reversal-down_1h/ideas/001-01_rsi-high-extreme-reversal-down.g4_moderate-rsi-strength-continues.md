---
brief: 001_rsi-extremes-predict-next-move
source-idea: 001-01_rsi-high-extreme-reversal-down
line: 7.g patterns
backtest: 001-01_rsi-high-extreme-reversal-down_1h
instruments: BTC, ETH, BNB
bar: 1h
period: fold A
---
Idea: When a coin's 14-bar RSI is moderately above 50 but not at an extreme, the coin rises over the next 12 hours more than its usual drift.
Consequence: A trader would refuse to short moderately strong RSI readings and could lean long on them.
Why:
- F7: The book is flat when the coin drifts down and short when it rises. On flat bars the coin returns -1.37 bp next bar and -8.9 bp of 12-bar excess. Moderate shorts (allocation -0.5 to -0.1, 5,691 bars) sit before +18.0 bp of 12-bar excess. The largest shorts (< -0.95, 250 bars) sit before -20.8 bp, but pay 4.6 bp per bar in fees.
- F4: The extreme bars that follow a fall continue down, on the side the idea never trades. In the top decile of 50-RSI (RSI far below 50, raw mean 8.6), the 12-bar excess return is -24.0 bp pooled (non-overlapping t -2.0), with -20.3 bp for BTC and -27.7 bp for ETH. The opposite decile (RSI far above 50) shows +10.4 bp (+8.3 / +12.4 bp).
- F9: The book loses in all 12 coin-windows, and worst in the rising windows: BTC loses -86.4 and -61.1 bp/day in w4 and w6 while the coin gains +51.3 and +42.9 bp/day; ETH loses -62.6 and -52.8 bp/day while the coin gains +41.4 and +30.7.
