---
line: 7.d confirmed, not profitable
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise_1d
idea tested: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5683 USD
---
## Findings
- **F1:** The failing measure is the falls. The book's deepest fall was -58.4 %, from w12 to w14 over 276 days, while the coins fell -81.2 %; its second was -54.0 %, from w1 to w3 over 309 days, while the coins fell -66.4 %; both were long bear stretches (book mean daily return -0.17 % in 2018 and -0.13 % in 2022), against a yearly return of +31.1 %, giving a Calmar of 0.53 against the 0.75 required.
- **F2:** The book stays long almost all the time: it is in a position on 90 % of the coins' days, holds a mean allocation of 0.49 even on grid bars with no signal, and 85 % of grid bars carry a long allocation, so in a bear market it takes most of the coin's fall.
- **F3:** The gain sits on the days the volume is heavy, not on the 10 days held after them: on bars with a positive forecast (6703) the next day's coin return is +0.29 % and the position's gain +0.25 % per bar (summed 16.8); on the bars held within 10 days after a signal (9423), the next day's coin return is +0.003 % and the gain +0.035 % per bar (summed 3.3), so most of the exposure that carries the falls earns almost nothing.
- **F4:** Holding is already too long at 10 days. On the 10-day grid the strongest forecast bucket (>1.5) has a mean excess of +1.03 % (t 1.58, n 639); on the 20-day grid it has only +0.41 % (t 0.29, n 284). Cutting the hold to 5 bars raised Calmar only to 0.58 (deepest fall -55.5 %), so the gain lies at a horizon shorter than the holds tested.
- **F5:** Where the day closes inside its range sharpens the effect. A heavy-volume day closing in the low third of its range is followed by a 10-day excess of +1.47 % (t 1.77, n 230), against +0.69 % for a mid close (n 224) and +0.43 % for a high close (n 254). The low close alone does not explain this: without a volume surge, a low close is followed by -2.00 % (t -2.25, n 275). This fits the brief's theory of absorption, where a seller finishes near the close and the pressure is gone.
- **F6:** A trend filter is not a repair. Keeping the book only above its 50-day mean cuts the deepest fall to -42.0 %, but Calmar reaches only 0.585, and the condition is an effect of its own: above the 50-day mean the next-day return is +0.217 % without a recent signal (n 239) and +0.225 % with one (n 6233). On the grid, above the mean, the excess is +0.51 % without a signal against +1.09 % with one, so the trend earns about half the move by itself.
- **F7:** The size of the idea covers its cost. The total move per case (+1.61 %) is 8.3 times the 0.19 % cost of a trade, and the unusual move (+0.43 %) is 2.2 times it, so the book fails on the falls it carries, not on fees.

## Ideas
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d1_heavy-volume-low-close-rebound` (from F5, F1, F2, F7): The heavier a coin's volume on a day relative to its own prior 20-day average, and the nearer that day's close sits to the day's low, the more the coin rises over the next 10 days.
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise` (from F3, F4, F2, F1): The heavier a coin's volume on a day relative to its own prior 20-day average, the more the coin rises over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
