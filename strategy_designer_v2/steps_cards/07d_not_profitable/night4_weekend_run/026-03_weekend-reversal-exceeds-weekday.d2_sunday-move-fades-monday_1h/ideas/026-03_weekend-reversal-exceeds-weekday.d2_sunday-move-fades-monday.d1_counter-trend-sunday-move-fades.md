---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday.d2_sunday-move-fades-monday
line: 7.d not profitable
backtest: 026-03_weekend-reversal-exceeds-weekday.d2_sunday-move-fades-monday_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's 24-hour return over Sunday is followed by an opposite move over the next 24 hours, and the larger Sunday's move, the larger that opposite move, only while Sunday's move runs against the coin's return over the six days before it.
Consequence: A trader would fade only the Sunday moves that counter the past week's trend and refuse those that extend it, which removes the cases that lose most.
Why:
- F3: Sunday's move fades more when it runs against the coin's prior 6-day return than when it extends it. Against that trend: fade24 +0.58 %, fade48 +0.75 %, book P&L per case +0.116 % with sd 2.37 %, 1260 cases. With the trend: fade24 +0.26 %, fade48 +0.42 %, book P&L per case −0.020 % with sd 2.87 %, 1003 cases.
- F4: The falls come from the largest Sunday moves, where the book holds its biggest positions but the fade stops growing. By Sunday-size quintile, mean |allocation| rises from 0.09 to 0.81, while fade24 goes 0.38 %, 0.29 %, 0.41 %, 0.62 %, 0.52 % (the top quintile is below the fourth). The top quintile's book P&L per case has sd 4.1 % and 8.2 % of its cases lose more than 5 %. The worst 5 % of Monday cases (113) have mean |allocation| 0.92 against 0.47 overall and z 1.07 against 0.60, and lose 6.1 times the book's whole Monday gain; this is the source of the 0.073 Calmar and window drawdowns down to −31 %.
