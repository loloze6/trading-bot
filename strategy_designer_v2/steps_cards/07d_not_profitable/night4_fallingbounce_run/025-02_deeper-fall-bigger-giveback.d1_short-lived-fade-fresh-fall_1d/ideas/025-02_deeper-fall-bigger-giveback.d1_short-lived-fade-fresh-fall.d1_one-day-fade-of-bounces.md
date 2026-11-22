---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-02_deeper-fall-bigger-giveback.d1_short-lived-fade-fresh-fall
line: 7.d not profitable
backtest: 025-02_deeper-fall-bigger-giveback.d1_short-lived-fade-fresh-fall_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is negative and that has just had a one-day rise of several usual daily moves, only while its 30-day return is also negative, the larger that one-day rise in usual daily moves, the larger its fall over the next day.
Consequence: A trader would short a large bounce in a falling coin for one day only, and size it by how many usual moves the bounce was, rather than holding it for two days or more.
Why:
- F1: The fade lasts one day and then reverses: on the first day of a short the book gains +0.198 % a day (t 1.60, 459 days), and on its second day it loses -0.300 % (t -2.59, 456 days) while the coin rises +0.43 %; trades closed after about 2 days earn +0.50 % before fees (633), and those held 3 to 4 days lose -3.87 % (148).
- F2: The book keeps shorts long after the bounce's signal is gone. Mean trade length is 5.6 days against a median of 2. On 2299 short days the forecast was already 0, and those days lost -0.074 % a day (t -2.96) while the coin rose +0.28 %. Short days with a live forecast gained +0.064 % (t 1.31, 1775 days).
- F3: The next-day fall grows with the bounce's size in usual daily moves. Next day, the coin's fall (raw) was +0.14 %, -0.29 %, +0.87 %, +2.16 %, +2.34 % and +2.53 % for rises of 0-1, 1-1.5, 1.5-2, 2-2.5, 2.5-3 and over 3 usual moves (140, 140, 63, 33, 17 and 9 cases). Over 2 days the pattern is not monotonic: +1.0 %, -0.9 %, +0.6 %, +1.2 %, +2.2 % and -1.1 %.
- F5: The size is too small for the cost. The idea's unusual move is +0.22 % per 2-day case (strength 0.038), against a cost of 0.19 % per trade. The coin's normal drift works against the short at +0.24 % per 2 days, so the total move is -0.02 %. The net result is 1409 trades at -0.95 % each after fees, and a book Sharpe of -0.31.
