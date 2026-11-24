---
idea: 031-04_yearly-low-break-reverses
brief: 031_yearly-low-capitulation-or-exhaustion
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 31f1a8c6c7f6
---
Fidelity:
- Situation: a daily close below the lowest close of the prior 365 days -> kept: a regime rule on the close's percent distance from the prior 365-day lowest close (bar excluded), `lt 0`; the book is flat on every other bar.
- Comparison: the further the close is below that old low, the larger the rebound -> kept: inside the regime the forecast is graded by the depth of the close below the old low.
- Outcome: the coin rises over the next 10 days -> kept: long only, each bet held 10 daily bars.
- Verdict transfer: yes: the test longs exactly the closes below the yearly low, sized by their depth, for the stated 10 days.
Forecast: One measure is used, `DistanceFromHighComponent` with `period` 365, `source` "close", `exclude_current` 1, `extreme` "low" and `form` "percent". It gives the close's percent distance from the lowest close of the prior 365 days. The regime detector selects `mean_reversion` only when this distance is below 0, meaning the close has broken the yearly low. Every other bar is `unknown`, which is null, so the forecast there is 0. Inside the regime, the same measure is standardised over 365 bars (min_periods 91), negated and clipped at 0. The forecast is therefore positive (long) and grows linearly with the depth of the close below the old low, capped at 20. It is never negative.
Config: 031-04_yearly-low-break-reverses_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: The cases are bets, read once per non-overlapping 10-bar grid cell of each window. A bet is a rise of the forecast of at least 2 points, in the `mean_reversion` regime. For each case, take the coin's 10-bar return from the signal bar's close and subtract the coin's mean 10-bar return over all its windows (holding the coin). The main measure is the mean of this unusual move, with its t computed with same-day cases summed into one.
- Supporting check: Split the cases at their median forecast. The mean unusual move of the deeper-break half minus that of the shallower half must be above 0.
- Confirm: The mean unusual move is above 0 with t ≥ 2, and the deeper-break half's mean unusual move exceeds the shallower half's.
- Reject: The mean unusual move is below 0 with t ≤ -2, meaning breaks of the yearly low are followed by further falls beyond the coin's normal drift.
- Inconclusive: Any t between -2 and 2 is inconclusive, as is a t ≥ 2 when the depth check fails. Fewer than 20 cases, or cases falling on fewer than 15 distinct days, is also inconclusive whatever the t.
