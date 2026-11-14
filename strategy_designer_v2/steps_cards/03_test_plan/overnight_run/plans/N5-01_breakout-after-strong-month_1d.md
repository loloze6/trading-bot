---
idea: N5-01_breakout-after-strong-month
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: a close at a new 20-day high after a strong prior 20-day rise -> adapted: the new high is a regime rule, and "strong rise" becomes a graded 20-day rise.
- Comparison: new highs from a strong rise vs. from a flat or falling month -> adapted: position size grows with the prior rise, so flat-range highs get small positions.
- Outcome: a further rise over the next one to two weeks -> adapted: the holding period is dropped, and the 10-bar forward return is read from the record.
- Verdict transfer: yes: forward returns after new-high bars, graded by the prior rise, test exactly whether strong-rise highs beat flat-range highs.
Forecast: The forecast is nonzero only on a bar whose close is above each of its prior 20 closes. That condition is a regime rule on BarsSinceHigh (lookback 20, max_bars 20) equal to 20. On such a bar the forecast is the 20-bar price change (PriceEvolution, period 20), standardised against its own past 60 values (target 10, cap 20) and clipped at 0. A new 20-day high always sits above the close 20 bars back, so the forecast is long and grows with the prior rise. It is small after a flat month and large after a strong rally. It is zero on every other bar.
Config: N5-01_breakout-after-strong-month_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: On new-high bars (forecast > 0), regress the 10-bar forward excess return on the forecast. The excess return is the forward close-to-close return minus the coin's mean 10-bar return over all windows pooled. Use the slope's t-stat, with overlapping 10-bar returns counted once (Newey-West, lag 9).
- Supporting check: The mean 10-bar forward excess return of the top third of forecasts minus that of the bottom third.
- Confirm: The slope is positive with t ≥ 2, and the top-minus-bottom-third difference is positive.
- Reject: The slope is negative with t ≤ -2, meaning highs after strong rises are followed by worse 10-bar returns than flat-range highs.
- Inconclusive: Any slope with -2 < t < 2 is inconclusive. So is any result from fewer than 100 new-high events that do not overlap within 10 bars, pooled over coins and windows.
