---
brief: 002_moving-average-cross-trend-persistence
source-idea: N4-04_dip-rebound-spans-days
line: 7.d not profitable
backtest: N4-04_dip-rebound-spans-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 20-day and 60-day changes are positive, a day that closes lower right after a sharp-drop day is followed by further decline over the next several days: the drop is the start of a fall, not a dip.
Consequence: A trader should not stay long in a dip that closes lower on the next day, because that is the position that carries the book's deepest falls.
Why:
- F1: The book fails on its falls, not its gain: the book's daily returns (each day, the mean over coins of `book_return`) earn about 21% a year, but the deepest fall chained across windows is -35.6%, and single windows fall far: w17 -21.7%, w13 -19.5%, w11 -17.7%, w19 -15.9%. In those windows nearly the whole fall sits in one to four book days below -2% (w17: one day carried -0.209 of a 3-day, -21.7% fall; w13: two days carried -0.205; w19: two days carried -0.163).
- F2: The loss comes from positions the dip does not repay quickly. Of 1432 trades, the 1017 closed within 1.5 days average +1.11% after fees. The 251 that lasted 1.5 to 3.5 days average -4.35% (worst -28.9%), and the 86 that lasted 3.5 to 7.5 days average -3.59%. A dip that keeps falling after entry is what the book holds into its falls.
