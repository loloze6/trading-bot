---
line: 7.d not profitable
backtest: 026-03_weekend-reversal-exceeds-weekday.d2_sunday-move-fades-monday_1h
idea tested: 026-03_weekend-reversal-exceeds-weekday.d2_sunday-move-fades-monday
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3888 USD
---
## Findings
- **F1:** The book earns almost only on Monday, the one day it holds a position: its mean book return is +0.072 % on days starting Monday (n 2484) and between −0.042 % and +0.009 % on the other six weekdays. With 0.22 trades a day it is out of the market about 6 days in 7, so a +0.39 % total move per weekly case (2.0 times the 0.19 % cost) cannot lift the mean daily return near 0.05 %; it reaches 0.0062 %.
- **F2:** The same fade of the previous UTC day's 24-hour return holds on most other days. Pooled over the day-starts other than Tuesday and Saturday it has t 7.57 over 11353 cases with fade24 +0.22 %, and +0.38 % on the larger half of moves. Per day-start, the slope t is 2.44 for Wednesday (fade24 +0.40 %), 3.30 for Thursday, 3.71 for Friday and 4.30 for Sunday. The two exceptions run the other way: Monday's move continues into Tuesday (slope t −2.77, fade24 −0.07 %), and Friday's move into Saturday shows nothing (t −0.48).
- **F3:** Sunday's move fades more when it runs against the coin's prior 6-day return than when it extends it. Against that trend: fade24 +0.58 %, fade48 +0.75 %, book P&L per case +0.116 % with sd 2.37 %, 1260 cases. With the trend: fade24 +0.26 %, fade48 +0.42 %, book P&L per case −0.020 % with sd 2.87 %, 1003 cases.
- **F4:** The falls come from the largest Sunday moves, where the book holds its biggest positions but the fade stops growing. By Sunday-size quintile, mean |allocation| rises from 0.09 to 0.81, while fade24 goes 0.38 %, 0.29 %, 0.41 %, 0.62 %, 0.52 % (the top quintile is below the fourth). The top quintile's book P&L per case has sd 4.1 % and 8.2 % of its cases lose more than 5 %. The worst 5 % of Monday cases (113) have mean |allocation| 0.92 against 0.47 overall and z 1.07 against 0.60, and lose 6.1 times the book's whole Monday gain; this is the source of the 0.073 Calmar and window drawdowns down to −31 %.
- **F5:** The Monday reversal keeps going into Tuesday. Monday-case fade48 is +0.60 % against fade24 +0.44 % (fade6 +0.09 %, fade12 +0.27 %), and it is positive for every coin (+0.16 % to +0.85 %). The Monday-case fade24 is positive in 19 of the 24 windows.

## Ideas
- `026-03_weekend-reversal-exceeds-weekday.d2_sunday-move-fades-monday.d1_counter-trend-sunday-move-fades` (from F3, F4): A coin's 24-hour return over Sunday is followed by an opposite move over the next 24 hours, and the larger Sunday's move, the larger that opposite move, only while Sunday's move runs against the coin's return over the six days before it.
- `026-03_weekend-reversal-exceeds-weekday.d2_sunday-move-fades-monday.d2_sunday-move-fades-over-two-days` (from F5, F1): A coin's 24-hour return over Sunday is followed by an opposite move over the next 48 hours, and the larger Sunday's move, the larger that opposite move.
- `026-03_weekend-reversal-exceeds-weekday.d2_sunday-move-fades-monday.d3_daily-moves-fade-most-weekdays` (from F2, F1): A coin's 24-hour return over a UTC day is followed by an opposite move over the next 24 hours, and the larger that day's move, the larger the opposite move, except when the day is a Monday or a Friday.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
