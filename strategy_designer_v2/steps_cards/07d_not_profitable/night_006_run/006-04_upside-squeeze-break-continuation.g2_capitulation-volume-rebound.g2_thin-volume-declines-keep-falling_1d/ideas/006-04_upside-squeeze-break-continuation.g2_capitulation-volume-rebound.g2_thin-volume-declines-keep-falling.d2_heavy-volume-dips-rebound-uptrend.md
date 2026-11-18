---
brief: 006_range-compression-precedes-expansion
source-idea: 006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound.g2_thin-volume-declines-keep-falling
line: 7.d not profitable
backtest: 006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound.g2_thin-volume-declines-keep-falling_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a coin has fallen over the last 5 days while its 30-day return is positive, the higher its 5-day average volume against its 30-day average, the larger its rebound over the next 3 days.
Consequence: A trader would buy heavy-volume dips inside a rising month rather than stay flat or short through them, recovering the market's rise the book misses.
Why:
- F5: The long side is strongest when a fall comes on heavy volume inside a rising month. The heaviest-volume quintile (ratio > 0.238) gives excess 3-bar return +0.0279 when the 30-day return is up (n=122), against +0.0032 when it is down (n=292).
- F1: The book earns a mean of 0.000173 a day against 0.00119 for holding (Sharpe 0.18 against 0.46), and about half its gross gain goes to fees (0.000362 gross per bar, 0.000187 in fees). Its market part is -0.000076 because it is short on 32% of bars and long on only 19%, and on the 49% of bars where it is flat the coin rises 0.00216 a day.
- F6: The book's falls happen while the coin trends, not because of it. The worst window drawdown is -0.51 (BTC) in a window where holding gained +0.20, and LTC fell -0.31 in a window where holding gained +1.32. Among the 47 windows where holding rose over 20%, the book's mean total is -0.02. The worst 3% of bars are 49% short.
