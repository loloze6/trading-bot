---
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday_1d
idea tested: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 3.9319 USD
---
## Findings
- **F1:** A Sunday close above Saturday's is followed by a fall over the next 2 days: on the non-overlapping grid the excess 2-day return after a Sunday rise is −2.04 % (t −8.6, 1081 cases). After a rise on any other day it is between −0.89 % (Tuesday) and +0.88 % (Saturday, t 4.6). Averaged across coins per Sunday it is −0.87 % (t −2.30, 310 Sundays), and it is negative in 17 of 19 coins.
- **F2:** The Sunday-rise reversal is large against the cost of a trade. In the short direction its unusual move is +1.0 % per case over 2 days, a strength of 0.135 (2147 cases), about 4.5 times the 0.22 % cost. It starts on Monday (excess 1-day return −0.50 %, t −4.17) and keeps building to −1.17 % over 4 days (t −5.10).
- **F3:** The Sunday-rise reversal is graded by Sunday's volume relative to the coin's 60-day average volume. The 2-day excess return is −1.39 % in the lowest volume tercile (t −5.6, 716 cases), −0.83 % in the middle one (t −2.9) and −0.79 % in the highest (t −2.3).
- **F4:** The Sunday-rise reversal is not graded by the size of the rise. The smallest third of rises is followed by −1.42 % (t −4.7), the middle third by −0.83 % and the largest third by −0.76 %. It belongs to Sunday's own bar: measured on the Saturday-plus-Sunday 2-day rise it shrinks to −0.39 % per Sunday (t −1.12, 324 Sundays), and the Friday-to-Sunday 3-day return has no slope (t −0.50).
- **F5:** The tested side, the Sunday fall, is weaker and graded only in its tail. The largest third of Sunday falls is followed by +1.14 % over 2 days (t 3.73) and +1.84 % over 4 days (t 3.91), but the smallest third by −0.28 %. The per-Sunday t of the tested measure is −0.55, and by year the fall's excess return runs from +2.66 % (2020) to −0.68 % (2025).
- **F6:** In the book, Sunday days lose −0.024 % (t −8.0, 5264 coin-days), Sunday being the day the position is entered and its fee paid, and Monday days earn +0.100 % (t 4.08). The book's profit sits on the Monday after entry.
- **F7:** Across all weekdays, the excess 2-day return after a large fall (below −2 of the coin's usual daily move) is +0.64 % (t 1.98, 385 cases). It reaches +2.55 % in the highest volatility tercile (t 2.37), but swings by year from +7.1 % (2021) to −2.4 % (2022). Given how many angles were looked at, this is not distinguishable from chance.

## Ideas
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.g1_thin-sunday-rise-reverses` (from F1, F2, F3, F4, F6): A coin whose Sunday close is above its Saturday close falls over the next 2 days, and the lower Sunday's traded volume is relative to the coin's 60-day average daily volume, the larger that fall.
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.g2_sunday-rise-four-day-reversal` (from F2, F3, F4): A coin whose Sunday close is above its Saturday close falls over the next 4 days, and the lower Sunday's traded volume is relative to the coin's 60-day average daily volume, the larger that fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
