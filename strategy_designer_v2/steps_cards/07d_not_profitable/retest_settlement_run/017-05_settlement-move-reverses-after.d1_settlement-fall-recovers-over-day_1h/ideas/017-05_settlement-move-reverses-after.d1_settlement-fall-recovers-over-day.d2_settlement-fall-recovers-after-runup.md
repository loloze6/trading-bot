---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day
line: 7.d confirmed, not profitable
backtest: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The rise over the 24 hours after a 00:00 or 16:00 UTC funding settlement, following a fall over the 2 hours before it, grows with the size of that fall against the coin's usual 2-hour move. It grows more the larger the coin's 7-day return before the settlement, when longs are the crowded side paying funding.
Consequence: A fall into settlement after a run up is a reason to be long for the next day, sized by the fall and by the run up, while a fall in a flat or falling coin gives no such reason.
Why:
- F1: The book is long most of the time and mostly carries the coin's own moves rather than the settlement effect: it holds a position on 72 % of bars (mean allocation 0.38) with a median trade of 24 h and a mean of 40 h, because bets on two settlements a day overlap. On the coin's worst-day quintile it loses −1.91 % against the coin's −5.36 %, and on the best it gains +1.72 % against +5.34 %. Its Sharpe is 0.417 against holding's 0.554, and its deepest fall is −61 %, so Calmar is 0.14.
- F2: The effect is only in the strong falls; the weak falls lose. Over 24 h after the signal, the excess return is −0.13 % (t −1.46) and −0.13 % (t −1.42) in the two lowest forecast quintiles, against +0.17 % (t 1.70) and +0.29 % (t 2.60) in the two highest. The top quintile's total move is +0.44 %, 2.3 times the 0.19 % cost of a trade; the bottom two quintiles' total moves are +0.01 % and +0.02 %, below that cost.
- F5: The 7-day trend sorts the signals as the brief's theory expects: falling into settlement after a run up, when longs should be the crowded, paying side. Signals with the 7-day return in its top third earn +0.20 % excess (t 2.51, total +0.35 %), against −0.01 % (down third) and −0.08 % (middle third). Non-signal settlement bars in the up third earn only +0.11 % (t 1.46), so the up trend alone carries about half of it.
- F6: The move is a 24-hour move and does not last. The excess return of all signals is +0.06 % at 24 h (t 1.27), −0.01 % at 48 h and −0.03 % at 72 h. For the top quintile it is +0.29 % at 24 h (t 2.60) and −0.02 % at 48 h, so holding the overlapping bets past a day (40 h on average) adds exposure and no gain.
