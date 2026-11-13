---
brief: 002_moving-average-cross-trend-persistence
source-idea: N1-01_trend-with-rising-month
line: 7.g patterns
backtest: N1-01_trend-with-rising-month_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's daily return on the bar stamped Saturday 00:00 UTC (and to a lesser degree the one stamped Friday) is higher than its average daily return. This holds across coins and years, whatever the trend state.
Consequence: A trader adding long exposure would do it before the Friday/Saturday-stamped bars rather than ahead of the Tuesday/Thursday-stamped ones.
Why:
- F1: The daily close-to-close return ending on the bar stamped Saturday (all bars are stamped 00:00 UTC) averages +0.44% against about +0.07% for the other days pooled (n=2415, t=5.39); it is positive for every coin (t 1.40 to 2.92), and in 6 of 8 years (t 2.80 to 3.36 in 2019, 2020, 2024 and 2025).
- F2: The return on the bar stamped Friday is also positive, +0.32% (n=2411, t=3.43), so Friday and Saturday are positive for all six coins together (t 1.87 to 3.76), while Tuesday (-0.10%, t=-1.09) and Thursday (-0.18%, t=-1.67) lean negative.
- F3: The Friday/Saturday tilt is larger when the book is long than when it is flat. The Saturday bar returns +0.95% against +0.21% flat, and Thursday returns -0.39% against -0.09% flat, so the book's daily P&L depends partly on weekday rather than on trend.
