---
idea: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b2_large-breakout-six-day-continuation
brief: 019_quiet-range-then-breakout-on-four-hour-bars
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 3d6ac1c822df
---
Fidelity:
- Situation: a 4h close above the highest high of the preceding two days (12 bars), sized in 30-day (180-bar) mean 4h ranges -> kept
- Comparison: only while the coin's 7-day (42-bar) return is positive -> kept
- Outcome: the coin rises over the next six days (36 bars), more for larger breaks -> kept
- Verdict transfer: yes: the forecast is the idea's own break size under its own condition, held for its own horizon.
Forecast: The break size is BreakoutInMeanRangesComponent with period 12 and base_period 180. It is max(0, close − highest high of the prior 12 bars) divided by the mean 4h bar range over the last 180 bars. It is standardised over its past 180 values (min_periods 45). It is 0 when the close is at or below the two-day high. It is positive on a break, and grows linearly with the break's size in average ranges, capped at 20. The detector sends a bar to "trending" only while PriceEvolutionOnPeriodComponent(42) is above 0, that is while the 7-day return is positive. Every other bar is flat. The forecast is never negative (long only).
Config: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b2_large-breakout-six-day-continuation_4h_config.json
Criterion:
- Horizon: 36 bars
- Main measure: The cases are the forecast's long bets, read once per 36-bar grid cell of each window. For each case, take the coin's 36-bar return from the signal bar's close and subtract the coin's normal 36-bar drift (holding the coin, all windows together). The measure is the mean of this unusual move, with the ordinary t of the mean, before costs.
- Supporting check: Split the cases at the median of their forecast. The mean unusual move of cases above the median, minus that of cases below, must be above 0.
- Confirm: The mean unusual move is above 0 with t ≥ 2 over at least 30 independent cases, and the supporting check passes.
- Reject: The mean unusual move is below 0 with t ≤ −2 over at least 30 independent cases.
- Inconclusive: Any t between −2 and 2, or a confirming t whose supporting check fails, neither confirms nor rejects. So does any count below 30 independent cases.
