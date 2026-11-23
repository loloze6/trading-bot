---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound
line: 7.b inconclusive
backtest: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The return over the next 24 hours after a fall over a coin's last 2 hours, at any hour of the day, runs upward, and the larger the fall against the coin's usual 2-hour move, the larger the rise.
Consequence: A trader buys the deepest 2-hour falls at whatever hour they happen and holds for a day, because only the deepest falls rebound by several times a trade's cost.
Why:
- F3: The rebound is not tied to settlement clock times: after falls of at least one usual 2-hour move, the excess 24-hour return is +0.58 % (t 5.71) at the 01:00 close, +0.41 % (t 3.74) at 21:00 and +0.40 % (t 3.31) at 06:00, against +0.37 % (t 3.47) at 00:00 and +0.28 % (t 2.97) at 16:00. Outside settlement hours the rebound is graded the same way: +0.93 % (t 12.2, n 8499) after falls of 3 or more usual moves, +0.26 % (t 4.89) after falls of 2 to 3. These t-statistics come from overlapping bars and overstate the evidence.
- F4: Counted once per 24-hour cell, at the first deep fall and without look-ahead, the any-hour rebound is smaller and present mostly in the deepest falls and some years. Outside settlement hours it is +1.01 % (t 2.62, n 466) after falls of 4 or more usual moves, +0.32 % (t 1.38) after falls of 3 to 4, and -0.12 % (t -2.24, n 7522) after falls of 1 to 1.5. Over all first falls of 2 or more usual moves it is +0.26 % (t 2.61, n 3638), carried by 2021 (+1.15 %, t 2.77) and 2024 (+0.89 %, t 4.43); 2022 is -0.21 %.
- F6: The rebound is front-loaded: the raw return after the settlement cases is +0.11 % over 2 hours (t 5.80), +0.23 % over 8 hours (t 7.26) and +0.36 % over 24 hours (t 6.67), so about two thirds of the day's move comes in the first 8 hours.
- F7: On average the move is too small to pay, but the deepest falls clear the cost. The unusual move is +0.16 % per case, 0.8 times the 0.19 % cost of a trade, and the total move is +0.30 %, 1.6 times the cost; the book's Sharpe is 0.42, 0.135 below holding, with a Calmar of 0.15. The settlement falls of 3 or more usual moves move +0.80 %, about 4 times the cost.
