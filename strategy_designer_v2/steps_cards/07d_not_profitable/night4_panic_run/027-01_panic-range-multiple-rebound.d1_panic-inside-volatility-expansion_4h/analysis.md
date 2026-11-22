---
line: 7.d not profitable
backtest: 027-01_panic-range-multiple-rebound.d1_panic-inside-volatility-expansion_4h
idea tested: 027-01_panic-range-multiple-rebound.d1_panic-inside-volatility-expansion
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3706 USD
---
## Findings
- **F1:** The book's deepest fall is −76.5 % against a yearly return of 26.8 % (Calmar 0.34). The fall ran 277 days across windows w12 to w14, while the coins fell −79.0 % together. So the book fell almost exactly as much as the coins did.
- **F2:** The book is long on 98.7 % of bars on average (median 99.9 % per coin-window), with a mean allocation of 1.07. Its forecast is positive on only 48.9 % of bars, so on 50.2 % of bars it is long with a forecast of zero. Trades last a median of 78 days, against the 14-day horizon. In practice the book is the coin held with leverage, and its falls are the coin's falls.
- **F3:** On the 84-bar grid, the long bars that carry a forecast of zero (517 cells) have an unusual move of +0.01 %. These long-but-no-signal bars, which are half the book's exposure, add drift and drawdown but no timing.
- **F4:** The effect depends on the 7-day/60-day volatility ratio at the signal bar:
- **F5:** Forecast size separates the cases only slightly. Cases with a forecast of 7.2 to 20 (n 859) have +0.11 %, against −0.52 % for 2.0 to 7.2 (n 287). The cubed product of range multiple and volatility ratio lets ratios below 1 still give full-size signals.
- **F6:** The 180-bar trend before the panic does not order the cases. By quartile of the prior 30-day return, the unusual move is −1.05 %, +1.10 %, −0.32 % and −0.08 %, all with |t| < 0.9.

## Ideas
- `027-01_panic-range-multiple-rebound.d1_panic-inside-volatility-expansion.d1_panic-premium-above-normal-turbulence` (from F1, F2, F3, F4, F5): When a coin falls over a 24-hour stretch and its high-low range over that stretch is a large multiple of its average 24-hour range over the past 30 days, it earns more than its usual return over the next 14 days, only while its volatility over the past 7 days is above its volatility over the past 60 days, the excess growing with how far that ratio stands above it, and the premium is concentrated in those 14 days after the panic.
- `027-01_panic-range-multiple-rebound.d1_panic-inside-volatility-expansion.d2_calm-market-drops-keep-falling` (from F4, F1): When a coin falls over a 24-hour stretch with a wide high-low range while its volatility over the past 7 days is low against its volatility over the past 60 days, it earns less than its usual return over the next 14 days, the lower that volatility ratio, the weaker the return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
