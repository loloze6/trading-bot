---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-05_sma-up-regime-positive-drift
line: 7.c rejected
backtest: 002-05_sma-up-regime-positive-drift_1d_minus1pct
instruments: BTC/USDT
bar: 1d
period: fold A
---
Idea: On a single coin's daily bars, when the 50-day SMA is above the 200-day SMA but the close is below its level of 20 bars earlier, the next day's return is negative on average.
Consequence: A trader should refuse long entries when the long averages say up but the last 20 days fell.
Why:
- F7: Price fell over the prior 20 bars on 220 of the 246 in-stretch bars, while the long average stayed above. Those 220 bars averaged -0.78% next bar, and the 26 bars after a rising 20 days averaged -1.01%.
- F1: On BTCUSD daily bars, the 290 bars inside the 50-over-200 SMA stretch had a mean next-bar return of -0.85% against -0.03% on the 434 bars outside it (Welch t -4.14). Only 27% of in-stretch next bars closed up, against 48% outside, and the in-stretch median next bar was -1.06% against -0.06%.
