---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-03_postsettle-recovery-after-uptrend.g1_one-hour-move-reversal
line: 7.g patterns
backtest: 017-03_postsettle-recovery-after-uptrend.g1_one-hour-move-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's return over the next 1 hour runs against its last-hour return, and the reversal is larger the higher that hour's volume is relative to the coin's median hourly volume over the past 7 days.
Consequence: Treat heavy-volume sharp hours as the ones worth fading, and quiet-hour moves as not worth the fee.
Why:
- F1: The fade's gross edge is real but fees swamp it: the book's mean daily gain before fees is 19.3 bp (t 11.0, 17,525 coin-days), fees average 156 bp per day, and turnover runs about 14.6 times the book per day, which explains the -16.35 Sharpe.
- F6: The 1h reversal also grows with the bar's volume relative to its last-week median. It is 3.14 bp (t 6.33) in the top quintile against 1.32 to 1.53 bp in the other four (t about 4 to 4.8).
