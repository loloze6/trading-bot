---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-01_resistance-retest-turns-down.d2_thirty-day-momentum-continues
line: 7.g patterns
backtest: 020-01_resistance-retest-turns-down.d2_thirty-day-momentum-continues_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The nearer a coin's close is to the top of its 20-day high-low range, the more it rises over the next 10 days, beyond its normal drift.
Consequence: A trader should lean long on a coin closing near the top of its recent range, more the nearer it is, and refuse longs on coins sitting low in it.
Why:
- F1: Where a coin's close sits in its own 20-day high-low range predicts its next 10 days better than the tested 30-day return does: the slope of the de-drifted 10-day return on the range position is +1.22 % per standard deviation (t 3.98, 2699 non-overlapping cases), against +0.78 % (t 2.44, 2411 cases) for the 30-day return. The slope is +0.70 % (t 3.48, 2843 cases) over 5 days and +1.15 % (t 3.62) for the 30-day range.
- F2: The range position takes over the 30-day momentum: in a joint regression on the 10-day de-drifted return, the 30-day range position keeps its slope (+1.17 %, t 2.67) while the 30-day return loses its own (-0.03 %, t -0.06).
- F3: The effect sits at the top of the range. In the top fifth of the 30-day range position, a coin beats its normal 10-day drift by +2.67 % (t 2.95, 485 cases), about 14 times the 0.19 % cost of a round trip. The second-lowest fifth falls -1.41 % (t -2.24), but the lowest fifth falls only -0.13 % (t -0.19).
- F6: The range-position effect is stronger in the later windows and uneven across coins:
