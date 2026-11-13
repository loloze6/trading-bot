---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-05_sma-up-regime-positive-drift
line: 7.a not observable
backtest: 002-05_sma-up-regime-positive-drift_1d
instruments: BTC/USDT, ETH/USDT, BNB/USDT, SOL/USDT, XRP/USDT, ADA/USDT, DOGE/USDT, LTC/USDT, LINK/USDT, AVAX/USDT
bar: 1d
period: 2018–2025
---
Idea: On one coin's daily bars, while the 50-day SMA stays above the 200-day SMA, from an upward cross until the next downward cross, the next day's close-to-close return is higher on average and positive more often than on that coin's days outside such stretches. Observed over many years and many coins, the sample holds several full up-stretches per coin and thousands of in-stretch and out-of-stretch days.
Consequence: A trader would hold a coin long only while its 50-day SMA is above its 200-day SMA, and would stay out after the downward cross.
Why:
- F1: The test ran on a single coin (BTCUSD) and a single window (w1) of 120 daily bars, about 119 days, all in 2022. That window held 0 upward SMA50/SMA200 crosses and 1 downward cross. Only 1 up-stretch appeared, one already under way at the window's first bar, against the plan's minimum of 3.
- F3: The forecast's situation runs from a 50-day/200-day cross to the next opposite cross, which typically lasts months. That is long compared with a 120-bar window. The standardisation alone uses a 200-value lookback, more than the window's 120 bars. So one window can hold at most a fraction of one stretch.
- F4: The window covers a 2022 decline: the coin fell 21.1% over the window, and the raw spread averaged −56.5 with a minimum of −92.0. The up-regime situation was essentially absent from the sampled period, not merely rare in it.
- F5: Next-bar returns vary widely from bar to bar: the standard deviation is 3.32% per day, against a mean of −0.145%. The in-stretch mean was −0.76% and the out-of-stretch mean −0.07%, a gap of −0.69% with Welch t of −0.95. At a 3.3% daily standard deviation, a 0.2%/day in/out gap would need roughly 2,000 bars on each side to reach t = 2. That is far beyond 13 in-stretch bars and beyond any single 120-bar window.
