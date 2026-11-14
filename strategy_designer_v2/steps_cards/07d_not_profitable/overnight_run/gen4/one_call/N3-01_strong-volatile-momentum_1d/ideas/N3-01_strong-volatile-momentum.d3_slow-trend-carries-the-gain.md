---
brief: 002_moving-average-cross-trend-persistence
source-idea: N3-01_strong-volatile-momentum
line: 7.d not profitable
backtest: N3-01_strong-volatile-momentum_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: Once a coin has stayed up over both 20 and 60 days for several weeks, its rise continues over the next several weeks more than the coin's average. The persistence lives in the slow part of the trend, not in the next few days.
Consequence: A trader would judge and hold the long on a weekly-or-slower view of the trend rather than reacting to day-to-day swings in the forecast, which cut winners short and churn losers.
Why:
- F2: The gain rests on a few long winners. The 10 best trades make up 74% of the summed gross gain, the median trade loses 1.32%, and only 43.8% of trades win.
- F3: Short holds lose and long holds pay. Gross mean per trade is -3.36% for holds of 2 days or less (n=332), -2.95% for 2–5 days (n=223), -1.08% for 5–10 days (n=191), +4.30% for 10–20 days (n=195) and +43.0% beyond 20 days (n=173).
- F4: Trades give back much of their best excursion. Even trades held over 20 days give back 38 points from a mean peak gain of 81%. Trades exited while the forecast was still 15 or more lost 6.46% gross (n=131).
- F8: Gains come early in a position. The book earns 1.31% per day in the first 2 days of a position (t=2.60, n=487) and loses 0.40% per day on days 5–10 (t=-1.26, n=598).
