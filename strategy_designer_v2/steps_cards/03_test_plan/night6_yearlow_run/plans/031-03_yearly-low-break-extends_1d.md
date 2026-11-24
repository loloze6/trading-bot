---
idea: 031-03_yearly-low-break-extends
brief: 031_yearly-low-capitulation-or-exhaustion
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 31f1a8c6c7f6
---
Fidelity:
- Situation: a daily close below the lowest close of the prior 365 days -> kept: a regime rule fires only while the close is under the prior 365-day closing low, with the current bar excluded from that low.
- Comparison: the depth of the close below that old low -> kept: the forecast is graded by the percent distance below the prior 365-day closing low.
- Outcome: the coin keeps falling over the next 10 days, falling further the deeper the break -> kept: the book goes short, sized by depth, and each bet is held 10 daily bars.
- Verdict transfer: yes: the test measures the same break, the same depth and the same 10-day fall the idea names.
Forecast: A regime rule reads DistanceFromHighComponent (period 365, source close, exclude_current 1, extreme low, form percent). This is the close's percent distance from the lowest close of the prior 365 bars. Only on bars where that distance is below 0 (a fresh close under the yearly low) is the regime "trending" active. On all other bars the book is flat. Inside the regime the same distance is standardised over its own past 365 values (min_periods 91), then clipped at max 0. The forecast is therefore negative (short) and grows in size the deeper the close sits under the old low. It is 0 at the low and is never long. Because standardise scales the depth against the coin's usual distance from its low, breaks give forecasts of only a few points. The rebalance minimum is therefore lowered to 0.05, so that small breaks still take positions.
Config: 031-03_yearly-low-break-extends_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: The cases are short bets, read once per 10-bar grid cell. For each case, take the coin's 10-bar return from the signal bar's close, minus the coin's normal 10-bar drift over all windows, on the short side. Take the mean of these values and its t, with cases on the same day taken together.
- Supporting check: Split the cases at the median |forecast|. The deeper half's mean short-side unusual move must be at least the shallower half's.
- Confirm: The mean short-side unusual move is above 0 with t >= 2, and the deeper half's mean is greater than or equal to the shallower half's.
- Reject: The mean short-side unusual move is below 0 with t <= -2, meaning the coin rises more than its drift after breaks.
- Inconclusive: Any t between -2 and 2, or a confirming main measure whose supporting check fails. The test needs at least 30 cases on at least 20 distinct days; with fewer, the result is inconclusive.
