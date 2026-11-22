---
line: 7.d not profitable
backtest: 024-03_uprun-volume-fade-depth-giveback.b2_deep-down-run-rebound_4h
idea tested: 024-03_uprun-volume-fade-depth-giveback.b2_deep-down-run-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3985 USD
---
## Findings
- **F1:** The book is close to a copy of holding the coins, so the Calmar fails. It is in position on 97.9 % to 99.6 % of bars for every coin, and its allocation averages 1.02 on bars whose forecast is 0 (still in position on 99.0 % of them). Its daily returns move with the coins' (correlation 0.94, beta 0.88). Its deepest fall is −76.7 % against holding's −81.2 %, for a yearly return of 27.0 % against 13.0 %, which gives a Calmar of 0.35 against the 0.75 required.
- **F2:** The forecast carries no grading and no selection. It is positive on 49 % of bars, its median positive value is 20 and its 90th percentile is 20, so almost any down close gives a full long. The cases' unusual move is +0.05 % per 18 bars (t 0.48, 5709 cases), 0.3 times the 0.19 % cost of a trade.
- **F3:** The falls come from being long through the coins' own crashes. On the book's worst 5 % of days (145 days, at or below −5.8 %) the coins fell 8.9 % on average, and those days carry 37 % of all the book's losses. The deepest falls inside a window reach −75.2 % (w14) and −76.7 % (w16).
- **F4:** The rebound after a down streak depends on the coin's 30-day return.
- **F5:** The coin's 3-day return before the signal sorts the cases the same way. The top fifth (past 3-day return positive, so a dip inside a rise) is followed by an unusual move of +1.01 % (t 3.10, 856 cases), and the second fifth by −0.53 % (t −2.28, 856 cases).
- **F6:** The streak's depth does not grade what follows.

## Ideas
- `024-03_uprun-volume-fade-depth-giveback.b2_deep-down-run-rebound.d1_down-streak-rebound-uptrend` (from F1, F3, F4, F2): After an unbroken streak of falling four-hour periods whose loss is large relative to the coin's typical four-hour move over the past 30 days, the coin rises over the next three days, only while the coin's 30-day return is positive. The larger that 30-day rise, the larger the rebound.
- `024-03_uprun-volume-fade-depth-giveback.b2_deep-down-run-rebound.d2_dip-within-rising-stretch` (from F5, F3, F1, F2): After an unbroken streak of falling four-hour periods whose loss is large relative to the coin's typical four-hour move over the past 30 days, the coin rises over the next three days, only while its 3-day return is still positive. The larger that 3-day rise around the streak, the larger the rebound.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
