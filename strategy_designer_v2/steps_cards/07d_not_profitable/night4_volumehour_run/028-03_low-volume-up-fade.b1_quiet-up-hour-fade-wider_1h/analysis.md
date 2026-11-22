---
line: 7.d not profitable
backtest: 028-03_low-volume-up-fade.b1_quiet-up-hour-fade-wider_1h
idea tested: 028-03_low-volume-up-fade.b1_quiet-up-hour-fade-wider
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4022 USD
---
## Findings
- **F1:** The book cannot pay at this size: per case the total move over 6 hours is +0.004 % and the unusual move +0.038 % (t 2.10, 19 445 cases), against a cost of 0.19 % per trade, while the book's trades lose 0.29 % to 0.74 % per trade before fees on every coin (BTC −0.29 %, ZEC −0.74 %), so its mean daily return is −0.10 %.
- **F2:** The book is short against coins that rise, which costs it on the failing Sharpe-against-holding measure: its mean position is short on every coin (−0.11 on ZEC to −0.26 on BTC, short 40–45 % of bars), the coins' mean daily return is +0.07 % to +0.16 %, and the book's mean daily return is −0.08 % to −0.14 % per coin.
- **F3:** The fade is concentrated in signals in the first four UTC hours of the day (00–04 UTC): there the unusual move is +0.106 % over 6 hours (t 2.54) and +0.209 % over 12 hours (t 3.46, 3 189 cases), while in the next block (04–08 UTC) it is −0.056 % and −0.125 %.
- **F4:** Inside those 00–04 UTC signals the fade is graded by the size of the rise: the two largest-rise quintiles give +0.35 % and +0.34 % over 12 hours (t 2.27 and 2.26, total move +0.28 % and +0.27 %, about 1.4 times the cost), and the smallest-rise quintile gives −0.01 %.
- **F5:** The fade over 12 hours holds only after flat or falling 3-day returns: the unusual move is +0.117 % (t 2.57) and +0.072 % (t 1.66) in the second and middle quintiles of the 3-day return, and −0.085 % (t −1.79) and −0.034 % in the two highest, where the total move of the short is −0.15 % (t −3.21) and −0.10 %.
- **F6:** The fade weakens as the hour's volume approaches the top of the ordinary band: the unusual move is +0.043 % over 1 hour (t 2.86) and +0.058 % over 6 hours (t 1.63) in the lowest volume-ratio quartile, and −0.002 % and −0.005 % in the highest (1.2 to 2.6 times average volume).
- **F7:** Beyond 12 hours the fade reverses: over 24 hours the unusual move is −0.048 % overall, and after the weakest prior 24-hour returns it is −0.27 % (t −2.87), so holding past half a day gives the gain back.

## Ideas
- `028-03_low-volume-up-fade.b1_quiet-up-hour-fade-wider.d1_post-midnight-quiet-rise-fade` (from F1, F3, F4, F7): After an hour in which the coin rises far more than its typical hourly move over the past 30 days while its volume stays near its average hourly volume over the past 30 days, the price gives back part of that rise over the next twelve hours, only when that hour falls in the first four hours of the UTC day; the larger that hour's rise, the larger the giveback.
- `028-03_low-volume-up-fade.b1_quiet-up-hour-fade-wider.d2_quiet-rise-fade-no-uptrend` (from F2, F5, F1): After an hour in which the coin rises far more than its typical hourly move over the past 30 days while its volume stays near its average hourly volume over the past 30 days, the price gives back part of that rise over the next twelve hours, only while the coin has fallen or held flat over the past 3 days; the larger that hour's rise, the larger the giveback.
- `028-03_low-volume-up-fade.b1_quiet-up-hour-fade-wider.d3_thinner-volume-larger-fade` (from F6, F1): After an hour in which the coin rises far more than its typical hourly move over the past 30 days while its volume stays near its average hourly volume over the past 30 days, the price gives back part of that rise over the next six hours, and the giveback grows both with the size of that hour's rise and with how far that hour's volume falls below its 30-day average.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
