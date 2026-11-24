---
idea: 031-01_extreme-rise-partly-reverses
brief: 031_medium-term-overreaction-reversal
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 31f1a8c6c7f6
---
Fidelity:
- Situation: a coin's 90-day return stands above its own usual 90-day move, scaled by its past volatility -> adapted: a regime holds only while the 90-day return is at least one usual 90-day move (daily volatility over 365 days x sqrt(90)); inside it the position is graded by how far above it stands.
- Comparison: its own usual 90-day move, from its own past volatility -> kept
- Outcome: price falls back over the next 30 days, more the further above -> kept
- Verdict transfer: yes: the test measures the 30-day fall after vol-scaled 90-day rises above one usual move, graded by their size, against the coin's normal drift.
Forecast: The forecast uses one quantity, the 90-day return divided by the usual 90-day move. The usual move is the standard deviation of the last 365 daily returns times sqrt(90). On bars where that ratio is below 1, the regime is flat and the forecast is 0. On bars where it is 1 or more, the forecast is short. Its size is the ratio standardised against its own last 365 values (about -10 at a typical size, capped at -20), so the short grows the further the rise stands above the usual move. The forecast is never positive.
Config: 031-01_extreme-rise-partly-reverses_1d_config.json
Criterion:
- Horizon: 30 bars
- Main measure: The cases are the bars in the mean_reversion regime that carry a bet, one per cell of a non-overlapping 30-bar grid in each window. For each case, take the coin's 30-bar return from that close, minus the coin's normal 30-bar drift (its mean over all windows), in the short direction. The measure is the mean of this unusual move and its t, with cases on the same day taken together.
- Supporting check: none
- Confirm: The mean unusual move in the short direction is above 0 with t >= 2.0, over at least 30 cases on at least 20 distinct days.
- Reject: The mean unusual move in the short direction is below 0 with t <= -2.0 (the coins keep rising), over at least 30 cases on at least 20 distinct days.
- Inconclusive: Any t between -2.0 and 2.0 is inconclusive. So is any result with fewer than 30 cases or fewer than 20 distinct days.
