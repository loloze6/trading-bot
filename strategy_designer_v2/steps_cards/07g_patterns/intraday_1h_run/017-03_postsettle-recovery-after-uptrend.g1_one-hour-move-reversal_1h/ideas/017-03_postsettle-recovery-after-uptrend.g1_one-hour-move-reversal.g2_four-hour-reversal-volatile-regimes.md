---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-03_postsettle-recovery-after-uptrend.g1_one-hour-move-reversal
line: 7.g patterns
backtest: 017-03_postsettle-recovery-after-uptrend.g1_one-hour-move-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's return over the next 4 hours runs against its own 4-hour return measured in units of its recent hourly volatility, and the reversal grows with the size of that move when the coin's 30-day volatility is high.
Consequence: In volatile regimes, fade sharp 4-hour moves rather than chase them, and expect little from it in calm regimes.
Why:
- F1: The fade's gross edge is real but fees swamp it: the book's mean daily gain before fees is 19.3 bp (t 11.0, 17,525 coin-days), fees average 156 bp per day, and turnover runs about 14.6 times the book per day, which explains the -16.35 Sharpe.
- F4: The same pattern holds on the 4h grid. The graded fade earns 4.9 bp (t 3.48) in the high-volatility half against 0.7 bp (t 0.70) in the low half. After the lowest quintile of 4h moves the next 4h gains 7.1 bp (t 4.22), after the highest it loses 5.7 bp (t -3.75). The effect is carried by XMR (t 4.22), ZEC (t 3.55) and XRP (t 2.35), with BTC and ETH near zero (t 0.30 and 0.19).
- F5: The 1h reversal grows steadily with 720-hour volatility quartile: 0.89, 1.06, 2.19 and 3.24 bp per bar, with t from 3.7 to 6.4 and about 78k bars each.
