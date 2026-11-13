---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: Once a coin's close has stayed above its 200-day SMA for more than about 20 consecutive bars, the coin keeps rising over the next 20 bars by more than its average 20-bar return. In the first 5–20 bars after the close moves above the SMA, the coin does worse than its average.
Consequence: Hold long only after an above-SMA episode has lasted past its first weeks, and skip the fresh crosses that the book now trades and loses on.
Why:
- F5: The book's gain sits entirely in long holds: 2228 trades, all long, with a 29.7% gross win rate and a median hold of 11 days; every duration class up to 30 days loses on average (-6.1%, -6.4%, -5.7% and -2.3% gross, summing to about -8040%), while the 515 trades held over 30 days make +33.9% each, summing to +17472%.
- F7: The 331 trades closed by a window's end average +43.9% gross, against -2.7% for all other trades, so the trades the signal itself exits lose money on average.
- F8: Young above-SMA episodes lose: bars 5–20 bars into an episode carry a mean allocation of 0.97 and earn -8.0 bp a day (sum -1.67), while episodes aged 20–60 and 60–150 bars earn +25.3 and +44.9 bp a day.
