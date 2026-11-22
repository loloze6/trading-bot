---
line: 7.d not profitable
backtest: 025-03_bounce-falling-versus-rising-regime.b2_bounce-fade-over-twenty-days_1d
idea tested: 025-03_bounce-falling-versus-rising-regime.b2_bounce-fade-over-twenty-days
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3548 USD
---
## Findings
- **F1:** The short side carries the losses. Bars held short summed −2.44 in bar gains over 8081 bars, against +12.29 over 8577 bars held long. The 885 short trades lost 13.3 % net on average (median −8.1 %, 30.5 % winners), while the 675 long trades made +8.2 % (47 % winners).
- **F2:** The book fades bounces while the coin keeps rising. The coin's mean next-bar return was +0.12 % on bars held short, higher than the +0.09 % on bars held long, so the shorts were on the wrong side of the coin's own drift.
- **F3:** The short side won only in windows where the coins kept falling and lost in windows where they recovered:
- **F4:** The result rests on one window. In w17 the book made 3.5 % a day (Sharpe 2.61, short side +6.99). With w17 left out, the book's Sharpe falls to −0.058, against 0.45 to 0.57 when any other window is left out.
- **F5:** The falls are deep. The chained book fell 86 % at its deepest (−80 % by w16, −86 % in w17), which gives a Calmar of 0.14. The book is almost never flat (4.2 % of bars), because trades last 35 to 42 days on average, so a short taken after one bounce stays on through the recovery that follows.
- **F6:** The tested gap itself is weak and unconfirmed. Up-regime minus down-regime is +2.17 % over 20 days, with Welch t 1.08 on 382 against 362 cases. The size is 0.048 of a usual move (+1.07 % total per case, 5.5 times the 0.19 % cost), so cost is not the cause. The cause is the short side's direction in recoveries.

## Ideas
- `025-03_bounce-falling-versus-rising-regime.b2_bounce-fade-over-twenty-days.d1_fade-bounces-in-ongoing-falls` (from F1, F2, F3, F5): In one coin, the 20-day return after a one-day rise of several usual daily moves (its day's return over the standard deviation of its last 20 daily returns) is lower when its 90-day return is negative than when it is positive, and the gap widens as the rise gets larger, only while its 30-day return is also negative, more so the more negative its 30-day return.
- `025-03_bounce-falling-versus-rising-regime.b2_bounce-fade-over-twenty-days.d2_bounces-continue-in-risers` (from F1, F4, F6): In one coin whose 90-day return is positive, the 20-day return after a one-day rise of several usual daily moves (its day's return over the standard deviation of its last 20 daily returns) is higher than the coin's normal 20-day drift, more so the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
