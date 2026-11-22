---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-01_fading-volume-uprun-giveback-size.d2_fading-volume-down-run-rebound
line: 7.d not profitable
backtest: 024-01_fading-volume-uprun-giveback-size.d2_fading-volume-down-run-rebound_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: The higher a coin's 30-day return, the more it rises over the next three days.
Consequence: A strong past month is a reason to hold the coin long, and a weak one a reason to refuse a long.
Why:
- F3: Bars held after a low 30-day return pay nothing but carry full risk. The book's mean bar gain in the lowest 30-day-return quintile is +0.000009 (t 0.06, n 12279, sd 0.0160) and in the second -0.00020 (t -1.56). In the highest quintile it is +0.00065 (t 4.08, n 12400), and the 7-day return shows the same pattern (lowest quintile +0.00014, t 0.88; highest +0.00062, t 4.07).
