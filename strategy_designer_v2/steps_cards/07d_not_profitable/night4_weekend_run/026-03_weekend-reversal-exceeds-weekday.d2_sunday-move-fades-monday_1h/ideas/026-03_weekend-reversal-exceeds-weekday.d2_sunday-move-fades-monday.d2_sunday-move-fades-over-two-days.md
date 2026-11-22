---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday.d2_sunday-move-fades-monday
line: 7.d not profitable
backtest: 026-03_weekend-reversal-exceeds-weekday.d2_sunday-move-fades-monday_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's 24-hour return over Sunday is followed by an opposite move over the next 48 hours, and the larger Sunday's move, the larger that opposite move.
Consequence: Holding the Sunday fade through Tuesday captures a larger move per case for the same cost of a trade.
Why:
- F5: The Monday reversal keeps going into Tuesday. Monday-case fade48 is +0.60 % against fade24 +0.44 % (fade6 +0.09 %, fade12 +0.27 %), and it is positive for every coin (+0.16 % to +0.85 %). The Monday-case fade24 is positive in 19 of the 24 windows.
- F1: The book earns almost only on Monday, the one day it holds a position: its mean book return is +0.072 % on days starting Monday (n 2484) and between −0.042 % and +0.009 % on the other six weekdays. With 0.22 trades a day it is out of the market about 6 days in 7, so a +0.39 % total move per weekly case (2.0 times the 0.19 % cost) cannot lift the mean daily return near 0.05 %; it reaches 0.0062 %.
