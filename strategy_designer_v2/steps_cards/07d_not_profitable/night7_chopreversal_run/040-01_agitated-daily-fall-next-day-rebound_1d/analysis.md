---
line: 7.d confirmed, not profitable
backtest: 040-01_agitated-daily-fall-next-day-rebound_1d
idea tested: 040-01_agitated-daily-fall-next-day-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3769 USD
---
## Findings
- **F1:** The Calmar failure comes from small falls. Ranked by the fall's size against the coin's usual daily move, the top quarter of signals (z above 1.42) is followed by a next-day move of +1.69 % above the coin's drift (t 4.45, 360 cases). The three lower quarters give +0.45 % (t 1.38), +0.57 % (t 1.58) and −0.02 % (t −0.06), about 2 to 3 times the 0.19 % cost of a trade at most. Yet the second and third quarters still put up −1.34 and −2.85 of summed losing-day gain, against −3.71 for the top quarter.
- **F2:** The book's deepest fall was rebuilt from the bars (−22 %, approximate). It lasted 76 days and held 144 positions. Those positions were mostly ordinary falls: mean z 0.86, below the top-quarter cut of 1.42, and only 24 % of them in the top quarter. Their mean next-day return was −2.2 %. The falls are therefore carried by the weak part of the signal, not by the large overshoots.
- **F3:** Rebuilt books with a cost of 0.095 % per side change the falls a lot. Trading only the top-quarter falls cuts the deepest fall from −22.0 % to −9.8 %. The yearly return moves from +21.4 % to +18.2 % and Calmar rises from 0.97 to 1.86. Scaling the position with the fall's size (allocation × z / median z) gives Calmar 1.75 and Sharpe 1.24, against 1.16 for the original. Both raise the failing measure, Calmar.
- **F4:** A fall that follows a fall the day before reverses more. Signals with a fall the previous day are followed by +0.99 % (t 3.28, 594 cases), against +0.41 % (t 1.95, 845) without one. Among top-quarter falls this is +3.08 % (t 4.36, 146) against +0.71 % (t 1.74, 214).
- **F5:** The previous-day fall is not an effect of its own. In agitated bars where the previous day fell but today did not (no signal), the next day is −0.74 % against drift (t −3.75, 802 cases). The condition earns only together with today's fall. This fits the brief's theory that urgent one-sided flow spread over consecutive days pushes price further from value.
- **F6:** The gain is spread across years rather than resting on one. Next-day excess return on signals is positive in 10 of 12 windows of folds B and C. The worst-days check agrees: the book's 20 worst days averaged −4.5 % while the coins fell −11.2 %, and they fall across 9 different windows.

## Ideas
- `040-01.d1_agitated-outsized-fall-rebound` (from F1, F2, F3, F6): In an agitated market, the larger a coin's one-day fall, measured as its percent change from the previous close against its usual daily move over the past 60 days, the larger its rise over the next day, with the rise growing faster than the fall so that falls several times the usual daily move carry most of it.
- `040-01.d2_agitated-second-down-day-rebound` (from F4, F5, F2): In an agitated market, the larger a coin's one-day fall, measured as its percent change from the previous close, the larger its rise over the next day, only when the coin also fell on the day before.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
