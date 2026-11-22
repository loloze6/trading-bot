---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday.d2_sunday-move-fades-monday
line: 7.d not profitable
backtest: 026-03_weekend-reversal-exceeds-weekday.d2_sunday-move-fades-monday_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's 24-hour return over a UTC day is followed by an opposite move over the next 24 hours, and the larger that day's move, the larger the opposite move, except when the day is a Monday or a Friday.
Consequence: The same one-day fade could be taken on five days a week instead of one, so the book is in the market most of the time.
Why:
- F2: The same fade of the previous UTC day's 24-hour return holds on most other days. Pooled over the day-starts other than Tuesday and Saturday it has t 7.57 over 11353 cases with fade24 +0.22 %, and +0.38 % on the larger half of moves. Per day-start, the slope t is 2.44 for Wednesday (fade24 +0.40 %), 3.30 for Thursday, 3.71 for Friday and 4.30 for Sunday. The two exceptions run the other way: Monday's move continues into Tuesday (slope t −2.77, fade24 −0.07 %), and Friday's move into Saturday shows nothing (t −0.48).
- F1: The book earns almost only on Monday, the one day it holds a position: its mean book return is +0.072 % on days starting Monday (n 2484) and between −0.042 % and +0.009 % on the other six weekdays. With 0.22 trades a day it is out of the market about 6 days in 7, so a +0.39 % total move per weekly case (2.0 times the 0.19 % cost) cannot lift the mean daily return near 0.05 %; it reaches 0.0062 %.
