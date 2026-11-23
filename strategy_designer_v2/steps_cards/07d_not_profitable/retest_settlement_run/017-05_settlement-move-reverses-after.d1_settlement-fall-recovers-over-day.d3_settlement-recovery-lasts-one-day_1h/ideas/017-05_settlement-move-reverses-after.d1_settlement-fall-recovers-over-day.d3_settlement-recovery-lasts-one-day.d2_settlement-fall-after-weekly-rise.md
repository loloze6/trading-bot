---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d3_settlement-recovery-lasts-one-day
line: 7.d confirmed, not profitable
backtest: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d3_settlement-recovery-lasts-one-day_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The rise over the 24 hours after a 00:00 or 16:00 UTC funding settlement grows with the size of the fall over the 2 hours before it against the coin's usual 2-hour move, only while the coin's 7-day return is positive, and it is gone by the second day after settlement.
Consequence: Taking the settlement-fall long only after a week of rising prices trades the crowded-long case the theory describes and avoids buying dips in a falling coin.
Why:
- F1: The book is a part-time copy of holding the coins rather than a timing book: it was in a position on 90 % of the coins' days, its daily returns correlate 0.75 with holding's (beta 0.34), it ran from −1.91 % a day in holding's worst fifth of days to +1.72 % in its best, and its deepest fall of −61 % over 309 days (w1 to w3) came while holding fell −66 % over the same days, so the Calmar of 0.14 is the market's fall carried through the book.
- F3: The 7-day trend splits the same way. Signal cases in a 7-day rise had +0.23 % unusual (t 3.01, 3838 cases) and +0.38 % total, against +0.03 % unusual (t 0.45, 4386 cases) for 7-day-rise settlements without a fall. Signal cases in a 7-day fall had −0.12 % (t −1.39, 4195 cases).
