---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-04_price-cross-below-long-sma
line: 7.d not profitable
backtest: 002-04_price-cross-below-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a coin's close crosses below its 200-day average, the coin keeps falling, more the deeper it sits below the average, only while the coin's recent weeks have been flat to rising rather than a sharp fall.
Consequence: A trader should hold the short only after the selling has paused and cut it as the recent fall steepens, which removes the crash-rebound days behind the book's deepest losses.
Why:
- F2: The short loses most where the forecast is strongest. Short days in the lowest 20-bar momentum quintile (the coin fell most over the prior 20 bars) earn -0.001288 a day (t -1.91, n 1669) at a mean allocation of -0.44. The upper two quintiles earn +0.000058 and -0.000009, so even the short's best states only break even.
- F5: The book's worst days come from shorting after a crash. The worst 5% of short days (418) sum to -21.56, against a total of -3.77 over all short days. On those days the coin had fallen -14.0% over 20 bars (against -2.0% on all short days) and sat -34.2 below its average (against -15.3).
- F7: No state of the short makes the book pay. Short days with a falling 200-day average and positive 20-bar momentum earn +0.000006 a day (n 2410). Short days with a rising average and negative momentum earn -0.001203 (t -2.97, n 1509).
