---
idea: 003-07_quiet-hours-moves-revert
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: sharp move while volume is low -> adapted: a day whose volume is below its 20-day mean, sized by that day's move; quiet hours cannot be seen on 1d bars, weekends can.
- Comparison: none -> kept
- Outcome: the move is partly given back next -> adapted: "once volume returns" becomes the next bar's return against the move.
- Verdict transfer: yes: low-volume days include the weekends, and a reversal on the next bar is the idea's claim.
Forecast: The forecast is active only on a bar whose volume is below its 20-bar mean, as set by a regime veto. On those bars it is minus the standardised 1-bar percent move: short after an up day, long after a down day. The move is standardised over the past 60 bars, then given a graded dead zone (exponent 2, pivot 10), so small moves give almost no position and sharp moves give a large one. On bars with average or higher volume the forecast is 0.
Config: 003-07_quiet-hours-moves-revert_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: Regress the next bar's close-to-close return on the forecast over all active (low-volume) bars, pooled across the 6 windows, with an intercept so the coin's own drift is not credited. The measure is the t-stat of the slope, before costs.
- Supporting check: On active bars in the top fifth of |forecast|, the mean of sign(forecast) × next-bar return should be positive.
- Confirm: Slope t >= 2.
- Reject: Slope t <= -2, meaning low-volume sharp moves continue rather than revert.
- Inconclusive: Any slope t between -2 and 2. Also inconclusive if there are fewer than 100 active bars, or fewer than 20 bars in the top fifth.
