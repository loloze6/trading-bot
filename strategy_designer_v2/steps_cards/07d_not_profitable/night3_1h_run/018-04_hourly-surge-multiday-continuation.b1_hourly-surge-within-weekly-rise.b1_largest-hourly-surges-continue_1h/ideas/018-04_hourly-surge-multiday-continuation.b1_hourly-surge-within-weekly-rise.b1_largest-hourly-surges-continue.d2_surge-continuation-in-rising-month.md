---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-04_hourly-surge-multiday-continuation.b1_hourly-surge-within-weekly-rise.b1_largest-hourly-surges-continue
line: 7.d not profitable
backtest: 018-04_hourly-surge-multiday-continuation.b1_hourly-surge-within-weekly-rise.b1_largest-hourly-surges-continue_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, first reaches several times its 30-day average absolute daily return on the upside, the price keeps rising over the next 5 days by more than the coin's usual 5-day return, only while its 30-day return is positive. The larger that 24-hour return against its 30-day average absolute daily return, the larger the rise, with most of it after surges of twice the usual daily move and more.
Consequence: A trader buys the largest up surges in a coin rising over the month and refuses surges in a coin falling over the month, which the 7-day rise does not screen out.
Why:
- F1: The Calmar fails because one fall dominates: the chained daily book returns a yearly 35.2 % against a deepest fall of 58.5 %, which took 271 days to reach its trough across w1 to w3 while holding the coins fell 62.4 % over the same days; the next four falls (30 to 38 %) also came while holding fell 30 to 79 %.
- F2: The book is mostly a long position in the coins, not timing: of its mean daily return of 0.112 %, 0.071 % is the market's own rise (mean allocation 0.60), so it rides the coins' falls with them.
- F4: Only the largest surges carry a move: cases whose 24-hour return exceeds 1.88 times its 30-day mean absolute value earn +1.97 % above the 5-day drift (t 3.23, 455 cases), while the four lower quintiles earn between -0.54 % and +0.17 % (455 to 454 cases each); the forecast is capped at twice the usual move and so sizes these surges no larger than ones that carry nothing.
- F6: The 7-day-return regime does not select the move: cases in the lowest 7-day quintile (0 to 0.9 %) earn +0.03 % and the middle three quintiles -0.16 % to -0.31 %; only the top quintile (above 12 %) earns +1.58 % (t 2.06), and 16 % of its cases lose more than 10 %.
- F8: A rising month helps: cases by 30-day-return quintile earn -0.37 %, -0.24 %, +0.27 %, +1.16 % (t 1.96, 361 cases) and +0.53 %.
