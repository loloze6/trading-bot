---
idea: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: d79aab634da6
---
Fidelity:
- Situation: a close above a price where the coin turned down several times in the past 90 days -> adapted: `ResistanceBreakTouchCountComponent` (period 90) finds swing-high closes crossed upward on this bar; "several times" becomes graded by the touch count N.
- Comparison: the more times the level held and the further the close above it, the larger the rise -> kept: the output is N times the close's percent margin above the level.
- Outcome: the price keeps rising over the next 20 days -> kept: each bet is held 20 bars and judged on the 20-bar return against the coin's drift.
- Verdict transfer: yes: the forecast is non-zero only on closes through repeatedly-turned 90-day levels and grows with touches and margin, so its 20-bar results are the idea's own.
Forecast: The forecast is long only and comes from one component, `ResistanceBreakTouchCountComponent`. - Settings: period 90 (the idea's 90 days), side 2 (the usual swing confirmation), band 2 percent (groups the touches of one level), cross_period 1 (the close-through bar itself). - Raw value: the number of swing-high closes within 2 percent of the crossed level, times the percent margin of the close above that level. - When it is non-zero: only on a bar whose close crossed such a level upward. It is zero on every other bar and never negative. - Scale: it is standardised over its last 90 values, so it is about 10 times its usual non-zero size, capped at 20. - Size: it grows with the touch count and with the distance above the level. - Holding: each bet is held for the 20-bar horizon.
Config: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation_1d_config.json
Criterion:
- Horizon: 20 bars
- Main measure: Per case (a long bet, read once per 20-bar grid cell of each window), take the coin's 20-bar return from the signal bar's close. Subtract the coin's normal 20-bar drift, measured on non-overlapping stretches of all its windows. Report the t of the mean of this excess across all coins and windows, before costs.
- Supporting check: Split the cases at their median forecast. The mean excess return of the upper half minus that of the lower half must be above 0.
- Confirm: Both of these hold: - the mean excess return has t >= 2 over at least 30 cases; - the upper-half-minus-lower-half difference is above 0.
- Reject: The mean excess return has t <= -2 over at least 30 cases.
- Inconclusive: Any of these is inconclusive: - t between -2 and 2; - t >= 2 while the upper-minus-lower difference is not above 0; - fewer than 30 cases.
