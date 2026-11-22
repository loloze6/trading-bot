---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue
line: 7.g patterns
backtest: 026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's return over the past 5 days, read at the start of the weekend, continues over the following 2 days in the same direction. The larger the 5-day move relative to the coin's usual 5-day move, the larger the weekend move that follows.
Consequence: A trader should lean with the coin's past-week trend going into Saturday and Sunday, more so the stronger that trend, and refuse to fade weekly moves at the weekend.
Why:
- F1: Over the next 48 hours, a coin's past 5-day return carries on most strongly from Friday and Saturday 00:00. Regressing the 48-hour excess return on the 5-day move (in units of its std) gives a slope of +0.0052 per std with t 4.5 (n 2301) from Saturday starts and +0.0048 with t 3.8 (n 2293) from Friday starts, against −0.0032 (t −2.0) from Monday starts. Seven start days were tested and t 4.5 still clears that.
- F2: Sorted into quintiles by the previous week's (Mon→Sat) move, the next weekend's return rises roughly monotonically: −0.04 % (t −0.1), +0.26 %, +0.44 %, +0.76 % (t 2.8), +0.63 % (t 1.9), about 448 weekends each. The spread of about 0.7 % between the extreme quintiles is several times the 0.19 % cost of a trade.
- F3: The weekend momentum of F1 is not even across coins or years. By coin the Saturday-start slope has t 4.2 for XRP and 3.3 for ETH, but only 0.6–1.1 for BTC, LTC, XMR and ZEC. By year it is positive in 2018 (t 3.6), 2019 (t 3.0) and 2024 (t 4.3), and negative in 2020 (t −1.0) and 2023 (t −1.8).
- F4: The brief's weekend reversal is absent. The weekend move has a correlation of −0.007 (slope t −0.21, n 2352) with the Monday–Tuesday excess return. By weekend-move quintile that excess is +0.40 %, −0.86 % (t −2.8), +0.02 %, +0.27 % and +0.17 %, with no order. Monday–Tuesday moves show no cleaner pattern into Wednesday–Thursday.
