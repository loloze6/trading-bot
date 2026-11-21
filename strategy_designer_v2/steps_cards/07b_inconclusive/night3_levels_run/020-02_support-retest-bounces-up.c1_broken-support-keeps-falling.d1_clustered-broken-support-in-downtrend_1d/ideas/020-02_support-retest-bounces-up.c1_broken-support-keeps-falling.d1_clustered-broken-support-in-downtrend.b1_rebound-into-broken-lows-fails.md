---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.d1_clustered-broken-support-in-downtrend
line: 7.b inconclusive
backtest: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.d1_clustered-broken-support-in-downtrend_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's daily close sits just below prices where it turned up several times in the past 90 days, after rising that day back toward them, it tends to fall over the next 10 days, only while the close is below its 50-day average price, and the larger that day's rise toward those past lows, the larger the fall.
Consequence: A strong up-day in a coin below its 50-day average that stalls just under a cluster of broken past lows is a reason to be short for about 10 days, while a close under those lows reached by a down-day is no reason to be short.
Why:
- F5: The idea's horizon puts the measure in the wrong place. On the signal's own bar the coin has already fallen 1.37 % (short side, t 8.7, 1365 cases). Over the next 1 to 3 days it bounces (-0.18 % t -1.35, -0.21 % t -0.91). The fall shows only by 10 days: +0.97 % (t 2.36) on the 5-day grid, but +0.90 % with t 1.80 over 902 cases on a proper 10-day grid. It fades again by 20 days (+0.73 %, t 1.03).
- F7: The effect shows clearly where the signal day was an up day, a retest of the broken lows from below. When the coin rose about 5.4 % on the signal bar (lowest quartile of the short-side bar move), the next 10 days fall 2.98 % more than usual (t 2.97, 212 cases). The other three quartiles give +0.06 %, -0.11 % and +0.22 % (all |t| < 0.2).
- F8: This retest effect belongs to the lows above the close, not to up days in a downtrend in general. Below-average bars with the same largest same-day rise give -0.09 % over 10 days (t -0.09, 179 cases). The retest cases' 2.98 % unusual move is about 15 times the 0.19 % cost of a trade, and still clears it after the coin's normal 10-day drift.
- F3: The cluster reading itself is not graded. By quartile of the raw cluster value, the 5-day unusual move is -0.01 %, -0.05 %, +0.58 % and +0.23 %, and the 10-day move on a 10-day grid is +1.62 %, +0.34 %, +1.18 % and +0.42 %. The Spearman correlation between cluster value and 10-day move is -0.018.
- F4: What little there is comes from the regime, not from the lows above the close. All below-50-day-average bars on the 5-day grid give +0.42 % (t 1.54, 1420 cases), about what the signals give. On the 10-day grid the same bars give +0.58 % (t 1.12, 713 cases).
