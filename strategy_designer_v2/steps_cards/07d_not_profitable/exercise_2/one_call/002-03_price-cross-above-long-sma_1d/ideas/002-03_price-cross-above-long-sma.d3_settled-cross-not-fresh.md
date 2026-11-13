---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The upward drift after the close crosses above the 200-day SMA appears once the close has stayed well above the average, and is reversed in the first bars just above it.
Consequence: Wait for the close to settle clearly above the average before entering, rather than buying the first bars after the cross.
Why:
- F3: The smallest forecasts, just after the cross, lose: forecast 0–5 bars averaged −0.00043 a day in book return and −0.25% over 20 bars, with a 38.8% hit rate; forecast-20 bars earned +0.0062 a day and +7.8% over 20 bars.
- F4: The trades lose because they are cut short by whipsaw, not because of fees. All 2228 trades are long and only 29.7% win before fees, with a median hold of 11 days. The 1483 trades held 20 days or less lost 4.3% to 6.4% each before fees, while the 742 held longer than 20 days earned 9.3% and 60.8%. Fees were only 0.31 per trade, against a mean gross gain of 4.23%.
