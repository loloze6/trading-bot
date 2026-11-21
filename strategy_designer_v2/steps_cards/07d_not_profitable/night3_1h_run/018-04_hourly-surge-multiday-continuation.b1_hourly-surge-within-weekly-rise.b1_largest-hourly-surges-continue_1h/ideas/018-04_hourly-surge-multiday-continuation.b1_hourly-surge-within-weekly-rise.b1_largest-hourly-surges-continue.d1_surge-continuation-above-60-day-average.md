---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-04_hourly-surge-multiday-continuation.b1_hourly-surge-within-weekly-rise.b1_largest-hourly-surges-continue
line: 7.d not profitable
backtest: 018-04_hourly-surge-multiday-continuation.b1_hourly-surge-within-weekly-rise.b1_largest-hourly-surges-continue_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, first reaches several times its 30-day average absolute daily return on the upside, the price keeps rising over the next 5 days by more than the coin's usual 5-day return, only while its price is above its 60-day average price. The larger that 24-hour return against its 30-day average absolute daily return, the larger the rise, and the rise keeps growing for surges well beyond twice the usual daily move.
Consequence: A trader buys exceptional up surges only in coins trading above their 60-day average, sizes larger for the largest ones, and stays out of surges in coins below that average, where the book took its deepest falls.
Why:
- F1: The Calmar fails because one fall dominates: the chained daily book returns a yearly 35.2 % against a deepest fall of 58.5 %, which took 271 days to reach its trough across w1 to w3 while holding the coins fell 62.4 % over the same days; the next four falls (30 to 38 %) also came while holding fell 30 to 79 %.
- F3: The book loses its falls on coin-days when the coin is below its 60-day average price: in the two lowest quintiles of distance to that average the book still held 0.24 and 0.43 of its value and lost 0.39 % and 0.32 % per coin-day, against +0.19 % and +1.27 % per day in the two highest quintiles (allocation 0.84 and 0.87).
- F4: Only the largest surges carry a move: cases whose 24-hour return exceeds 1.88 times its 30-day mean absolute value earn +1.97 % above the 5-day drift (t 3.23, 455 cases), while the four lower quintiles earn between -0.54 % and +0.17 % (455 to 454 cases each); the forecast is capped at twice the usual move and so sizes these surges no larger than ones that carry nothing.
- F5: Measured over all its cases, the idea's unusual move is +0.12 % per case against a round-trip cost of 0.19 % (0.6 times the cost), whereas the top-surge quintile's +1.97 % is about 10 times the cost.
- F7: Below the 60-day average, ordinary surges lose and only the largest pay: by tercile of surge size, cases below that average earn -0.61 %, -0.67 % and +1.01 % (t 1.79), and cases above it earn -0.35 %, +0.72 % and +0.98 % (376 to 415 cases per cell).
