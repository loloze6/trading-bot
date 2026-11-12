---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.d not profitable
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a daily close at a new 60-day high, the coin keeps rising over the following days, more than from its other bars.
Consequence: A trader would buy fresh 60-day-high closes rather than the slow 50/200 spread, and refuse longs while price sits far below its recent high.
Why:
- F4: On active bars, the next-day return rises with closeness to the 60-day high.
- F8: The forecast misses gains while flat. Flat bars with positive 20- and 60-day momentum return 0.0027 next day (t=2.03, n=1027), above the 0.0013 of active bars.
- F2: Inside the active (50>200) state, the gain sits only where 20-day and 60-day momentum are both positive.
