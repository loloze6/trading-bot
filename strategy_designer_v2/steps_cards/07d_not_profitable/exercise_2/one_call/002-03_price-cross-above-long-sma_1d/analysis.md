---
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma_1d
idea tested: 002-03_price-cross-above-long-sma
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3078 USD
---
## Findings
- **F1:** Nearly all of the book's gain comes from active bars where both the 200-day SMA is rising (20-bar slope > 0) and 20-day momentum is positive: they summed +18.83 in daily book return over 3710 bars (mean +0.0051 a day), while active bars with a falling SMA and falling momentum summed −2.38 over 1916 bars (mean −0.0012 a day).
- **F2:** Being above a falling 200-day SMA does not pay: active bars with a falling SMA averaged −0.00073 a day in book return and +0.8% over the next 20 bars, against +0.0029 a day and +5.1% when the SMA was rising; inside the falling-SMA group, the largest forecasts (12–20) did worst, at −0.0030 a day and −1.1% over 20 bars.
- **F3:** The smallest forecasts, just after the cross, lose: forecast 0–5 bars averaged −0.00043 a day in book return and −0.25% over 20 bars, with a 38.8% hit rate; forecast-20 bars earned +0.0062 a day and +7.8% over 20 bars.
- **F4:** The trades lose because they are cut short by whipsaw, not because of fees. All 2228 trades are long and only 29.7% win before fees, with a median hold of 11 days. The 1483 trades held 20 days or less lost 4.3% to 6.4% each before fees, while the 742 held longer than 20 days earned 9.3% and 60.8%. Fees were only 0.31 per trade, against a mean gross gain of 4.23%.
- **F5:** Being active while 20-day momentum is negative loses: those 4713 active bars averaged −0.00055 a day in book return, against +0.0040 for the 4746 active bars with positive momentum. With negative momentum, even forecasts of 12–20 lost (−0.0012 a day).
- **F6:** Volatility is not the cause, because active bars earned in every volatility tercile (calm +0.0013, mid +0.0017, wild +0.0037 a day). The poor Calmar of 0.14 comes from the allocation reaching up to 2.2x: in windows w11, w17 and w21 the book's average maximum drawdown (−0.55, −0.54, −0.42) was deeper than the coin's (−0.33, −0.35, −0.24).
- **F7:** Losses cluster in years when the coin barely trends: in 2023 the book lost −0.00027 a day while the coin gained +0.0015 and the book was active 68% of the time; in 2018 and 2022 the book also lost (−0.0007 and −0.0004 a day).

## Ideas
- `002-03_price-cross-above-long-sma.d1_rising-average-confirms-trend` (from F1, F2, F7): A coin whose close is above its 200-day SMA keeps rising over the next weeks when that SMA has itself risen over the last 20 bars.
- `002-03_price-cross-above-long-sma.d2_momentum-confirmed-persistence-above-average` (from F1, F5): A coin trading above its 200-day SMA keeps drifting up when its close is also higher than 20 bars ago, which shows the move is still being extended by late buyers.
- `002-03_price-cross-above-long-sma.d3_settled-cross-not-fresh` (from F3, F4): The upward drift after the close crosses above the 200-day SMA appears once the close has stayed well above the average, and is reversed in the first bars just above it.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
