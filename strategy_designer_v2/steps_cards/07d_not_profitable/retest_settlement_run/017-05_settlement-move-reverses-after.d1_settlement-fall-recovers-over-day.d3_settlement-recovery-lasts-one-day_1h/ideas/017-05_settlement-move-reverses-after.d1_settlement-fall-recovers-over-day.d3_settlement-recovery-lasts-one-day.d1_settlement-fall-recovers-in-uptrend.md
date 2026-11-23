---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d3_settlement-recovery-lasts-one-day
line: 7.d confirmed, not profitable
backtest: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d3_settlement-recovery-lasts-one-day_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The rise over the 24 hours after a 00:00 or 16:00 UTC funding settlement grows with the size of the fall over the 2 hours before it against the coin's usual 2-hour move, only while the coin's 30-day return is positive, and it is gone by the second day after settlement.
Consequence: A fall into settlement is a one-day long sized by the fall's depth in a coin that has risen over the past month, and no trade when the coin has fallen over the month, which keeps the book out of the market's long falls.
Why:
- F1: The book is a part-time copy of holding the coins rather than a timing book: it was in a position on 90 % of the coins' days, its daily returns correlate 0.75 with holding's (beta 0.34), it ran from −1.91 % a day in holding's worst fifth of days to +1.72 % in its best, and its deepest fall of −61 % over 309 days (w1 to w3) came while holding fell −66 % over the same days, so the Calmar of 0.14 is the market's fall carried through the book.
- F2: The effect pays only while the coin's 30-day return is positive. There, signal cases had an unusual 24-hour move of +0.20 % (t 2.45, 3221 cases) and a total move of +0.34 %, 1.8 times the 0.19 % cost. In a 30-day fall, signal cases had −0.07 % unusual (t −0.77, 3219 cases) and +0.08 % total, under the cost. The condition alone is not the effect: rising-trend settlements without a fall earned only +0.06 % unusual (t 0.75, 3395 cases). It belongs to the theory, because a crowded long side paying funding after a run up is exactly the brief's setting for pre-settlement selling that reverses.
- F4: The information lies in the deeper falls. The two lowest of the five forecast quintiles gave −0.08 % and −0.16 % unusual 24-hour moves (t −0.71, −1.36), against +0.41 % (t 3.23) and +0.19 % (t 1.39) in the two highest, around 1700 cases each. The deepest two quintiles in a rising 30-day trend gave +0.47 % unusual (t 3.41, 1241 cases) and +0.61 % total, 3.2 times the cost, against −0.05 % (t −0.32, 1333 cases) in a falling trend.
