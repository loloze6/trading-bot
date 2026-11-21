---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.e1_dip-depth-in-uptrend-rebounds
line: 7.g patterns
backtest: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.e1_dip-depth-in-uptrend-rebounds_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 30-day return is negative, the larger its 24-hour move in multiples of its 30-day average absolute daily return, the more the coin moves back the opposite way relative to its normal drift over the next 2 days.
Consequence: In a falling month, a sharp one-day move is a reason to trade against it for about 2 days, sized by how many usual daily moves it spans.
Why:
- F1: When a coin's 30-day return is negative, its 24-hour move reverses over the next day on both sides and in grades. Falls of more than 2 times its 30-day average absolute daily move were followed by +0.82 % above drift (t 2.56, 507 cases). Rises of more than 2 times were followed by −0.94 % (t −3.45, 307 cases). The slope is 27 bps per unit of scaled move (t 6.06, 6319 cases) at 1 day and 38 bps per unit (t 4.31, 3140 cases) at 2 days. It fades to 5 bps per unit (t 0.41) at 3 days.
- F2: This down-trend reversal is carried by the coin's most volatile third of bars. There the 1-day slope is 69 bps per unit (t 7.29, 2419 cases), against −3 bps (t −0.61) in its calmest third. It holds in both halves of the windows: w1–12 t 2.22, w13–24 t 5.81. It holds in every coin with the same sign, from t 1.21 (ZEC) to t 4.27 (XRP).
- F5: In an up-trend, large 24-hour rises are not reversed over the next day: +0.00 % in the reversal direction (t 0.02, 959 cases). Large falls are reversed: +0.53 % (t 2.34, 547). Only the down-trend reverses both ways.
