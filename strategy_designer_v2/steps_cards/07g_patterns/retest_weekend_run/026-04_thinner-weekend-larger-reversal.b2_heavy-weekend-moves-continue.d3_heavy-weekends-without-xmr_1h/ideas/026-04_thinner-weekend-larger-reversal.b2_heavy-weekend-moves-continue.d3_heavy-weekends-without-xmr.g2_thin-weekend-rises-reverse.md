---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d3_heavy-weekends-without-xmr
line: 7.g patterns
backtest: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d3_heavy-weekends-without-xmr_1h
instruments: BTC, ETH, LTC, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's Saturday-Sunday rise made on volume lighter than its mean over the preceding five weekdays is followed by a fall over the next 48 hours, the larger the thinner the weekend volume is against the weekdays.
Consequence: A weekend rise on thin volume is a reason to fade it over Monday and Tuesday, or to refuse to buy it.
Why:
- F4: Weekend rises made on the thinnest volume (bottom ratio quintile, mean ratio 0.28) reverse over the next 48 hours: −0.205 usual moves, t −3.06, n 185. Weekend falls in the same quintile do not reverse (+0.023, t 0.35).
- F1: On weekends ending Sunday 23:00 UTC, the signed 48-hour move after the weekend (in usual 48-hour moves) grows with the log of the weekend-to-weekday volume ratio, with slope 0.187 and t 4.48 over 1904 cases. Windows ending on other weekdays show slopes of 0.015–0.064 with t of 1.8 or less, so the volume grading is specific to the weekend. By coin it holds in XRP (t 3.77), BTC (t 2.63), ETH (t 2.52) and LTC (t 1.93), but not in ZEC (t 0.18).
