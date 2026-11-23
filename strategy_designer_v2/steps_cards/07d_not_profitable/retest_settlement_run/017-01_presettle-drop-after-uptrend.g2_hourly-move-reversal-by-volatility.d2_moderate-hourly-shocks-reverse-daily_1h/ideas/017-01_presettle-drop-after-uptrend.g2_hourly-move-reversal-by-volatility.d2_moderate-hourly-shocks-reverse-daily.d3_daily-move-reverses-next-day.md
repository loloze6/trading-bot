---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d2_moderate-hourly-shocks-reverse-daily
line: 7.d confirmed, not profitable
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d2_moderate-hourly-shocks-reverse-daily_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 24-hour return relative to its 24-hour volatility, the more its return over the next 24 hours runs the opposite way.
Consequence: A trader would fade the day's move rather than the last hour's, sized by how large that move is against the coin's volatility.
Why:
- F6: The shock's information lies more in its 24-hour size than in one hour. Faded by the sign of the 24-hour return, the drift-removed 24-hour move is +0.425 % (t 5.33, 5,702 cases) in the top third of |24-hour return|, against −0.046 % and −0.033 % in the bottom and middle thirds. The 1-hour shock bands are uneven: +0.428 % (t 4.64) at 1.0 to 1.5 usual moves, −0.004 % at 1.5 to 2.0, and −0.078 % beyond 3.
- F2: The reversal is almost all on the long side. On 24-hour grid cases, the 24-hour return in the fade's direction is +0.303 % after an hourly drop (t 5.60, 8,622 cases) and only +0.048 % after an hourly rise (t 0.88, 8,480 cases). The cost of a trade is 0.19 %, so the long side's move covers it and the short side's does not.
