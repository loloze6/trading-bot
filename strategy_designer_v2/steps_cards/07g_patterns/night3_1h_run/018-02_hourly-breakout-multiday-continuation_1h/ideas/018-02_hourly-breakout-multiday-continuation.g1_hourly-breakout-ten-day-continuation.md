---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-02_hourly-breakout-multiday-continuation
line: 7.g patterns
backtest: 018-02_hourly-breakout-multiday-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's hourly close first rises above its highest price of the prior 20 days, the price keeps rising over the next 10 days by more than the coin's usual 10-day return. The further that close sits above the 20-day high, in multiples of its 30-day average absolute daily return, the larger the rise.
Consequence: A trader who buys hourly breakouts should hold them for about 10 days rather than 5, because about half of the move comes after the fifth day.
Why:
- F1: The move after an hourly close first breaks above its 20-day high keeps growing well past the tested 5 days: on the first break per 120-hour cell, the unusual move is +0.41 % over 1 day (t 1.61, 663 cases), +1.63 % over 5 days (t 3.19, 663), +3.13 % over 10 days (t 3.60, 629) and +4.09 % over 20 days (t 3.07, 572). The 10-day move is about twice the 5-day one, with the highest t, which fits findings F9 and F10.
- F2: The book's gain comes from the trades that outlast the horizon. Trades held over 10 days earn a mean +20.7 % before fees (167 trades), and those over 20 days earn +60.0 % (19). Trades closed within 5.5 days lose a mean −2.0 % (687), and those held 5.5 to 10 days earn +2.6 % (334).
- F3: Over 5 days, the move grows with the size of the break up to a point, then levels off. On all first breaks (1,940 events), it is +0.77 % for breaks of 0 to 0.1 usual daily moves (t 1.52), +1.76 % for 0.1 to 0.3 (t 3.71), +3.13 % for 0.3 to 0.6 (t 4.01) and +2.59 % above 0.6 (t 3.11). Over 20 days the quartiles rise steadily, from +2.1 % to +6.4 %, but the rank correlation is weak (Spearman 0.04, 572 cases).
