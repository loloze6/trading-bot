---
brief: 016_grind-versus-jump-moves
source-idea: 016-04_down-jump-price-reversal.g1_volatile-regime-daily-move-reversal
line: 7.d not profitable
backtest: 016-04_down-jump-price-reversal.g1_volatile-regime-daily-move-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 24-hour return measured in units of its past 7-day hourly volatility, the more it moves the opposite way over the next 24 hours, only while the coin's 7-day volatility stands above its own 30-day usual level, and the further above it stands, the stronger the reversal.
Consequence: Fade sharp one-day moves only when the coin is in an unusually volatile stretch, and stand aside in calm stretches, where the fade only pays fees and fights the drift.
Why:
- F1: The book loses because of fees, not because the forecast is wrong: before fees it earns +0.00031 a day (t 1.49), but it pays 0.00262 a day in fees on a turnover of 2.42 of the book per day, which leaves a mean daily return of −0.0023 and a Sharpe of −2.30.
- F3: The gain sits entirely in the highest third of volatility ratio (7-day volatility over its 30-day average): on the 24-hour grid that third earns +0.0077 per case, against +0.0001 for the middle third and −0.0007 for the lowest; in the hourly book it earns +0.00197 a day before fees, against −0.00083 in the lowest third.
- F5: Gain grows with forecast size only at the daily scale: on the 24-hour grid the top fifth of |forecast| earns +0.0073 against −0.0002 for the bottom fifth, but in the hourly book the top fifth earns −0.0002 a day before fees, so the hourly re-sizing destroys the graded edge.
