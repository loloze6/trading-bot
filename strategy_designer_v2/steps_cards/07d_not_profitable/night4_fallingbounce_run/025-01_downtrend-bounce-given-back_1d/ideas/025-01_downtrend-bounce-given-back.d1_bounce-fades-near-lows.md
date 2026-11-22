---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-01_downtrend-bounce-given-back
line: 7.d not profitable
backtest: 025-01_downtrend-bounce-given-back_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is negative, a one-day rise that is large relative to its usual daily move (its 20-day standard deviation of daily returns) is followed by a fall over the next 5 days, and the closer the coin's close on that day to its lowest close of the past 90 days, the larger the fall.
Consequence: A trader would short bounces that leave a falling coin still near its 90-day low, and refuse to short bounces from coins that have already climbed well off it.
Why:
- F4: The fade lives where the coin still trades near its 90-day low. When the close is 1 % to 10 % above its 90-day low, the unusual move is +2.33 % (t 1.43) and +2.96 % (t 2.38), and the total move is +1.77 % and +2.39 %, above the cost. More than 34 % above the low, the move is -1.83 %. In the same way, shallow 90-day falls give +2.39 % (t 2.73) and +2.20 % (t 2.23), while 90-day falls deeper than 49 % give -1.55 %. These counts cover only the 260 cases whose 90 days fit inside the window.
- F1: The book loses because of the coins' own drift, not because its timing is wrong. Its mean daily return is -0.000484. Position times coin return is -0.000305, of which the market's own rise accounts for -0.000370 and timing for only +0.000065. The book is short on 45 % of days at a mean allocation of -0.69, and in the years the coins rose (2020, 2021, 2023, 2024, coin mean daily return +0.0015 to +0.0042) it lost every time (-0.0007 to -0.0025 a day).
- F2: Per case the total move cannot pay a trade. Over the 1299 cases with 10 bars left, the unusual 5-day move is +0.32 % (t 1.19), but the total move in the short direction is -0.27 %, against a cost of 0.19 % per trade. Trades last 8.9 to 11.3 days on a 5-day horizon.
