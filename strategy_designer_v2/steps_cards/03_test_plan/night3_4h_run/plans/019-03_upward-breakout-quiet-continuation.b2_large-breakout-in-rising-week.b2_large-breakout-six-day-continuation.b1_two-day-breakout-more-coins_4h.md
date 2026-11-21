---
idea: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b2_large-breakout-six-day-continuation.b1_two-day-breakout-more-coins
brief: 019_quiet-range-then-breakout-on-four-hour-bars
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 3d6ac1c822df
---
Fidelity:
- Situation: a 4h close above the highest high of the preceding two days, only while the 7-day return is positive -> kept: BreakoutInMeanRangesComponent(period 12) is positive only on such a close, and a regime rule on PriceEvolution(42) > 0 gates it.
- Comparison: the break's distance measured in the coin's 30-day average 4h range -> kept: the component divides the break by the mean bar range over 180 bars.
- Outcome: the coin rises over the next six days, more after larger breaks -> kept: each long bet is held 36 bars and judged against the coin's normal drift.
- Verdict transfer: yes: the config builds exactly the stated break, gate, scaling and horizon, so its result is the idea's result.
Forecast: On every 4h bar, a regime rule checks the coin's 42-bar (7-day) percent return. When it is above 0, the bar is `trending`. On every other bar the regime is `unknown`, which is null, so the forecast is 0. In `trending`, the forecast is BreakoutInMeanRangesComponent with period 12 and base_period 180. Its raw value is max(0, close − highest high of the prior 12 bars) divided by the mean high−low range of the last 180 bars. That value is standardised over its last 180 values (min_periods 45). The forecast is therefore 0 when there is no break, and positive and growing with the break's size up to the cap of 20. It is never negative: long or flat only.
Config: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b2_large-breakout-six-day-continuation.b1_two-day-breakout-more-coins_4h_config.json
Criterion:
- Horizon: 36 bars
- Main measure: The cases are the bets: rises of the forecast of at least 2 points, read once per 36-bar grid cell of each window. For each case, take the coin's 36-bar return from the signal bar's close and subtract the coin's normal 36-bar drift over all its windows. Measure the mean of this unusual move over all coins and its ordinary t.
- Supporting check: Split the cases at their median forecast. The mean unusual move of the larger-forecast half minus that of the smaller-forecast half must be above 0.
- Confirm: The mean unusual move is above 0 with t ≥ 2, and the supporting check is above 0.
- Reject: The mean unusual move is below 0 with t ≤ -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. A t ≥ 2 with the supporting check at or below 0 is also inconclusive. Fewer than 30 independent cases in total is inconclusive whatever the t.
