---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-03_postsettle-recovery-after-uptrend
line: 7.g patterns
backtest: 017-03_postsettle-recovery-after-uptrend_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's return over the next 1 hour runs against its own last-hour return, and the larger that move relative to the coin's recent hourly volatility, the larger the reversal. The reversal is strongest when the coin's 30-day volatility is high.
Consequence: Fade sharp single-hour moves, sized up in volatile periods, and refuse to chase them.
Why:
- F1: Over the hour after each bar's close, returns run against that bar's own move in every coin and almost every year. The slope of the excess 1-hour return on the volatility-scaled last-hour move is negative for BTC (-1.15 bp per z, t -3.6), ETH (t -2.9), LTC (t -6.7), XMR (t -6.7), XRP (t -5.9) and ZEC (-4.43 bp per z, t -7.6), each with about 50,000 bars; 2022 is the only year with a positive slope (t +2.3).
- F2: The 1-hour reversal grows with the size of the move and with the volatility level. The lowest decile of last-hour return is followed by +7.2 bp excess (t 8.9) and the highest by -2.6 bp (t -3.4). In the highest volatility tercile, bars with a move below -2 z are followed by +27.1 bp, against +4.2 bp in the lowest volatility tercile.
