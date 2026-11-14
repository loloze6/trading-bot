---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-05_sma-up-regime-positive-drift
line: 7.a not observable
backtest: 002-05_sma-up-regime-positive-drift_1d
instruments: BTC/USDT
bar: 1h
period: fold A
---
Idea: On BTC hourly bars, the bars where the 50-bar SMA is above the 200-bar SMA (from an up-cross to the next down-cross) are followed by a higher mean next-hour return than the bars where it is below.
Consequence: Stated at a time scale where the regime turns over many times per window, the trend-persistence claim gets enough stretches to be accepted or refused as an entry filter.
Why:
- F1: The test had one coin (BTCUSD) and one window (w1) of only 120 daily bars, so it found 13 in-stretch bars against the plan's minimum of 100 and 1 up-cross stretch against the minimum of 3; the 106 out-of-stretch bars just met their own minimum of 100.
- F2: The only up-stretch is not a new cross: it was already under way at the window's first bar and covers bars 0 to 12 (raw spread positive in 10.8% of bars, max 50.3); the next 107 bars all have the 50-day SMA below the 200-day SMA.
- F3: After the stretch the spread moved further away from a new up-cross, not toward one: its raw mean was -85.4 in the window's middle third (min -92.0) and still -66.4 in the last third (max -56.9). BTC fell 21.1% over the window, so the window held one down-regime, and the 50/200-day regime lasts longer than the window itself.
- F5: The forecast's spread follows the regime exactly: it is 0 on 75% or more of bars (median 0, mean 0.36, max 6.47), and it is positive on exactly the raw-positive bars (0 mismatches). The book made only 3 trades, so the config reaches its situation as designed, and the shortfall comes from too little data.
