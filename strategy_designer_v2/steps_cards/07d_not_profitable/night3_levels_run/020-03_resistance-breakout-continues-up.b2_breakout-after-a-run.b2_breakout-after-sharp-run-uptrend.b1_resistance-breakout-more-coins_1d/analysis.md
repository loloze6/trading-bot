---
line: 7.d not profitable
backtest: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend.b1_resistance-breakout-more-coins_1d
idea tested: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend.b1_resistance-breakout-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6893 USD
---
## Findings
- **F1:** The book fails on its falls, not on its gain. Its deepest fall is 33.6 % against a yearly return of 24.9 %, a Calmar of 0.741 against the 0.75 required, while its Sharpe is 1.02 and it beats holding by 0.44. That fall runs 623 days across w1 to w6, and the next falls are 27.7 % (w12 to w15) and 22.8 % (w16 to w17).
- **F2:** Breaks that come after a falling month lose. Of 1338 trades, the fifth with the lowest 30-day return at entry (mean −12.7 %) lost 2.3 % per trade, with 68 % losers. The other four fifths earned +2.2 % to +5.2 % per trade, with 51 % to 62 % losers.
- **F3:** The cost of those trades shows on the days the book holds them. In w1 to w6 a held day earned −0.41 % when the coin's 30-day return at entry was negative, against +0.16 % when it was positive. In w7 to w24 the same comparison was −0.01 % against +0.40 %.
- **F4:** Leaving out the days held on trades entered with a negative 30-day return lifts the Calmar from 0.74 to 1.05. This drops 16 % of the held days; the deepest fall goes from 33.6 % to 26.4 %, the Sharpe from 1.02 to 1.22, and the mean daily return from 0.069 % to 0.074 %. This is a reading of the same days, not a separate test.
- **F5:** Weak breaks carry no rise, and the strength of the break grades the rise. Trades in the lowest fifth of the break reading (touch count × margin, mean 0.45) returned −0.5 % per trade; the top fifth (mean 11.6) returned +7.4 %, and the middle fifths +0.6 % to +2.4 %. Leaving out weak-break days together with falling-month days takes the deepest fall to 20.7 % and the Calmar to 1.20; this is also in-sample.
- **F6:** The 10-day run before the break grades the 5-day rise only weakly. By fifth of the 10-day return, the 5-day return runs −0.1 %, 2.0 %, 0.5 %, 1.2 %, 1.6 %. Measured against the coin's 20-day volatility, the 10-day run gives no ordered pattern in return per trade (1.7 %, 4.1 %, 0.0 %, 6.3 %, 3.0 %).
- **F7:** The worst days are falls the coins share. On the book's 30 worst days (−5.2 % on average) it held 8.7 coins against 5.0 usually, while the coins fell 11.1 % on average. Days with five or more coins held have a daily standard deviation of 1.7 %, against 0.3 % to 1.1 % with fewer.
- **F8:** The idea is large enough to pay its costs. Per case, the unusual move of +0.43 % over 5 days is 1.9 times the 0.22 % round trip, and the total move of +1.17 % is 5.2 times it. The book's shortfall is in when it is long, not in the size of the move it bets on.

## Ideas
- `020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend.b1_resistance-breakout-more-coins.d1_breakout-only-after-rising-month` (from F1, F2, F3, F4, F8): When a coin closes above a price where it turned down several times in the past 90 days, it tends to keep rising over the next 5 days, only while its 60-day return and its 30-day return are both positive, and the larger its 10-day return before the break, the larger the rise.
- `020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend.b1_resistance-breakout-more-coins.d2_stronger-break-larger-rise` (from F1, F5, F6, F8): When a coin closes above a price where it turned down several times in the past 90 days, it tends to keep rising over the next 5 days, only while its 60-day return is positive, and the more often that level turned the price down and the farther the close sits above it, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
