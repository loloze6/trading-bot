---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e3_weekly-momentum-over-twelve-days
line: 7.g patterns
backtest: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e3_weekly-momentum-over-twelve-days_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: The wider a coin's high-low range over the 7 days before its latest 7 days, relative to its usual range, the more strongly its 7-day volatility-scaled return continues in the same direction over the next twelve days.
Consequence: A trader would trust a weekly momentum signal more when it follows an already wide, active week, and less when it follows a narrow one.
Why:
- F3: The tested momentum carries on after a wide past week, not a narrow one, the reverse of the brief's mechanism. Split by the range of the week before the 7-day move, the slope of the 12-day drift-adjusted return on the 7-day scaled return has t -0.65 in the narrowest tercile, 2.10 in the middle and 5.07 in the widest (276 cases each).
- F4: Narrow ranges are not followed by larger moves. The mean absolute 12-day move is 13.2 % after the narrowest current-week range quintile and 13.8 % after the widest. By the previous week's range tercile it is 12.3 %, 12.4 % and 11.7 %.
- F5: Only the largest forecasts carry the tested idea's capture. In the top quartile of the forecast's size the signed 12-day drift-adjusted return is +3.49 % (t 3.32, 279 cases); the lower three quartiles give -0.77 %, +0.52 % and +1.23 % (all |t| < 1.2). Both extreme forecast quintiles capture: shorts +3.05 % (t 3.65), longs +3.11 % (t 2.47).
