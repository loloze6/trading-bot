---
brief: 016_grind-versus-jump-moves
source-idea: 016-04_down-jump-price-reversal.g1_volatile-regime-daily-move-reversal
line: 7.d not profitable
backtest: 016-04_down-jump-price-reversal.g1_volatile-regime-daily-move-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 24-hour return measured in units of its past 7-day hourly volatility, the more it moves the opposite way over the next 24 hours, with the reversal unfolding across the whole following day, so that the move as it stands at a day's close carries it rather than its hour-to-hour changes.
Consequence: Set the fade once a day from the daily move and hold it for the day, instead of re-sizing it every hour on a signal whose hourly changes carry no reversal.
Why:
- F1: The book loses because of fees, not because the forecast is wrong: before fees it earns +0.00031 a day (t 1.49), but it pays 0.00262 a day in fees on a turnover of 2.42 of the book per day, which leaves a mean daily return of −0.0023 and a Sharpe of −2.30.
- F2: The same forecast, read only every 24 hours and held for 24 hours, earns +0.00223 per day before fees (t 4.80, 17,246 independent cases) on a turnover of only 1.29 a day, so fees would be about 0.0014 (at the book's 0.0011 per unit of turnover); the hourly book throws this gain away because the forecast's autocorrelation is 0.94 one hour ahead but −0.02 to −0.09 one day ahead, and its sign flips on about 10% of hours.
- F5: Gain grows with forecast size only at the daily scale: on the 24-hour grid the top fifth of |forecast| earns +0.0073 against −0.0002 for the bottom fifth, but in the hourly book the top fifth earns −0.0002 a day before fees, so the hourly re-sizing destroys the graded edge.
