---
line: 7.d confirmed, not profitable
backtest: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d2_afternoon-settlement-fall-rebound_1h
idea tested: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d2_afternoon-settlement-fall-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3984 USD
---
## Findings
- **F1:** The book's gain is eaten by its fees: over all bars it earns 0.183 bp per bar before costs and pays 0.178 bp per bar in fees, with the fees landing on the entry bar (2.12 bp at the 16:00 close) and the exit bar (2.05 bp eight hours later), so a Sharpe of -0.02 and a yearly return of -2.0 % follow from a move per case (+0.23 % total) only 1.2 times the 0.19 % cost of a trade.
- **F2:** Most cases are too small to pay: at the 16:00 close the 8-hour return after a fall is +0.086 % (t 1.1, n 1153) for forecasts up to 2 and +0.089 % (t 1.3, n 1607) for forecasts 2 to 5, both below the 0.19 % cost; it is +0.42 % (t 6.5, n 2111) for forecasts 10 to 20; and the two smallest fall quintiles give +0.07 % and +0.04 % (t 1.2 and 0.5) against +0.48 % and +0.30 % (t 6.5 and 3.2) for the two largest.
- **F3:** The rebound after a fall is concentrated where the coin's recent volatility is high: among the two largest fall quintiles, the 8-hour return is +0.85 % (t 6.5, n 1110) in the top tercile of the coin's 48-hour mean absolute 2-hour move against its 720-bar usual, against +0.27 % (t 4.0) in the bottom tercile and +0.05 % (t 0.5) in the middle one.
- **F4:** High volatility is not an effect of its own: at the 16:00 close in the high-volatility tercile, the 8-hour return is +0.62 % (t 6.0, n 1587) after a large fall and +0.31 % (t 3.2, n 1229) after a small fall, but only +0.07 % (t 1.0, n 2759) after a rise, so the condition alone earns about a tenth of what it earns with the signal; it belongs to the idea's theory, since crowded, expensive positions and forced flows around settlement are largest in agitated markets.
- **F5:** In the high-volatility tercile the large-fall rebound keeps building past 8 hours, to +0.82 % over 24 hours (t 5.0, n 1577), 4.3 times the cost of a trade, against +0.06 % and +0.09 % over 24 hours in the low and middle terciles (t 0.4 and 0.6) and +0.11 % (t 1.1) after rises in high volatility.
- **F6:** The book's volatility-target sizing works against the effect: it shrinks the position in exactly the high-volatility states where the move is largest (F3). Its mean position is 0.25 of the book in the 8 hours after 16:00 and 0.37 of the book when it is in a position, so the trade-level gross gain of +0.32 % per trade (13404 long trades, net +0.22 %) does not reach the book, which has a mean daily return of -0.002 % on days in a position.
- **F7:** The capped cases are weaker than the cases just below the cap: forecasts at the cap of 20 give +0.22 % over 8 hours (t 2.5, n 1738) against +0.42 % for forecasts 10 to 20, and those trades net +0.01 % after fees against +0.22 % to +0.39 % for the middle quintiles. The result also varies by period, with 2022 at -0.17 % (t -1.9) and the window book means ranging from -19.9 bp (w2) to +12.5 bp (w11).

## Ideas
- `017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d2_afternoon-settlement-fall-rebound.d1_volatile-settlement-fall-day-rebound` (from F1, F3, F4, F5): The return over the 24 hours after the 16:00 UTC funding settlement runs opposite to a fall over the 2 hours before it, while the coin's 2-day volatility is raised against its usual 30-day level, and the larger the fall against the coin's usual 2-hour move, the larger the rise.
- `017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d2_afternoon-settlement-fall-rebound.d2_settlement-fall-scaled-by-volatility` (from F2, F3, F4, F6): The return over the 8 hours after the 16:00 UTC funding settlement runs opposite to a fall over the 2 hours before it, and the larger the fall against the coin's usual 2-hour move, multiplied by the coin's 2-day volatility against its usual 30-day level, the larger the rise.
- `017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d2_afternoon-settlement-fall-rebound.d3_settlement-fall-one-day-rebound` (from F1, F2, F5): The return over the 24 hours after the 16:00 UTC funding settlement runs opposite to a fall over the 2 hours before it, and the larger the fall against the coin's usual 2-hour move, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
