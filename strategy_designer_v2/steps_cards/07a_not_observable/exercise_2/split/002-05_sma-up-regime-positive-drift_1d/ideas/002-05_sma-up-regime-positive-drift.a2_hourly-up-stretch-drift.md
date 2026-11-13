---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-05_sma-up-regime-positive-drift
line: 7.a not observable
backtest: 002-05_sma-up-regime-positive-drift_1d
instruments: BTC/USDT, ETH/USDT, SOL/USDT, BNB/USDT, XRP/USDT
bar: 1h
period: 2021–2025
---
Idea: On one coin's hourly bars, while the 50-bar SMA stays above the 200-bar SMA, from an upward cross until the next downward cross, the next bar's close-to-close return is higher on average and positive more often than on that coin's bars outside such stretches. This is the same cross-to-cross situation at a time scale where it recurs many times per window and gives thousands of bars on each side.
Consequence: A trader would take hourly long exposure only while the 50-bar SMA is above the 200-bar SMA, and would step aside after the downward cross.
Why:
- F2: The forecast was positive on 13 bars and zero on 107. All 13 positive bars sit in the first 12-to-13-bar block, where the raw spread starts at +50.3 and the forecast averages 3.34 with a maximum of 6.47. From the second block on, the spread averages −14.8, then falls to between −50 and −91. The plan asked for 100 in-stretch bars and got 13.
- F3: The forecast's situation runs from a 50-day/200-day cross to the next opposite cross, which typically lasts months. That is long compared with a 120-bar window. The standardisation alone uses a 200-value lookback, more than the window's 120 bars. So one window can hold at most a fraction of one stretch.
- F5: Next-bar returns vary widely from bar to bar: the standard deviation is 3.32% per day, against a mean of −0.145%. The in-stretch mean was −0.76% and the out-of-stretch mean −0.07%, a gap of −0.69% with Welch t of −0.95. At a 3.3% daily standard deviation, a 0.2%/day in/out gap would need roughly 2,000 bars on each side to reach t = 2. That is far beyond 13 in-stretch bars and beyond any single 120-bar window.
