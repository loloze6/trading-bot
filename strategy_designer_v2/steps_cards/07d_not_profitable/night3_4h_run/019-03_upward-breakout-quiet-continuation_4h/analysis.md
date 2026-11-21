---
line: 7.d not profitable
backtest: 019-03_upward-breakout-quiet-continuation_4h
idea tested: 019-03_upward-breakout-quiet-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3382 USD
---
## Findings
- **F1:** The book misses its Calmar target by a hair: 0.749 against 0.75 (34.1 % a year, deepest fall 45.5 %). The deepest fall runs from w5 to w10 over 556 days, with the book down 33.8 % while the coins fell 52.3 %.
- **F2:** The quieter a coin's past seven days were against its past 60 days, the better its breakout entries did. Entries in the quietest quarter (7-day mean bar range at 0.32 to 0.76 of the 60-day one) returned +1.47 % over 18 bars (t 2.66, 236 entries) and fell 4.2 % at worst along the way. The other three quarters returned only +0.24 % to +0.44 % (t ≤ 0.69) and fell 5.2 % to 6.5 %, out of 1919 entries from flat.
- **F3:** The falls come from breakouts made while the coin was already turbulent. Inside the fall windows w5 to w10, entries in the two highest 7-day/60-day range quarters lost −0.27 % and −0.46 % over 18 bars (136 entries). The two quietest quarters gained +1.90 % and +0.90 % there, and those losing entries were held at larger positions (1.26 to 1.34 of the book).
- **F4:** The quiet-week edge holds across time and coins. The quietest quarter gives +1.48 % in w1 to w12 and +1.45 % in w13 to w24 (t 1.81 and 2.01). It is positive on all six coins (+0.70 % on LTC to +2.00 % on XRP), and it is the best quarter on five of them.
- **F5:** Breakouts after a falling week do worse than those after a rising one. Entries in the lowest quarter of the 7-day return (−35 % to −3.5 %) lost −0.43 % over 18 bars, while the two upper quarters gained +0.86 % and +1.02 % (t 2.01 and 1.87). Among the quietest-quarter entries, those after the stronger half of the 7-day return gained +1.73 % (t 2.45, 131 entries).
- **F6:** The tested idea's own move is barely above a trade's cost: +0.20 % unusual move per case, 1.1 times the 0.19 % cost of a trade. Entries in the quietest-week quarter carry a total move of +1.47 %, which is about +1.06 % above the coin's +0.41 % normal drift, so about 5.5 times the cost.

## Ideas
- `019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week` (from F1, F2, F3, F4, F6): When a four-hour bar closes above the highest high of a coin's preceding two-day narrow stretch, the coin rises over the next three days. The rise is larger the narrower that stretch was compared with the coin's 30-day average four-hour range, and larger still the quieter the coin's average four-hour range over the past 7 days was compared with its average over the past 60 days.
- `019-03_upward-breakout-quiet-continuation.d2_breakout-with-rising-week` (from F1, F5, F6): When a four-hour bar closes above the highest high of a coin's preceding two-day narrow stretch, the coin rises over the next three days. The rise is larger the narrower that stretch was compared with the coin's 30-day average four-hour range, and larger the higher the coin's 7-day return at the breakout.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
