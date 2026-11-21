---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.e1_dip-depth-in-uptrend-rebounds
line: 7.g patterns
backtest: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.e1_dip-depth-in-uptrend-rebounds_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 30-day return is positive, the rebound above its normal drift over the next 3 days after a 24-hour fall, in multiples of its 30-day average absolute daily return, is larger the higher its hourly volatility over the last 30 days.
Consequence: A trader buying sharp dips inside a rising month should weight them by the coin's recent volatility and expect little from dips in calm stretches.
Why:
- F3: The tested dip-in-uptrend rebound over 3 days also grows with the coin's 30-day volatility. In the calm third of up-trend dips the rebound is +0.49 % (t 1.09, 116 cases). In the middle third it is +2.41 % (t 4.12, 127), and in the volatile third +2.57 % (t 1.75, 92). The slope rises from 23 bps per unit in the calm third to 197 bps (t 3.25) in the middle third.
- F4: The tested rebound does not outlast its 3 days. After up-trend falls beyond 2 times the usual daily move, the excess is +2.68 % at 3 days (t 3.65, 93 cases). It turns to −0.82 % at 6 days (t −0.63, 39) and −3.01 % at 10 days (t −1.56, 26).
