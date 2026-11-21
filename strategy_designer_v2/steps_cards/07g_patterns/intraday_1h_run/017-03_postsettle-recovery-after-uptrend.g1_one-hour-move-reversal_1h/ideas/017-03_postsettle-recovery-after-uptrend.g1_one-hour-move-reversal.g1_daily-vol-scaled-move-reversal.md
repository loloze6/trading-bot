---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-03_postsettle-recovery-after-uptrend.g1_one-hour-move-reversal
line: 7.g patterns
backtest: 017-03_postsettle-recovery-after-uptrend.g1_one-hour-move-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's return over the next 1 day runs against its own 1-day return measured in units of its recent hourly volatility, and the sharper that move, the larger the reversal. The effect is strong when the coin's 30-day volatility is high and larger after falls than after rises.
Consequence: Fade sharp daily moves, especially sharp daily drops, in volatile periods, at a daily pace that the fees can bear, rather than fading every hour.
Why:
- F1: The fade's gross edge is real but fees swamp it: the book's mean daily gain before fees is 19.3 bp (t 11.0, 17,525 coin-days), fees average 156 bp per day, and turnover runs about 14.6 times the book per day, which explains the -16.35 Sharpe.
- F2: Over a 1-day horizon the reversal is much larger per trade and sits in high volatility. On the non-overlapping 24h grid, the vol-scaled graded fade earns 19.3 bp per case (t 4.44, n 16,526). In the coin's upper half of 720-hour volatility it earns 37.2 bp (t 4.65, n 6,465), against -4.2 bp (t -0.78) in the lower half. 68% of the 144 coin-windows are positive.
- F3: The 1-day reversal is lopsided toward falls. After the lowest quintile of vol-scaled 24h returns, the next 24h beats the coin's mean by 40.6 bp (t 4.17, n 3,312). After the highest quintile it trails by 19.8 bp (t -2.25), and the middle quintiles are not significant.
- F5: The 1h reversal grows steadily with 720-hour volatility quartile: 0.89, 1.06, 2.19 and 3.24 bp per bar, with t from 3.7 to 6.4 and about 78k bars each.
