---
line: 7.g patterns
backtest: 031-03.g1.b1.d2.e2.g1.g1_reversal-scaled-by-volatility-excess_1d
idea tested: 031-03.g1.b1.d2.e2.g1.g1_reversal-scaled-by-volatility-excess
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3957 USD
---
## Findings
- **F1:** XMR's next-day reversal comes almost entirely from down days. The fade slope of next-day excess return on minus the volatility-scaled one-day return is 0.0068 (t 3.37, 1133 down days) after down days and 0.0016 (t 0.94, 1282 up days) after up days. Among down days, the largest-fall quintile is followed by +0.95 % (t 2.85, 227) and the next quintile by +0.73 % (t 2.45, 226); the three milder quintiles give between −0.22 % and +0.23 %.
- **F2:** The book's shorts carry its losses. Short trades average −0.81 % net (1370 trades, median −0.22 %) against −0.13 % for longs (1236 trades, median +0.19 %), which matches the up-day fade being indistinguishable from 0.
- **F3:** Where the day closes in its range forecasts the next day. The slope of next-day excess return on close location ((close−low)−(high−close))/(high−low) is −0.0076 (t −5.10, 2897 bars). The quintile closing nearest the low is followed by +0.85 % (t 4.17, 580) and the one nearest the high by −0.60 % (t −3.33, 580). The slope is negative in both halves of the windows (t −2.81 and −4.33) and in 7 of 8 years. On non-overlapping 2-day returns it is −0.0072 (t −2.57, 1442).
- **F4:** The close-location effect is strongest on wide-range days. Its slope is −0.0115 (t −3.86, 806) in the tercile whose range is 1.6 times its 30-day average, against −0.0048 (t −1.95) and −0.0035 (t −1.39) in the narrower terciles. It is also stronger on down days (−0.0082, t −2.37) than on up days (−0.0036, t −1.30). It overlaps the scaled return, though: fitted together, close location keeps a slope of −0.0031 (t −1.43) and the scaled return −0.0031 (t −2.45).
- **F5:** The fade does grow with elevated volatility, as the tested idea says. Its slope is 0.0082 (t 3.87, 454) in the highest volatility-ratio tercile (ratio 1.32), against 0.0025 (t 1.42) and 0.0028 (t 1.38) in the lower two.
- **F6:** The reversal lasts only a few days, and the brief's two-to-three-month move shows nothing at these horizons.

## Ideas
- `031-03.g1.b1.d2.e2.g1.g1.g1_xmr-fades-sharp-falls-only` (from F1, F2, F5): The larger XMR's one-day fall against its 30-day daily volatility, the more its price rises over the next day, and more so when its 30-day volatility stands above its six-month norm.
- `031-03.g1.b1.d2.e2.g1.g1.g2_xmr-close-in-range-reversal` (from F3, F4): The nearer XMR closes to the low of its day's range, the more its price rises over the next day, and the nearer it closes to the high, the more it falls; the effect grows with how wide the day's range is against its 30-day average range.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
