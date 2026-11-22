---
line: 7.d not profitable
backtest: 025-02_deeper-fall-bigger-giveback.d1_short-lived-fade-fresh-fall_1d
idea tested: 025-02_deeper-fall-bigger-giveback.d1_short-lived-fade-fresh-fall
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3770 USD
---
## Findings
- **F1:** The fade lasts one day and then reverses: on the first day of a short the book gains +0.198 % a day (t 1.60, 459 days), and on its second day it loses -0.300 % (t -2.59, 456 days) while the coin rises +0.43 %; trades closed after about 2 days earn +0.50 % before fees (633), and those held 3 to 4 days lose -3.87 % (148).
- **F2:** The book keeps shorts long after the bounce's signal is gone. Mean trade length is 5.6 days against a median of 2. On 2299 short days the forecast was already 0, and those days lost -0.074 % a day (t -2.96) while the coin rose +0.28 %. Short days with a live forecast gained +0.064 % (t 1.31, 1775 days).
- **F3:** The next-day fall grows with the bounce's size in usual daily moves. Next day, the coin's fall (raw) was +0.14 %, -0.29 %, +0.87 %, +2.16 %, +2.34 % and +2.53 % for rises of 0-1, 1-1.5, 1.5-2, 2-2.5, 2.5-3 and over 3 usual moves (140, 140, 63, 33, 17 and 9 cases). Over 2 days the pattern is not monotonic: +1.0 %, -0.9 %, +0.6 %, +1.2 %, +2.2 % and -1.1 %.
- **F4:** The forecast loses this grading. Its saturated level of -20 (143 cases, mean rise 2.08 usual moves) gave a 2-day unusual fall of only +0.43 % (t 1.02), and -10 to -20 gave -1.08 % (t -1.54). The verdict's supporting check came out -0.61 % (larger half minus smaller).
- **F5:** The size is too small for the cost. The idea's unusual move is +0.22 % per 2-day case (strength 0.038), against a cost of 0.19 % per trade. The coin's normal drift works against the short at +0.24 % per 2 days, so the total move is -0.02 %. The net result is 1409 trades at -0.95 % each after fees, and a book Sharpe of -0.31.
- **F6:** Short days after a down day lost -0.081 % a day (t -2.79, 1690 days) while the coin rose +0.44 %. Short days on the first up day gained +0.115 % (t 2.33, 1229 days) with the coin falling -0.49 %. Once the bounce has been given back for a day, the coin turns up.

## Ideas
- `025-02_deeper-fall-bigger-giveback.d1_short-lived-fade-fresh-fall.d1_one-day-fade-of-bounces` (from F1, F2, F3, F5): In a coin whose 90-day return is negative and that has just had a one-day rise of several usual daily moves, only while its 30-day return is also negative, the larger that one-day rise in usual daily moves, the larger its fall over the next day.
- `025-02_deeper-fall-bigger-giveback.d1_short-lived-fade-fresh-fall.d2_bounce-fade-then-rebound` (from F1, F6, F3): In a coin whose 90-day return is negative and that has just had a one-day rise of several usual daily moves, only while its 30-day return is also negative, the larger that one-day rise in usual daily moves, the larger its fall over the next day, and the larger its rise over the following day once that next day has closed lower.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
