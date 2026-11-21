---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e3_weekly-momentum-over-twelve-days
line: 7.g patterns
backtest: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e3_weekly-momentum-over-twelve-days_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: The more a coin's 4h volatility over the last three days exceeds its 4h volatility over the last twenty days, the more the coin rises over the next twelve days, whichever way its last week moved.
Consequence: A trader would lean long into a coin whose volatility is picking up and refuse longs on a coin going quiet, holding for about twelve days.
Why:
- F1: How fast volatility is rising predicts the next twelve days better than the tested forecast does. On the non-overlapping 72-bar grid (1,116 cases), the coin's 12-day return minus its drift grows with the ratio of its 20-bar to its 120-bar 4h volatility, pooled slope +0.070 per unit of ratio (t 4.47). Added next to the forecast in one regression it keeps its weight (t 4.72), and the forecast keeps its own (t 3.70). From the lowest to the highest quintile of the ratio, the drift-adjusted 12-day return goes from -2.57 % (t -2.38) to +4.74 % (t 2.97), against a 0.19 % round trip.
- F2: The rising-volatility effect does not depend on the direction of the last week, though it is uneven across years. In the highest ratio quintile both sides end higher: after a 7-day fall +3.76 % (t 2.81, 124 cases), after a 7-day rise +5.95 % (t 1.87, 99). In the lowest quintile both end lower: -3.12 % (t -2.26) and -2.03 % (t -1.22). The slope is positive on 5 of 6 coins (t 1.7 to 2.7; XMR t 0.20) and in 6 of 8 years (t 4.09 in 2024 and 3.28 in 2025, but -1.78 in 2023).
- F4: Narrow ranges are not followed by larger moves. The mean absolute 12-day move is 13.2 % after the narrowest current-week range quintile and 13.8 % after the widest. By the previous week's range tercile it is 12.3 %, 12.4 % and 11.7 %.
