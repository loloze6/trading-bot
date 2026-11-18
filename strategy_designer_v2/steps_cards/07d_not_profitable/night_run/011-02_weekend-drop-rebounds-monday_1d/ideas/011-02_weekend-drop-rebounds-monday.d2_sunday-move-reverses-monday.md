---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-02_weekend-drop-rebounds-monday
line: 7.d not profitable
backtest: 011-02_weekend-drop-rebounds-monday_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's Saturday-to-Sunday close-to-close return is reversed over the next 1 day (Monday): the larger the Sunday move in either direction, the larger the opposite Monday move, and the reversal is stronger the more negative the coin's 20-day return.
Consequence: Trading both sides of the Sunday move on Monday would roughly double the book's active days and the gain those days carry, against a long-only book that sits flat 88 % of the time.
Why:
- F1: The book barely earns because it is in the market on only 11.6 % of days: its mean daily return is 0.000112 against 0.00118 for holding the coins, and its Sharpe is 0.31 against holding's 0.55.
- F2: All of the book's timing gain comes from the Monday bar. A position held from Sunday's close gains 0.002468 a day, of which only 0.000543 is the market's own rise. A position held over Tuesday gains 0.000475, below its market part of 0.000545, so its timing is slightly negative.
- F5: The Sunday move's sign carries the information. Monday returns +0.0073 after a Sunday drop (n 967) and -0.0040 after a Sunday rise (n 1084). After small rises of 0 to 0.5 usual moves Monday returns -0.0071 (t -3.15, n 544). Across all Sundays, the negated Sunday z correlates 0.069 with Monday's return.
- F7: Sunday rises reverse on Monday mostly in a 20-day downtrend: Monday returns -0.0078 there (n 488) against -0.0009 in an uptrend (n 596).
