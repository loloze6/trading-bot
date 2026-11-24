---
line: 7.g patterns
backtest: 031-01.b1.b2.b2.e2_short-rise-in-uptrend-continues_1d
idea tested: 031-01.b1.b2.b2.e2_short-rise-in-uptrend-continues
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3941 USD
---
## Findings
- **F1:** The day after a coin's largest daily falls, it rose more than its normal drift. In the bottom quintile of 1-day returns (mean −6.0 %), the next day's excess return was +0.45 % (t 4.63, 3450 days). Every other quintile was flat or negative: −0.01 %, −0.17 %, −0.11 %, and −0.20 % (t −2.06) after the largest rises. This is the strongest pattern of the roughly fifteen angles examined.
- **F2:** The tested idea's continuation does not hold coin by coin or year by year. Inside 60-day uptrends, the slope t of the 3-day excess return on the 5-day rise is 3.09 for XRP but −2.97 for XMR, and between −0.60 and 0.49 for BTC, ETH, LTC and ZEC. No year reaches 2 (highest 1.85 in 2024). The top 5-day-rise quintile's excess is +0.95 % (t 1.48, 286 cases), and the size check gives t 0.28.
- **F3:** The book mostly follows the market rather than timing it. Its daily returns correlate 0.56 with holding the coins, and it earned 0.066 % a day against holding's 0.118 %.
- **F4:** The book's best and worst days both come after large runs. Its worst 5 % of days in a position (coin −7.3 % that day) and its best 5 % (coin +9.4 %) both follow a prior 5-day rise of about 16 %, against 4.1 % on all its days in a position. After a sharp run, the next day's sign decides the book.
- **F5:** After very wide-range days, the coin rose more over the next 3 days. In the top quintile of range relative to its 20-day average (1.96×), the 3-day excess return was +0.75 % (t 2.54, 1061 cases), against −0.23 % to +0.06 % in the other quintiles. Given the number of angles examined, this is too weak to count on its own.
- **F6:** Next-day excess returns differ by weekday, from +0.30 % after Fridays (t 3.76, 2479 days) to −0.30 % after Wednesdays (t −2.70). This is a calendar pattern with no grading, so no idea is drawn from it.
- **F7:** The wide-and-flat day the brief describes shows no grading over the next 3 days. After a 5-day rise, the excess by quintile of range × flatness is +0.11 %, +0.89 %, +0.08 %, +0.44 % and +0.05 % from narrowest to widest-flattest, so the widest-flattest days are not followed by a larger fall.

## Ideas
- `031-01.b1.b2.b2.e2.g1_one-day-fall-bounces-back` (from F1, F4): The larger a coin's fall over its last day, the more it rises over the next day, compared with its normal drift.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
