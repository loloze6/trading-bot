---
line: 7.d confirmed, not profitable
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise_1d
idea tested: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3900 USD
---
## Findings
- **F1:** The tested book's deepest fall (−35.3 %, over 201 days from w1 into w3, while the coins fell −62.5 %) comes from the heavy-volume days on which the coin closed up. On those signal bars the next-day excess return is −0.05 % (t −0.56, n 3409), and in w1–w3 they summed a gain of −0.93 against +0.08 for the down-day signal bars. A book trading only up-day signals has Sharpe 0.03, Calmar −0.02 and its deepest fall at −42.4 %.
- **F2:** The heavy-volume days on which the coin fell carry the effect: next-day excess +0.41 % (t 4.33, n 3294) against −0.05 % on up days. Restricted to those days, the book (rebuilt with 0.19 % per round trip) moves from the full book's figures to these:
- **F3:** Inside the heavy-volume down days the move grows with the size of the day's fall:
- **F4:** Where the day closed in its range points the same way, as the brief's absorption theory reads it:
- **F5:** The forecast's grade holds and concentrates the move:
- **F6:** Down-day signals lose in one year only:

## Ideas
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day` (from F1, F2, F3, F5, F6): The heavier a coin's volume on a day relative to its own prior 20-day average, the more the coin rises over the next day, when that day was a down day, and the more so the larger the day's fall.
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close` (from F1, F4, F5): The heavier a coin's volume on a day relative to its own prior 20-day average, the more the coin rises over the next day, the lower the day's close sits within its high-low range.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
