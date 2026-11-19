---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-03_postsettle-recovery-after-uptrend.g2_daily-move-reversal
line: 7.d not profitable
backtest: 017-03_postsettle-recovery-after-uptrend.g2_daily-move-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's return over the next 1 day runs against its own 1-day return, and the larger the past day's move relative to the coin's recent volatility, the larger the move back, only while the coin's 7-day volatility is high relative to its own past month, and the higher that volatility the larger the move back.
Consequence: Lean against outsized daily moves only in volatile stretches, when the move back is large enough to pay the fees, and stay out in calm stretches where the reversal is absent.
Why:
- F1: The book makes almost nothing before fees and loses to fees. Its gross gain is 0.000073 a day, while its fees cost 0.00284 a day. Turnover is 2.63 times the book a day, trades last a median of 5 hours, and there are 195,067 trades averaging -0.31% before fees and -0.41% after. So the book's mean daily return is -0.00274 (sd 0.0252, n 17381), against +0.00119 for holding.
- F3: The whole edge sits in high-volatility periods. The 24-hour product is 0.00599 (t 6.61, n 5463) when the coin's 168-hour volatility ranks in the top third of its past 720 hours. It is 0.000037 (t 0.04, n 4232) in the middle third and -0.00066 (t -0.97, n 6255) in the bottom third. So most cases carry no edge but still pay full fees.
- F5: Forecast size alone does not separate the gain enough to beat fees. The product is -0.00009 (t -0.50), 0.00188 (t 3.23) and 0.00362 (t 2.86) across the low, mid and high |forecast| thirds. Days that run against the 7-day trend give 0.0023 (t 4.42) and days with it give 0.0015 (t 2.11), so the trend's direction matters less than its size (F4).
