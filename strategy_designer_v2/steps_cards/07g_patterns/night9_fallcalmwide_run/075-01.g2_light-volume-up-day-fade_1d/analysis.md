---
line: 7.g patterns
backtest: 075-01.g2_light-volume-up-day-fade_1d
idea tested: 075-01.g2_light-volume-up-day-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6003 USD
---
## Findings
- **F1:** Up days in a falling market fall the next day at every volume level, so volume does not drive the move. With the trend read as the 30-day return below −10 %, up days in volume quintiles 0 to 4 have next-day unusual moves of −1.27 % (t −2.78, n 351), −0.84 % (t −2.17), −0.65 % (t −1.70), −0.84 % (t −1.67) and −1.40 % (t −2.09, n 220). In a rising 30-day trend the same quintiles give +0.16, −0.49, +0.03, −0.04 and +0.59 %, and in a choppy one −0.09 to −0.23 %, all with |t| ≤ 1.37.
- **F2:** Light-volume up days fall only outside rising markets. Over all trends, up days in volume quintiles 0 and 1 have unusual moves of −0.44 % (t −1.75) and −0.48 % (t −2.22), against −0.17 % and −0.07 % in quintiles 3 and 4. With the 60-day trend, the light half falls −0.63 % in falling markets (t −1.80, n 560) and −0.52 % in choppy ones (t −1.53), but −0.004 % in rising ones (t −0.01, n 486). Within up days, the covariance of volume with the next-day move is +11.0e-4 with t 1.02, so there is no smooth gradient; this matches the verdict's failed thirds check (top minus bottom −0.05 %).
- **F3:** The fade sits on small rises: up days in the lowest tercile of the day's return over its 20-day standard deviation have unusual moves of −0.60 % (t −1.83), −0.55 % (t −2.03) and −0.05 % to −0.52 % across volume quintiles, while the largest-rise tercile sits near 0 in every volume quintile (−0.61 % with n 93, then +0.03, −0.12, +0.03, +0.03 %).
- **F4:** Heavy-volume down days rebound, and the rebound grows with volume. Down days in volume quintiles 0 to 4 have next-day unusual moves of +0.15 %, +0.16 %, +0.19 %, +0.34 % and +1.15 % (t 2.59, n 955). The quintile-4 mean is positive in all 12 windows shown, ranging from +0.14 % to +2.84 %.
- **F5:** Among heavy-volume down days (quintile 4), the lower the close in the day's range, the larger the rebound: the bottom close tercile gives +1.75 % (t 2.77, n 319), the middle +1.18 % (t 1.99) and the top +0.52 % (t 0.61). Over all days, the close-location quintiles also fall in order, from +0.60 % (t 1.78) to −0.35 % (t −1.52).
- **F6:** The book lost because its short fought the coins' drift. Its total move per case is +0.11 %, against an unusual move of +0.26 %, after a normal drift of −0.15 % in the short direction. That total is half the 0.22 % cost of a trade, giving a Sharpe of −0.39 and −4.2 % a year. The falling-market up days in F1 move −0.65 % to −1.40 % per case, three to six times that cost.

## Ideas
- `075-01.g2.g2_falling-market-light-rise-fade` (from F1, F2, F6): In a falling market, on a day a coin rises, the lighter its volume against its average daily volume over the past 20 days, the larger its fall over the next day.
- `075-01.g2.g3_heavy-volume-low-close-rebound` (from F4, F5): On a day a coin falls and closes in the lower part of its range, the heavier its volume against its average daily volume over the past 20 days, the larger its rise over the next day.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `075-01.g2.g1_falling-market-small-bounce-fade` (from F1, F3, F6): In a falling market, the smaller a day's rise against the coin's usual daily move over the past 20 days, the larger its fall over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
