---
idea: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b2_breakout-graded-by-quiet-week
brief: 019_quiet-range-then-breakout-on-four-hour-bars
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 42e48552438e
---
Fidelity:
- Situation: a 4h bar closes above the highest high of the preceding two days (12 bars) -> kept: a regime rule fires when `BreakoutInMeanRangesComponent` (period 12, prior highs, bar t excluded) is above 0.
- Comparison: the 7-day average 4h range is quieter than the 60-day average -> kept: `MeanBarRangeRatioComponent` (60-day mean range / 7-day mean range, 360/42 bars) sizes the position, larger when quieter.
- Outcome: the coin rises over the next three days, more so the quieter the week -> kept: each breakout bet is long and held 18 bars.
- Verdict transfer: yes: the test bets long on exactly the stated breakouts and sizes them by the stated quietness ratio over the stated horizon.
Forecast: On a bar that closes above the highest high of the 12 bars before it, the regime is "trending". Only there, the forecast is the ratio of the 360-bar mean bar range to the 42-bar mean bar range, standardised against its own past 360 values. It sits near +10 when the past week was as quiet as usual relative to two months, and rises towards +20 when the week was quieter. It shrinks towards 0 when the week was busier. It is never negative. On every other bar the regime is flat (0), so each breakout bar is one long bet, held for the horizon.
Config: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b2_breakout-graded-by-quiet-week_4h_config.json
Criterion:
- Horizon: 18 bars
- Main measure: The unusual move of the cases. A case is a breakout bet (the forecast rises by at least 2 points on a trending bar), read once per 18-bar grid cell. Its unusual move is the coin's 18-bar return from the signal bar's close minus the coin's normal 18-bar drift, pooled over all coins and windows. The statistic is the t of its mean.
- Supporting check: Split the cases at the median of their `post_pipeline_value` of `quiet`. Measure the high-half mean unusual move minus the low-half mean unusual move (Welch t).
- Confirm: The main measure's mean unusual move is positive with t ≥ 2, and the supporting check's difference is greater than 0.
- Reject: The main measure's mean unusual move has t ≤ -2, or the supporting check's difference has Welch t ≤ -2.
- Inconclusive: Any other result is inconclusive, including a main t between -2 and 2, or a positive main t with a supporting difference ≤ 0 whose Welch t is above -2. Fewer than 30 cases in total, or fewer than 15 in either half, is also inconclusive.
