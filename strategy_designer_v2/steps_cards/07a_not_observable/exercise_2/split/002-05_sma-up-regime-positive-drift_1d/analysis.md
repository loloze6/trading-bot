---
line: 7.a not observable
backtest: 002-05_sma-up-regime-positive-drift_1d
idea tested: 002-05_sma-up-regime-positive-drift
step 5: not observable
step 6: none
mode: analyst then deducer
explorations: 1
cost: 0.2127 USD
---
## Findings
- **F1:** The test ran on a single coin (BTCUSD) and a single window (w1) of 120 daily bars, about 119 days, all in 2022. That window held 0 upward SMA50/SMA200 crosses and 1 downward cross. Only 1 up-stretch appeared, one already under way at the window's first bar, against the plan's minimum of 3.
- **F2:** The forecast was positive on 13 bars and zero on 107. All 13 positive bars sit in the first 12-to-13-bar block, where the raw spread starts at +50.3 and the forecast averages 3.34 with a maximum of 6.47. From the second block on, the spread averages −14.8, then falls to between −50 and −91. The plan asked for 100 in-stretch bars and got 13.
- **F3:** The forecast's situation runs from a 50-day/200-day cross to the next opposite cross, which typically lasts months. That is long compared with a 120-bar window. The standardisation alone uses a 200-value lookback, more than the window's 120 bars. So one window can hold at most a fraction of one stretch.
- **F4:** The window covers a 2022 decline: the coin fell 21.1% over the window, and the raw spread averaged −56.5 with a minimum of −92.0. The up-regime situation was essentially absent from the sampled period, not merely rare in it.
- **F5:** Next-bar returns vary widely from bar to bar: the standard deviation is 3.32% per day, against a mean of −0.145%. The in-stretch mean was −0.76% and the out-of-stretch mean −0.07%, a gap of −0.69% with Welch t of −0.95. At a 3.3% daily standard deviation, a 0.2%/day in/out gap would need roughly 2,000 bars on each side to reach t = 2. That is far beyond 13 in-stretch bars and beyond any single 120-bar window.

## Ideas
- `002-05_sma-up-regime-positive-drift.a1_daily-up-stretch-drift-multi-year` (from F1, F3, F4, F5): On one coin's daily bars, while the 50-day SMA stays above the 200-day SMA, from an upward cross until the next downward cross, the next day's close-to-close return is higher on average and positive more often than on that coin's days outside such stretches. Observed over many years and many coins, the sample holds several full up-stretches per coin and thousands of in-stretch and out-of-stretch days.
- `002-05_sma-up-regime-positive-drift.a2_hourly-up-stretch-drift` (from F2, F3, F5): On one coin's hourly bars, while the 50-bar SMA stays above the 200-bar SMA, from an upward cross until the next downward cross, the next bar's close-to-close return is higher on average and positive more often than on that coin's bars outside such stretches. This is the same cross-to-cross situation at a time scale where it recurs many times per window and gives thousands of bars on each side.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
