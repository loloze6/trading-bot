---
line: 7.d confirmed, not profitable
backtest: 039-01_agitated-low-close-next-day-rebound_1d
idea tested: 039-01_agitated-low-close-next-day-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4087 USD
---
## Findings
- **F1:** The book fails on its mean daily return on days in a position (0.0143 % against 0.05 %) because its positions are tiny, not because the effect is too small. On agitated bars the mean absolute position is 0.092 of the book, and the median active position is 0.061. Each case moves 0.31 % in the signal's direction on the long side (t 2.68, 2783 bars) and 0.45 % on the short side (t 3.68, 2292 bars), but this reaches the book as only 0.043 % and 0.024 % per bar before fees. The fee drag is 0.0084 % per bar.
- **F2:** The gain sits at the ends of the range, and the middle of the range carries almost none of it. Agitated bars closing in the lowest tenth of the range return +0.90 % in the signal's direction over the next day (t 2.77, 323 bars), with a book gain of 0.12 % per bar. Bars closing between 25 % and 50 % below the high return only +0.105 % (t 0.65, 1323 bars), with a book gain of 0.0017 %. Closes in the outer 15 % at either end, which are 27 % of agitated bars, return +0.70 % signed (t 3.57, 990 cases).
- **F3:** The effect lives in falling markets and turns over in rising ones. With a 60-day return below -10 %, agitated low closes are followed by +3.15 % over the next day (100 bars). The falling trend alone earns nothing: falling bars with middle closes return -0.27 % (548) and with high closes -0.27 % (90). With a 60-day return above +10 %, the sign flips: low closes return -0.43 % (72) and high closes +0.42 % (147).
- **F4:** A wider day's range grades the rebound after a low close. In the widest third of agitated days' ranges, low closes are followed by +1.71 % (175 bars, 0.21 of a 20-day swing). In the middle third they return +0.30 % (117), and in the smallest third -0.05 % (87). The wide range alone earns little: wide days with middle closes return +0.32 % (867).
- **F5:** The deepest fall of the book, -5.1 %, ran 238 days from w11 to w13 while the coins rose 31 % on average. w11 and w12 are the only losing windows apart from the 15-bar w7, with book sums of -0.5 % and -1.1 %. In w11 the coins' summed daily return was +149 %. Shorts taken while the 20-day trend was positive lost money: -0.018 % gross per bar with the trend between 0 and +10 % (274 bars), and -0.005 % with it above +10 % (759 bars). This is the rising-market reversal of F3 working against the book.
- **F6:** Longs taken after an up day lose. Long bars after a 1-day return between 0 and +3 % return -0.50 % signed (t -2.52, 614 bars). Long bars after a 1-day fall deeper than 3 % return +0.98 % (t 4.66, 1066 bars). However, a down day alone earns nearly as much: down days with a middle close return +0.79 % (t 2.71). So the down day is the coin's own reversal, a separate effect, and is not used as a repair.
- **F7:** The slope of next-day excess return on close location is three times steeper in agitated markets (0.0185, t 4.82, 3691 bars) than in calm ones (0.0063, t 2.57, 4639 bars). This confirms the brief's agitated profile.

## Ideas
- `039-01.d1_falling-agitated-low-close-rebound` (from F3, F5, F7): In a falling, agitated market, the lower a coin closes within its day's high-low range, the larger its rise over the next day.
- `039-01.d2_wide-range-low-close-rebound` (from F4, F2, F1): In an agitated market, the lower a coin closes within its day's high-low range, the larger its rise over the next day, and the larger still the wider that day's high-low range is against its close.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
