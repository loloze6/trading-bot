---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall.c1_broken-support-below-average
line: 7.d not profitable
backtest: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall.c1_broken-support-below-average_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's daily close sits just below prices where it turned up several times in the past 90 days, it tends to fall over the next 10 days, and the more such past turning-up lows lie just above the close, the larger the fall, only while the close is below its 50-day average and still well above its 90-day low, the farther above that low the larger the fall.
Consequence: A short under a broken support cluster is worth taking in the middle of the coin's 90-day range, and refused once the coin is already pressed against its 90-day low, where it rebounds.
Why:
- F2: On the 627 grid cases with a forecast of -2 or below, the short-direction unusual 10-day move is +0.86 % (t 1.47), but the total move is -0.35 %, so the drift the short gives up outweighs the effect found.
- F3: The raw size of the cluster of turning-up lows does grade the fall. In the two upper quartiles of the raw value (mean 0.78 and 2.49), the unusual move is +2.19 % (t 2.27) and +2.24 % (t 2.42) and the total move is +1.01 % and +1.07 %, about 5 times the 0.19 % cost of a trade. In the two lower quartiles (mean 0.17 and 0.37), the unusual move is -0.53 % and -0.47 % and the total move is -1.77 % and -1.72 %.
- F5: Where the close sits in its 90-day range splits the cases. In the lowest two quartiles of the range position (mean 0.08 and 0.20), the total short move is -1.70 % and -1.45 % and the unusual move is -0.47 % and -0.26 %. In the third quartile (0.32) the unusual move is +3.52 % (t 3.03) and in the top quartile (0.51) +2.11 % (t 1.81).
- F6: After a deep 90-day fall the coin rebounds instead of falling. In the lowest quartile of the 90-day return (mean -47 %, 33 cases) the unusual short move is -5.83 % (t -2.09), against +5.26 % (t 3.08) and +4.13 % (t 3.39) in the next two quartiles (-23 % and -6 %). After the steepest 30-day falls (mean -32 %, 117 cases) it is -0.61 %, against +1.7 % to +2.1 % in the other quartiles.
