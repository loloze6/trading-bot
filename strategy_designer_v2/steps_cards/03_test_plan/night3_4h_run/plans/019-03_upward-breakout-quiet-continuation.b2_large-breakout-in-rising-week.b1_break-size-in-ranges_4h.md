---
idea: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b1_break-size-in-ranges
brief: 019_quiet-range-then-breakout-on-four-hour-bars
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 3d6ac1c822df
---
Fidelity:
- Situation: a 4h close above the highest high of the prior two days, only while the 7-day return is positive -> kept: the break is `BreakoutInMeanRangesComponent` over the prior 12 bars, and a regime rule passes only bars where the 42-bar return is above 0.
- Comparison: break size counted in the coin's 30-day average 4h range; small breaks are no reason to trade -> adapted: the 180-bar mean high-low range is kept, and "no reason to trade" becomes a graded dead zone (`signed_power`).
- Outcome: the coin rises over the next three days, more for bigger breaks -> kept: a long position held 18 bars, sized by break size.
- Verdict transfer: yes: the forecast is the idea's break size in average ranges, long only, inside a rising week, held for its 3-day horizon.
Forecast: A regime rule makes the forecast active only when the 42-bar (7-day) price change is above 0; on every other bar it is 0. - In active bars, the forecast is the close's distance above the highest high of the prior 12 bars, in units of the mean high-low range over the last 180 bars. It is 0 when the close is at or below that high. - This break size is standardised against its own past 180 values (target 10, cap 20). - It then goes through `signed_power` with exponent 3 and pivot 20, the strongest graded dead zone allowed. Small breaks give a position near 0, and the position grows steeply up to the largest breaks. - The forecast is never negative, so the test is long only.
Config: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b1_break-size-in-ranges_4h_config.json
Criterion:
- Horizon: 18 bars
- Main measure: Each case is a bet (a rise of the forecast of at least 2 points), read once per 18-bar grid cell. For each case, take the coin's 18-bar return from the signal's close minus the coin's normal 18-bar drift over all windows. Measure the mean of these excess returns over all cases on all coins, before costs, with the t of the mean.
- Supporting check: Split the cases by the raw break size (`last_history_value`), at 1 or more average ranges against below 1. The mean excess return of the large-break cases minus that of the small-break cases must be above 0.
- Confirm: The mean excess return is above 0 with t ≥ 2, and the supporting check is above 0.
- Reject: The mean excess return is below 0 with t ≤ -2.
- Inconclusive: Any t between -2 and 2, or t ≥ 2 with the supporting check at or below 0. At least 30 independent cases over all coins are required; fewer is inconclusive.
