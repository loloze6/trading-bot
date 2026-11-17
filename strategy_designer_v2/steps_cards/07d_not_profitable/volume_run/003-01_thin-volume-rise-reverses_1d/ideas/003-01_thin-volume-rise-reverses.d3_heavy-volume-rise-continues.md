---
brief: 003_volume-separates-reversal-from-continuation
source-idea: 003-01_thin-volume-rise-reverses
line: 7.d not profitable
backtest: 003-01_thin-volume-rise-reverses_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin rises sharply over one day on volume well above its own 30-day average daily volume, it keeps rising over the next 5 days. The larger the rise and the heavier its volume against that average, the larger the further rise.
Consequence: A trader would be long after heavy-volume sharp rises, betting with the coins' rise rather than against it.
Why:
- F6: On the non-overlapping 5-day grid, rises above 2 usual daily moves on volume over 1.25 times the 30-day average carry on, with a 5-day excess of +0.032 (t 1.94, 80 cases). Thin rises of 1 to 1.5 usual moves show no giveback: +0.033 (17 cases) at volume 0.5 or less, and +0.021 (45 cases) at 0.5 to 0.75.
- F5: Being short against the coins' rise (coin daily mean +0.00119) costs -0.000042 per bar. Timing adds only +0.000024 and fees take 0.000069 per bar, which leaves a mean daily book return of -0.0000885 and a Sharpe of -0.58.
