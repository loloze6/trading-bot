---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-03_uprun-volume-fade-depth-giveback.b2_deep-down-run-rebound
line: 7.d not profitable
backtest: 024-03_uprun-volume-fade-depth-giveback.b2_deep-down-run-rebound_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: After an unbroken streak of falling four-hour periods whose loss is large relative to the coin's typical four-hour move over the past 30 days, the coin rises over the next three days, only while its 3-day return is still positive. The larger that 3-day rise around the streak, the larger the rebound.
Consequence: A trader would buy a short down streak that interrupts a 3-day rise and refuse one that extends a 3-day fall, which keeps the book out of the coin's crashes.
Why:
- F5: The coin's 3-day return before the signal sorts the cases the same way. The top fifth (past 3-day return positive, so a dip inside a rise) is followed by an unusual move of +1.01 % (t 3.10, 856 cases), and the second fifth by −0.53 % (t −2.28, 856 cases).
- F3: The falls come from being long through the coins' own crashes. On the book's worst 5 % of days (145 days, at or below −5.8 %) the coins fell 8.9 % on average, and those days carry 37 % of all the book's losses. The deepest falls inside a window reach −75.2 % (w14) and −76.7 % (w16).
- F1: The book is close to a copy of holding the coins, so the Calmar fails. It is in position on 97.9 % to 99.6 % of bars for every coin, and its allocation averages 1.02 on bars whose forecast is 0 (still in position on 99.0 % of them). Its daily returns move with the coins' (correlation 0.94, beta 0.88). Its deepest fall is −76.7 % against holding's −81.2 %, for a yearly return of 27.0 % against 13.0 %, which gives a Calmar of 0.35 against the 0.75 required.
- F2: The forecast carries no grading and no selection. It is positive on 49 % of bars, its median positive value is 20 and its 90th percentile is 20, so almost any down close gives a full long. The cases' unusual move is +0.05 % per 18 bars (t 0.48, 5709 cases), 0.3 times the 0.19 % cost of a trade.
