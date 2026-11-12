---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-05_sma-up-regime-positive-drift
line: 7.c rejected
backtest: 002-05_sma-up-regime-positive-drift_1d_minus1pct
instruments: BTC/USDT
bar: 1d
period: fold A
---
Idea: On a single coin's daily bars, while the 50-day SMA is above the 200-day SMA, the drop comes in the gap from one day's close to the next day's open, and the next day's open-to-close return is flat to slightly positive.
Consequence: Any position taken against the stretch should be held over the close-to-open gap, because the intraday session alone carries none of the effect.
Why:
- F6: The whole in-stretch loss sits in the gap from the close to the next open. That gap averaged -1.00% in-stretch against -0.001% outside, while the next bar's open-to-close averaged +0.11% in-stretch against -0.03% outside.
- F8: The pattern is unusually even, which suggests a planted -1%-per-bar effect (the record's name ends in "minus1pct"); a reader should treat the result as a test case more than a market fact. Friday in-stretch bars had a next-bar sd of only 0.9% and 12% up bars. No trades were recorded.
