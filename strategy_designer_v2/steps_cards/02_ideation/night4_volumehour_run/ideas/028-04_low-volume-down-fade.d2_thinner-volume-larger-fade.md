---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-04_low-volume-down-fade
line: 7.d not profitable
backtest: 028-04_low-volume-down-fade_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin falls far more than its typical hourly move over the past 30 days while its volume stays near its average hourly volume over the past 30 days, the price recovers part of that fall over the next two to six hours; the further that hour's volume lies below its 30-day hourly average, the larger the recovery.
Consequence: The thinner the volume behind a sharp hourly fall, the more of that fall a trader can expect to be given back within six hours.
Why:
- F1: The move per case is smaller than the cost of a trade, so the book loses before any other effect. The total move is +0.07 % per case over 6 hours against a cost of 0.11 % per trade. Per day, BTC's gross gain is 0.032 % against 0.078 % of fees. ETH's gross gain is 0.062 % against 0.062 % of fees. The book's mean daily return is -0.025 %.
- F3: The deepest falls get the largest positions, and the trades on them earn the least. Trades entered at forecast 10 to 20 number 6763, more than half of the 12736 trades, and earn +0.046 % gross and -0.054 % net. Trades entered at forecast 2 to 5 earn +0.32 % gross and +0.22 % net (n 3233). Trades entered at forecast 5 to 10 earn +0.23 % gross and +0.13 % net (n 2730). This matches the failed supporting check (upper minus lower half -0.022 %).
- F4: On volume near its average, the recovery does not grow with the depth of the fall. On non-overlapping 6-hour cases, the unusual move is as follows:
- F6: Falls on volume below 2/3 of its 30-day average recover more than falls on volume near its average, though the samples are small. For falls of 1.5 to 2 usual moves, the move is +0.28 % (t 1.9, n 222) against +0.11 % (n 316). For falls of 3 to 4 usual moves, it is +1.27 % (t 3.2, n 8) against +0.32 % (n 74).
- F7: The recovery fades beyond 6 hours. For normal-volume falls of more than 2 usual moves, the unusual move is +0.02 % at 2 hours, +0.05 % at 6 hours and -0.21 % at 12 hours (grid cases 1051, 392 and 219).
