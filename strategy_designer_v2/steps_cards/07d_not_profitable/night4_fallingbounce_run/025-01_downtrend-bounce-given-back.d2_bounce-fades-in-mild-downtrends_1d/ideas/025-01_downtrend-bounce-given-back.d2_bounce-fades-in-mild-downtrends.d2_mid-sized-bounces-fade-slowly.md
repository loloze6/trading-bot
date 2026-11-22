---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-01_downtrend-bounce-given-back.d2_bounce-fades-in-mild-downtrends
line: 7.d not profitable
backtest: 025-01_downtrend-bounce-given-back.d2_bounce-fades-in-mild-downtrends_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is negative, a one-day rise that is moderate relative to its usual daily move (its 20-day standard deviation of daily returns) is followed by a fall over the next 10 days. The larger the rise is within the range of ordinary sharp up days, the larger the fall, while the very largest rises are followed by further gains.
Consequence: A trader would size bounce fades for mid-sized up days over a 10-day hold and leave the most explosive up days alone.
Why:
- F4: The cubic grading puts the largest shorts on the bounces that fade least. The largest quarter of one-day rises (mean +10.7 %) is followed by an unusual move of -0.01 % and a total of -0.63 %, while the second quarter (mean +3.8 %) gives +0.74 % unusual and +0.15 % total.
- F5: The fade grows with the horizon: the unusual move is +0.25 % at 1 day, +0.32 % at 5 days and +0.67 % at 10 days (t 1.49). The total move stays negative at -0.52 % over 10 days, because the drift grows as well.
- F2: On the bounce cases (982 in my reconstruction), the short's unusual 5-day move is only +0.32 % (t 1.07), while the coins' normal 5-day drift is +0.30 % to +0.91 % upward. The total move a short earns is therefore -0.28 % per case, below zero before the 0.19 % cost of a trade.
