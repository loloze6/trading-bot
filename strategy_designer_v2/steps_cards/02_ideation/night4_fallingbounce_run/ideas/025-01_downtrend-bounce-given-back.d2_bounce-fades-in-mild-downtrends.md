---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-01_downtrend-bounce-given-back
line: 7.d not profitable
backtest: 025-01_downtrend-bounce-given-back_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is negative, a one-day rise that is large relative to its usual daily move (its 20-day standard deviation of daily returns) is followed by a fall over the next 5 days, and the shallower the coin's 90-day fall, the larger the fall that follows.
Consequence: A trader would fade bounces in coins drifting gently lower, and refuse to fade bounces in coins that have already crashed, where bounces hold.
Why:
- F4: The fade lives where the coin still trades near its 90-day low. When the close is 1 % to 10 % above its 90-day low, the unusual move is +2.33 % (t 1.43) and +2.96 % (t 2.38), and the total move is +1.77 % and +2.39 %, above the cost. More than 34 % above the low, the move is -1.83 %. In the same way, shallow 90-day falls give +2.39 % (t 2.73) and +2.20 % (t 2.23), while 90-day falls deeper than 49 % give -1.55 %. These counts cover only the 260 cases whose 90 days fit inside the window.
- F3: The idea's grading runs the wrong way. The smallest bounces fade best: in z quintiles (0.36, 0.56] and (0.56, 0.76] the unusual move is +1.29 % (t 2.13) and +1.37 % (t 2.04), while in (1.04, 1.45] it is -0.88 % (t -1.46). The 650 cases at forecast -20 give +0.07 % (t 0.18), against +1.11 % (t 2.12) for the weakest forecasts. The strongest-forecast trades lose -3.37 % net each (1714 trades, 36 % winners), against -1.77 % for the rest.
- F1: The book loses because of the coins' own drift, not because its timing is wrong. Its mean daily return is -0.000484. Position times coin return is -0.000305, of which the market's own rise accounts for -0.000370 and timing for only +0.000065. The book is short on 45 % of days at a mean allocation of -0.69, and in the years the coins rose (2020, 2021, 2023, 2024, coin mean daily return +0.0015 to +0.0042) it lost every time (-0.0007 to -0.0025 a day).
