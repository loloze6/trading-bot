---
idea: N4-01_breakout-drift-lasts
brief: 002_moving-average-cross-trend-persistence
data-instruments: NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: fold D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: a close at the highest of the prior 20 days, on an up day -> adapted: "after the new high" becomes "while within 10 bars of a 20-bar closing high" (BarsSinceHigh regime); the size is graded by where the close sits in its 20-bar range; the up day is implied by the new high.
- Comparison: none stated; judged against the coin's own average move -> kept
- Outcome: price keeps rising over the next ten or more days, even after closes below the high -> adapted: the 10-day hold is dropped and the position is long while the regime holds.
- Verdict transfer: yes: the forecast is long exactly in the 10 bars after each new 20-bar closing high, so its excess return tests the idea's claim directly.
Forecast: The regime is `trending` while the last close above every one of its prior 20 closes is at most 9 bars old (BarsSinceHigh, lookback 20, max_bars 20, value >= 11). That window is the high day plus the next 9 bars. On all other bars the forecast is flat. Inside the regime the forecast is the 20-bar Donchian range position, standardised over its past 60 values and clipped at 0. It is largest on the new-high day. It shrinks smoothly as the close falls back below the high but stays positive while the close is in the upper half of the range. It is never short.
Config: N4-01_breakout-drift-lasts_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: On each window's non-overlapping 10-bar grid, take the bars with forecast > 0. Measure their 10-bar forward return minus the coin's mean 10-bar return over all windows, pooled over the four coins, with the t of the mean.
- Supporting check: Take the grid bars in the regime where the close is below its 20-bar high (bars since the high >= 1). Their mean 10-bar excess return must be above 0.
- Confirm: The mean excess is above 0 with t >= 2, and the supporting check passes.
- Reject: The mean excess is below 0 with t <= -2.
- Inconclusive: Any t strictly between -2 and 2 is inconclusive. A t >= 2 with a failed supporting check is also inconclusive. Fewer than 20 pooled independent cases is inconclusive.
