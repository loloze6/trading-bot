---
line: 7.d confirmed, not profitable
backtest: 061-01.b1.b1.b1.d1.d1.d3_quieter-upper-close-fade_1d
idea tested: 061-01.b1.b1.b1.d1.d1.d3_quieter-upper-close-fade
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4588 USD
---
## Findings
- **F1:** The book's gain rests on one window. w16 holds 0.2337 of the book's summed daily return of 0.2439 across the twelve windows of folds B and C. Its 13 cases short-move +24.8 % over 5 days (t 5.96) and its 15 trades net +23.98 % on average. With w16 left out, the Sharpe falls to 0.074, against 0.45 to 0.52 when any other window is left out. This is what fails "lowest Sharpe, one window left out", and it drags the Calmar and the comparison with holding.
- **F2:** Outside w16 the idea's grading by the depth of the 5-day fall (in recent-swing units) is inverted, and the sizing follows it.
- **F3:** How near the close sits to the day's high grades the move the way the brief's theory says. On the quartile of cases with the close nearest the high (median location 0.89), the short 5-day move is +6.95 % (t 3.06, 23 cases), against +5.38 %, +5.13 % and +1.59 % on the lower quartiles (median locations 0.57, 0.68, 0.80). The lowest quartile is not the smallest, so the grading is not monotone. This was not measured with w16 left out.
- **F4:** How wide the day's range is against its 20-day average also grades the move.
- **F5:** The situation's own conditions do not earn alone. On the 5-bar grid of every bar:
- **F6:** The move builds over the 5-day horizon and gives part back after it: +2.56 % at 1 day, +2.87 % at 2, +4.25 % at 3, +4.79 % at 5 (t 3.49, 89 cases), and +1.64 % at 10 days. The 5-day holding (trades last 4.1 to 5.1 days) is right. The grading, not the horizon, is what the repair must change.

## Ideas
- `061-01.b1.b1.b1.d1.d1.d3.d1_high-pinned-close-fades` (from F1, F2, F3, F5, F6): In a choppy, agitated market, when a coin's daily close sits in the upper part of that day's high-low range after its 5-day return has been negative, its price falls over the next five days, and the nearer that close is to the day's high, the larger the fall.
- `061-01.b1.b1.b1.d1.d1.d3.d2_wide-day-upper-close-fade` (from F1, F2, F4, F5, F6): In a choppy, agitated market, when a coin's daily close sits in the upper part of that day's high-low range after its 5-day return has been negative, its price falls over the next five days, and the wider that day's high-low range against its average range over the last 20 days, the larger the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
