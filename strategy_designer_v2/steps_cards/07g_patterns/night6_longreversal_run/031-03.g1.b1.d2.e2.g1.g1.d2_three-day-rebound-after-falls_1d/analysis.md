---
line: 7.g patterns
backtest: 031-03.g1.b1.d2.e2.g1.g1.d2_three-day-rebound-after-falls_1d
idea tested: 031-03.g1.b1.d2.e2.g1.g1.d2_three-day-rebound-after-falls
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4054 USD
---
## Findings
- **F1:** XMR's one-day return scaled by its 30-day volatility predicts the next day's return against it: correlation −0.099 (t −4.91, 2,417 non-overlapping 1-day cases); the bottom quintile (falls below −0.68 usual moves) is followed by +0.80 % excess (t 3.73, 484 cases), the top quintile (rises above +0.74) by −0.44 % (t −2.27, 484 cases).
- **F2:** The reversal fades with the horizon: the same scaled move has a correlation t of −2.46 over 3 days (785 cases) and −2.25 over 2 days, and is gone over 10 days (t +0.50, 234 cases). The 3-day horizon tested keeps only part of an effect that is mostly over within one day.
- **F3:** The one-day reversal grows with how far 30-day volatility stands above its six-month level: correlation of scaled move with the next day's scaled return −0.041 (t −0.90, 486 cases) in the lowest volatility-ratio tercile (median 0.66), −0.104 (t −2.30) in the middle one (median 0.94) and −0.115 (t −2.54) in the highest (median 1.16).
- **F4:** The reversal is negative in 6 of 8 years (2018 t −1.87, 2020 t −4.34, 2024 t −1.75; 2019 +0.18 and 2025 +0.36 the exceptions), so no single year carries it alone, although 2020 is the strongest.
- **F5:** Where the close sits in the day's range carries the same next-day reversal: correlation −0.094 (t −5.10, 2,898 cases); closes in the bottom fifth of the range are followed by +0.85 % excess (t 4.17), closes in the top fifth by −0.60 % (t −3.33); over 2 days its correlation t is −2.95, against −2.25 for the scaled move. With the scaled move in the same regression the close location adds little (t −0.86 against −1.93), but on down days alone it still grades the rebound (correlation t −2.06; lowest quarter +0.68 % excess, t 2.39).
- **F6:** A combined score (scaled fall plus close near the low) puts its top quintile at +0.93 % mean next-day return (+0.82 % excess, t 3.99, 484 cases), about 3 times the 0.31 % cost of a trade; the bottom quintile gives −0.44 % excess (t −2.29).
- **F7:** The book mostly holds the coin rather than the signal: its daily returns correlate 0.77 with the coin's, it is in a position on 88 % of days, and 35 % of bars carry a positive allocation with a zero forecast. In 15 of 24 windows its summed daily return is below the coin's (w11: +0.44 against +1.35).
- **F8:** Friday and Saturday next-day returns are positive (+0.42 %, t 2.43; +0.59 %, t 2.96, about 413 cases each), but in 2018–2021 neither reaches t 2 (Friday t 0.48, Saturday t 1.18). It was one of about twenty angles examined and supports no idea.

## Ideas
- `031-03.g1.b1.d2.e2.g1.g1.d2.g1_one-day-scaled-move-reversal` (from F1, F2, F3, F4, F6): The larger XMR's one-day move against its 30-day daily volatility, the more its price moves back the other way over the next day: up after scaled falls, down after scaled rises. The lean grows with how far its 30-day volatility stands above its usual level over the past six months.
- `031-03.g1.b1.d2.e2.g1.g1.d2.g2_close-location-next-day-reversal` (from F5, F6): The nearer XMR closes to the low of its day's range, the more its price rises over the next one to two days; the nearer it closes to the high, the more it falls.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
