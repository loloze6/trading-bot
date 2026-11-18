---
idea: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation
brief: 006_range-compression-precedes-expansion
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 4e6cc97f57e5
---
Fidelity:
- Situation: the coin closes above the high of its prior 20 days -> kept: a regime rule fires when the close is above the highest high of bars t-20..t-1.
- Comparison: the wider its prior 20-day range against its 100-day range -> kept: the 20-day over 100-day high-low range ratio, ending at t-1, sizes the position.
- Outcome: price rises further over the next 10 days -> adapted: the 10-day holding is dropped, so the position is held only on breakout bars; the criterion reads the 10-bar forward return.
- Verdict transfer: yes: the criterion measures the 10-bar rise after each breakout directly against the width, so a confirm or reject here is one for the idea.
Forecast: A regime rule sets `trending` on bars where (close − highest high of the prior 20 bars) / that high × 100 is above 0, which is a close above the prior 20-day high. Every other bar is flat. On breakout bars the forecast is long and sized by the prior range width: (max high − min low over bars t-20..t-1) / (the same over bars t-100..t-1), from RangeCompressionRatioComponent with `form` "width" and `exclude_current` 1. That width is standardised over its last 100 values (min_periods 25). The forecast is always positive on breakout bars, near +10 at a usual width, larger after wide active ranges and smaller after tight squeezes. It is zero off breakouts.
Config: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: The sample is breakout bars (regime `trending`), taken without overlap: within each window, the first breakout, then the next breakout at least 10 bars later. For each, compute the coin's 10-bar forward return minus that coin's mean 10-bar return over all windows (holding the coin), before costs. Regress this excess return on the bar's forecast (`post_pipeline_value` of `width`); the measure is the t of the slope.
- Supporting check: The mean excess 10-bar return of the top third of breakout cases by forecast minus that of the bottom third (Welch t) is above 0.
- Confirm: The slope t is 2 or more, and the top-minus-bottom-third difference is positive.
- Reject: The slope t is −2 or less.
- Inconclusive: Any slope t between −2 and 2 is inconclusive. So is a slope t of 2 or more with a top-minus-bottom difference at 0 or below. At least 60 non-overlapping breakout cases across all coins and windows are needed; fewer is inconclusive.
