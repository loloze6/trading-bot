---
idea: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend
brief: 019_quiet-range-then-breakout-on-four-hour-bars
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: ad5059559106
---
Fidelity:
- Situation: a 4h close below the lowest low of the preceding two-day narrow stretch, only while the 30-day return is positive -> adapted: the break (close under the prior 12-bar low) and the positive 180-bar return are the regime; "narrow" is made graded.
- Comparison: the stretch's narrowness against the coin's 30-day average four-hour range -> kept: the 12-bar stretch range (bar t excluded) over the mean high-low range of the last 180 bars.
- Outcome: the coin falls over the next three days, more when the stretch was narrower -> kept: a short held 18 bars, sized larger the narrower the stretch.
- Verdict transfer: yes: the forecast is short only on downward breaks in a rising month, and it grows with the narrowness the idea names, so the 18-bar falls after its bets confirm or reject the idea.
Forecast: The regime is `trending` on a bar where both of these hold: - the close is below the lowest low of the 12 bars before it (DistanceFromHigh, period 12, extreme low, bar t excluded, below 0); - the 180-bar return is above 0. Every other bar is flat. In `trending`, the forecast combines two components with equal weights: - the narrowness reading: the stretch compression 1 − S/B, where S is the 12-bar stretch range and B is the 180-bar mean bar range. It is standardised (window 180, min_periods 45), negated, and capped at +10. It reads about +10 for a stretch of usual width and falls toward 0 or below as the stretch narrows. - a constant at −10. The forecast is the mean of the two: - it is 0 for a stretch of usual or wider width; - it is negative, and larger in size, the narrower the stretch is; - it reaches about −15 at the narrowest. It is never positive.
Config: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend_4h_config.json
Criterion:
- Horizon: 18 bars
- Main measure: Per case, the return from the close of the bet's bar over 18 bars, minus the coin's normal 18-bar drift, signed short. A case is a short bet, read once per cell of the 18-bar grid of each window. The measure is the mean of these unusual moves over all coins and windows, with its t of the mean.
- Supporting check: Split the cases at the median absolute forecast. The mean short-signed unusual move of the larger-forecast cases minus that of the smaller-forecast cases is above 0.
- Confirm: The mean short-signed unusual move is positive with t >= 2, and the supporting check passes.
- Reject: The mean short-signed unusual move is negative with t <= -2.
- Inconclusive: Every result with t between -2 and 2 is inconclusive. A t >= 2 whose supporting check fails is also inconclusive. Fewer than 30 cases over all coins and windows is inconclusive whatever the t.
