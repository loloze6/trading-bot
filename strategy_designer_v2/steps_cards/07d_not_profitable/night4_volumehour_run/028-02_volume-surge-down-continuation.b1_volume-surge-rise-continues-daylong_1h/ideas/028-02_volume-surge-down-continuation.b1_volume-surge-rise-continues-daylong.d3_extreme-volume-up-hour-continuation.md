---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong
line: 7.d not profitable
backtest: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour whose volume is several times its 30-day hourly average and whose return is positive, the price keeps rising over the next 24 hours. The larger the volume relative to its 30-day average, the larger the rise, whatever the size of that hour's move.
Consequence: A trader would rank up-hours by how extreme their volume is rather than by how large their move is, and buy only the most extreme volume hours.
Why:
- F3: The idea's own move is too small to pay. At the book's 5792 entries the unusual 24-hour move is +0.026 % (t 0.49), and at step 5's 5008 cases it is +0.06 %, which is half the 0.11 % cost of a trade. The larger-forecast half did worse than the smaller half (-0.079 %), and among up-hour grid cells the product of rise and relative volume shows no grading in either the 7-day-up or the 7-day-down group.
- F6: Within the surge itself, volume matters more than the size of the hour's move. Entries in the top quintile of volume against its 30-day mean gain +0.36 % unusual (t 2.44, n 1072), while entries in the top quintile of the hour's scaled rise gain -0.05 % (t -0.32).
