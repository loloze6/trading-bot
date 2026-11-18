---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-02_weekend-drop-rebounds-monday
line: 7.d not profitable
backtest: 011-02_weekend-drop-rebounds-monday_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin that fell over the weekend (its Saturday-to-Sunday close-to-close return) rises over the next 1 day (Monday only), and the larger the weekend drop the larger the rebound, only while the coin's 20-day return is negative, more so the deeper that 20-day fall.
Consequence: A trader would buy weekend drops only in coins already falling over 20 days, hold through Monday and be out before Tuesday, which removes the Tuesday give-back.
Why:
- F2: All of the book's timing gain comes from the Monday bar. A position held from Sunday's close gains 0.002468 a day, of which only 0.000543 is the market's own rise. A position held over Tuesday gains 0.000475, below its market part of 0.000545, so its timing is slightly negative.
- F3: Tuesday gives back part of the deepest Sunday drops: after a Sunday fall of more than 2 usual moves, Tuesday returns -0.0276 (t -3.96, n 40), while Monday returns +0.0142 (t 2.77).
- F4: Inside Sunday drops, the depth of the drop does not grade the Monday rebound. The correlation of drop size with Monday's return is 0.015 among drops. Monday rises after every drop bin from 0 to -1.5 usual moves (+0.0057 to +0.0174, t 2.2 to 2.7).
- F6: Drop depth grades the rebound only when the coin was already falling. Among Sunday drops with a negative 20-day return, deep drops are followed by a 2-day excess of +0.0176 against +0.0042 for shallow ones (n 186/137). In flat or rising 20-day trends deep drops give only +0.0015 to +0.0026.
