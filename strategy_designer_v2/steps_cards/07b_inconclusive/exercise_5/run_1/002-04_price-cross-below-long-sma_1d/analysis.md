---
line: 7.b inconclusive
backtest: 002-04_price-cross-below-long-sma_1d
idea tested: 002-04_price-cross-below-long-sma
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.4213 USD
---
## Findings
- **F1:** The short excess return sits only in the shallow half of the below-average bars, where the close is just under its 200-day SMA: over 10 days, shallow blocks give mean excess -0.0118 (t -1.91, n 420) against +0.0049 in deep blocks (t 0.66, n 421), a shallow-minus-deep Welch t of -1.72. The plan's forecast sizes the short larger the deeper the close sits, which points the opposite way and explains its negative slope of -0.0126 and pooled t of -0.23.
- **F2:** The shallow fall is present in all six coins at 10 days, with means from -0.0045 (LTC) to -0.0205 (BTC), but no single coin reaches |t| 1.6. So the effect is consistent in direction and small against a 10-day excess-return standard deviation of 0.141.
- **F3:** The shallow fall is clearest when the close has been sinking further below the average over the past 10 days: mean 10-day excess -0.0199 (t -2.06, n 188), against -0.0051 (t -0.65) when it has been recovering.
- **F4:** Deep-below bars reverse upward in some years and some states. Deep 10-day excess is +0.109 (t 4.74) in 2020, +0.116 (t 2.70) in 2021 and +0.064 (t 2.27) in 2024. It is also +0.038 (t 1.81) when the 50-day SMA slope is flat or rising, while deep in low volatility falls (-0.032, t -2.02). This mixes downward persistence with rebounds.
- **F5:** The effect is mixed across periods. The pooled position x excess product by year runs from +0.0121 (2018) to -0.0227 (t -3.46, 2020), and shallow excess is strongly negative only in 2018 (-0.074, t -3.08) and 2022 (-0.066, t -4.03).
- **F6:** The book's mean daily return of -0.000281 is almost entirely the market's own rise against the short (-0.000280); timing adds only -0.0000008. The strategy captured no timing at all.

## Ideas
- `002-04_price-cross-below-long-sma.b1_fresh-break-below-sma200` (from F1, F2, F3, F6): While a coin's close is below its 200-day simple moving average, the closer it sits under the average and the more its distance below has widened over the past 10 days, the further the coin falls beyond its average over the next 10 days.
- `002-04_price-cross-below-long-sma.b2_deep-below-sma200-rebounds` (from F1, F4): While a coin's close is far below its 200-day simple moving average and that average has stopped falling over the past 50 days, the deeper the close sits under the average, the more the coin rises beyond its average over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
