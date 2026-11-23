---
brief: 030_absorption-day-close-location
source-idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise
line: 7.g patterns
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: On a day whose volume is heavy against the coin's prior 20-day average, the lower the close sits within that day's high-low range, the more the coin rises over the next day. The heavier the volume, the stronger the link.
Consequence: A trader goes long for one day after a heavy-volume day that closed near its low, and treats a heavy-volume close near the high as no reason to be long.
Why:
- F2: Close location in the day's range adds to this. In the top volume fifth, next-day excess return is +1.061 % (t 5.60, n 897) when the close sits in the lowest third of the range. It is +0.148 % (t 0.76, n 884) in the middle third and −0.068 % (t −0.39, n 1129) in the top third. In no other volume fifth does the low-close third exceed |t| 1.3.
- F1: The tested idea's edge is a rebound after heavy-volume falling days, not after volume surges in general. In the top fifth of the volume ratio (today's volume over its prior 20-day mean), next-day excess return is +1.074 % (t 5.19, n 923) when the day's return is in the coin's bottom fifth. When that day's return is in the top fifth, it is −0.152 % (t −0.81, n 957).
- F4: The rebound is several times the cost of a trade, unlike the tested idea's average case. The rebound of +1.06 % per day is about 5.6 times the 0.19 % cost. The tested idea's total move of +0.21 % is 1.1 times the cost.
