---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-06_rebound-in-high-volatility
line: 7.g patterns
backtest: N2-06_rebound-in-high-volatility_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin that falls on a day whose high-low range is much wider than its recent average range, and closes near that day's low, tends to close higher the next day, and more so when the day's volume is well above its recent average.
Consequence: A trader would take a rebound long only after drops that were wide-range, closed near the low and came on heavy volume, and would refuse it after narrow-range or mid-range-close drops.
Why:
- F1: Across the six coins, a wide-range down day is followed by a next-day excess return of +0.89%, with t=6.07 over 1616 cases and 62.6% up days; a wide-range down day here means the top fifth of each coin's high-low range relative to its 60-day average. A wide-range up day is followed by −0.34%, with t=−2.04 over 1287 cases and 43.7% up days.
- F2: Where the bar closes within its range sorts what follows a drop. Drop days (z<−1.5) that close in the bottom fifth of their range are followed by +1.22%, with t=4.44 over 454 cases and 66.5% up. Drop days that close in the upper half are followed by −0.93%, with t=−1.23 over 45 cases and 44% up.
- F3: Among bars that close in the bottom tenth of their range, the next day returns +1.27% (t=3.73, n=312, 64.7% up) when the bar's range is in its widest third, and −0.14% (t=−0.53, n=312) when the range is in its narrowest third.
- F4: Drops (z<−1.5) on volume above 1.89 times the 20-day mean are followed by +1.25% (t=2.88, n=271), against +0.10% (t=0.33, n=271) on volume below 1.25 times the mean.
