---
brief: 030_absorption-day-close-location
source-idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise
line: 7.g patterns
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The more a coin falls on a day whose volume is heavy against its own prior 20-day average, the more it rises over the next day. The rebound grows both with the size of the day's fall and with how heavy the volume was, and it is largest when the coin's 20-day volatility is high.
Consequence: A trader buys a coin for one day after a heavy-volume sell-off, sized by the fall and the surge, and refuses to buy after heavy-volume up days.
Why:
- F1: The tested idea's edge is a rebound after heavy-volume falling days, not after volume surges in general. In the top fifth of the volume ratio (today's volume over its prior 20-day mean), next-day excess return is +1.074 % (t 5.19, n 923) when the day's return is in the coin's bottom fifth. When that day's return is in the top fifth, it is −0.152 % (t −0.81, n 957).
- F3: Volume is what makes a falling day rebound. Across all days, bottom-fifth return days are followed by +0.456 % (t 4.64, n 3438). On low-volume days (bottom two volume fifths) the same falling days are followed by only +0.011 % (t 0.06, n 687).
- F4: The rebound is several times the cost of a trade, unlike the tested idea's average case. The rebound of +1.06 % per day is about 5.6 times the 0.19 % cost. The tested idea's total move of +0.21 % is 1.1 times the cost.
- F5: Falling days carry most of the book's gain. Its in-position gain on bars whose day return is in the bottom fifth sums to 8.49 out of about 13.16 in total (65 %), at +0.452 % per bar (n 1880). Top-fifth return days give +0.101 % per bar (n 1972).
- F6: The heavy-volume effect is strongest when the coin is already volatile. In the highest third of 20-day volatility, the top volume fifth is followed by +0.838 % (t 3.27, n 913). In the middle third it is −0.013 % (t −0.08, n 965), and in the lowest third +0.245 % (t 1.97, n 1032).
