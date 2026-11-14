---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-05_sma-up-regime-positive-drift
line: 7.a not observable
backtest: 002-05_sma-up-regime-positive-drift_1d
instruments: BTC/USDT, ETH/USDT
bar: 1h
period: 2021-2025
---
Idea: On a coin's hourly bars, the hours on which its 50-hour simple average is above its 200-hour simple average are followed by a higher mean next-hour close-to-close return than the hours on which it is below. At this scale, cross-to-cross stretches recur many times within a few months.
Consequence: A trader would take hourly longs only while the short hourly average sits above the long one.
Why:
- F2: The data is one coin (BTCUSD) and one window (w1) of 120 daily bars covering 119 days. That is shorter than the 200-day slow average itself, so a full cross-to-cross stretch of a 50/200 daily pair can hardly fit inside it.
- F4: After the down-cross the raw spread never came back. Every 12-bar block from the third onward averaged between -50.2 and -90.8 (low of -92.0, last value -56.9), so the window is one regime and gave no chance of a second up-cross.
- F5: The outcome varies far more than the effect being measured. The next-bar return SD was 0.0233 in-stretch and 0.0342 out-of-stretch, against a mean difference of -0.0069 (Welch t -0.95). At a daily SD near 0.03, a true drift of 0.2% per day needs roughly 1,800 bars per side to reach t=2, which means many years of daily bars or many coins.
