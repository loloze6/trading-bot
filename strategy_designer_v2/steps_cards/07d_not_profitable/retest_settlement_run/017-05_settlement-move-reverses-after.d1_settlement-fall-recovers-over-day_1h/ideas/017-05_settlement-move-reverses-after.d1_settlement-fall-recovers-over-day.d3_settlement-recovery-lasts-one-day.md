---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day
line: 7.d confirmed, not profitable
backtest: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The rise over the 24 hours after a 00:00 or 16:00 UTC funding settlement grows with the size of the fall over the 2 hours before it against the coin's usual 2-hour move, and it is gone by the second day after settlement.
Consequence: A fall into settlement is a one-day long, sized by the fall, closed after a day rather than carried into the next settlement's bet.
Why:
- F1: The book is long most of the time and mostly carries the coin's own moves rather than the settlement effect: it holds a position on 72 % of bars (mean allocation 0.38) with a median trade of 24 h and a mean of 40 h, because bets on two settlements a day overlap. On the coin's worst-day quintile it loses −1.91 % against the coin's −5.36 %, and on the best it gains +1.72 % against +5.34 %. Its Sharpe is 0.417 against holding's 0.554, and its deepest fall is −61 %, so Calmar is 0.14.
- F2: The effect is only in the strong falls; the weak falls lose. Over 24 h after the signal, the excess return is −0.13 % (t −1.46) and −0.13 % (t −1.42) in the two lowest forecast quintiles, against +0.17 % (t 1.70) and +0.29 % (t 2.60) in the two highest. The top quintile's total move is +0.44 %, 2.3 times the 0.19 % cost of a trade; the bottom two quintiles' total moves are +0.01 % and +0.02 %, below that cost.
- F6: The move is a 24-hour move and does not last. The excess return of all signals is +0.06 % at 24 h (t 1.27), −0.01 % at 48 h and −0.03 % at 72 h. For the top quintile it is +0.29 % at 24 h (t 2.60) and −0.02 % at 48 h, so holding the overlapping bets past a day (40 h on average) adds exposure and no gain.
- F7: The 15:00-stamped settlement (16:00 UTC) carries more than the 23:00 one: +0.065 % excess (t 1.17, n 8402) against +0.038 % (t 0.53, n 4246).
