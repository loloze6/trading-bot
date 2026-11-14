---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-05_sma-up-regime-positive-drift
line: 7.a not observable
backtest: 002-05_sma-up-regime-positive-drift_1d
instruments: BTC/USDT, ETH/USDT
bar: 4h
period: 2021 to 2025
---
Idea: In one coin's 4-hour bars, while the 50-bar SMA stays above the 200-bar SMA (from an upward cross to the next downward cross), the next bar's close-to-close return is higher on average than on bars when the 50-bar SMA is below the 200-bar SMA.
Consequence: A trader can apply the same cross-to-cross holding rule at a time scale where up-stretches come often enough, within one year, to be counted.
Why:
- F2: The SMA50-over-SMA200 situation reached only 1 up-cross stretch in the window, 13 bars long, all in the window's first third (in-stretch share 0.325 there, 0.000 in the second and third thirds), followed by a single downward cross and one 107-bar run below; the raw spread had 1 sign change over 119 days, with a median of -66.2 (min -92.0, max 50.3).
- F3: The cross-to-cross stretch this idea measures runs on the time scale of the 50 and 200-day averages, so it changes sign about once in 120 bars; a single 120-day window inside a 2022 bear phase cannot hold 3 distinct up-stretches or 100 in-stretch bars.
- F5: Next-bar returns vary widely from case to case (std 0.0332 overall, 0.0233 in-stretch, 0.0342 out-of-stretch), so even the plan's minimum of 100/100 bars only resolves a mean difference of about 0.94% per day at t = 2; at the actual 13/107 counts it needs about 1.45%, and the observed difference was -0.69% (t -0.95).
