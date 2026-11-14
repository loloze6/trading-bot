---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-05_sma-up-regime-positive-drift
line: 7.a not observable
backtest: 002-05_sma-up-regime-positive-drift_1d
instruments: BTC/USDT, ETH/USDT, and other large spot coins with long daily histories
bar: 1d
period: 2017 to 2025
---
Idea: In one coin's daily bars, while the 50-day SMA stays above the 200-day SMA (from an upward cross to the next downward cross), the next day's close-to-close return is higher on average than on days when the 50-day SMA is below the 200-day SMA.
Consequence: A trader holding the coin only while the 50-day average is above the 200-day average would catch better-than-average days and sit out the weaker ones.
Why:
- F1: The backtest holds one coin (BTCUSD), one window (w1) of 120 daily bars, all in 2022, so only 13 in-stretch bars (forecast > 0) and 107 out-of-stretch bars could occur, against the plan's minimum of 100 in-stretch bars and 3 up-cross stretches.
- F2: The SMA50-over-SMA200 situation reached only 1 up-cross stretch in the window, 13 bars long, all in the window's first third (in-stretch share 0.325 there, 0.000 in the second and third thirds), followed by a single downward cross and one 107-bar run below; the raw spread had 1 sign change over 119 days, with a median of -66.2 (min -92.0, max 50.3).
- F3: The cross-to-cross stretch this idea measures runs on the time scale of the 50 and 200-day averages, so it changes sign about once in 120 bars; a single 120-day window inside a 2022 bear phase cannot hold 3 distinct up-stretches or 100 in-stretch bars.
- F5: Next-bar returns vary widely from case to case (std 0.0332 overall, 0.0233 in-stretch, 0.0342 out-of-stretch), so even the plan's minimum of 100/100 bars only resolves a mean difference of about 0.94% per day at t = 2; at the actual 13/107 counts it needs about 1.45%, and the observed difference was -0.69% (t -0.95).
