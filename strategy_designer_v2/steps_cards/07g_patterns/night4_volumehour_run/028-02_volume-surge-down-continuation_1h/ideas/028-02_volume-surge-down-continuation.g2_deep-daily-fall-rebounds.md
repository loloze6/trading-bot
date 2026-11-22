---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-02_volume-surge-down-continuation
line: 7.g patterns
backtest: 028-02_volume-surge-down-continuation_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: After a day in which the coin has fallen far more than its usual daily move, it rises over the next 24 hours more than its normal drift. The deeper the 24-hour fall relative to its 30-day hourly volatility, the larger the rise.
Consequence: A trader would buy, rather than short, a coin after an unusually deep 24-hour fall, holding for about a day.
Why:
- F2: The 24-hour reversal is graded and is largest at the extremes. After the bottom quintile of past-day moves, the next day ends +31 bp (BTC) and +46 bp (ETH) above drift; after the top quintile, -21 bp and -16 bp. After past-day falls beyond 2 units it ends +146 bp (t 2.64, 133 cases). This spread is several times the 0.11 % cost of a trade.
- F4: The tested situation shows no continuation; it leans toward a rebound instead. The 6-hour drift-removed return after hours falling more than 3 standard deviations is -10.8 bp in the idea's short direction terms, a rise of +10.8 bp (t 0.32, 177 cases). On volume above 4 times the average it is +27.6 bp (93 cases). The volume ratio's rank correlation with the outcome is 0.006 over 8416 cases.
- F5: About half the book's loss comes from being short in a rising market. The book is short on 57 % of BTC bars and 59 % of ETH bars. Its hourly gain is -0.50 bp (BTC) and -0.44 bp (ETH), of which -0.26 bp and -0.26 bp is the market's own rise. Its daily mean is positive mainly in windows where the coins fell (w1, w2, w14, w20, w22, w24).
