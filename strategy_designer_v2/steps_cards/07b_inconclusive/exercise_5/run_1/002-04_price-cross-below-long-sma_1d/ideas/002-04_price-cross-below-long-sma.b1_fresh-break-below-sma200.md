---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-04_price-cross-below-long-sma
line: 7.b inconclusive
backtest: 002-04_price-cross-below-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close is below its 200-day simple moving average, the closer it sits under the average and the more its distance below has widened over the past 10 days, the further the coin falls beyond its average over the next 10 days.
Consequence: A trader would short a fresh, deepening break of the 200-day average and size by nearness to it, not by depth below it.
Why:
- F1: The short excess return sits only in the shallow half of the below-average bars, where the close is just under its 200-day SMA: over 10 days, shallow blocks give mean excess -0.0118 (t -1.91, n 420) against +0.0049 in deep blocks (t 0.66, n 421), a shallow-minus-deep Welch t of -1.72. The plan's forecast sizes the short larger the deeper the close sits, which points the opposite way and explains its negative slope of -0.0126 and pooled t of -0.23.
- F2: The shallow fall is present in all six coins at 10 days, with means from -0.0045 (LTC) to -0.0205 (BTC), but no single coin reaches |t| 1.6. So the effect is consistent in direction and small against a 10-day excess-return standard deviation of 0.141.
- F3: The shallow fall is clearest when the close has been sinking further below the average over the past 10 days: mean 10-day excess -0.0199 (t -2.06, n 188), against -0.0051 (t -0.65) when it has been recovering.
- F6: The book's mean daily return of -0.000281 is almost entirely the market's own rise against the short (-0.000280); timing adds only -0.0000008. The strategy captured no timing at all.
