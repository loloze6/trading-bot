---
idea: 013-06_breakout-volume-drives-continuation
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: a coin closes above its prior 52-week high -> kept: BarsSinceHigh(lookback 364, max_bars 1) equals 1 only on a close above the prior 364 closes, and a regime rule picks those bars.
- Comparison: breakout-day volume relative to its own 90-day average -> adapted: VolumeRatio(90) on the breakout bar is graded instead of a high/low split; its average includes that bar.
- Outcome: the higher that volume, the larger the return over the next 30 days -> adapted: the 30-day holding period is dropped; the 30-bar forward return is read from the recorded closes.
- Verdict transfer: yes: the same breakout, the same volume ratio and the same 30-day return are measured, so a high-minus-low volume difference confirms or rejects the idea directly.
Forecast: Only on a bar whose close is above every one of its prior 364 closes (a new 52-week closing high), the forecast is that bar's volume divided by its 90-bar average volume, standardised against its own past 90 values (an ordinary-volume day gives about +10, twice the usual ratio up to the +20 cap). It is long-only and grows with relative volume. It is 0 on every other bar (regime null).
Config: 013-06_breakout-volume-drives-continuation_1d_config.json
Criterion:
- Horizon: 30 bars
- Main measure: The cases are breakout bars (regime trending, forecast > 0) with close[t+30] inside the same window. In each coin-window, a bar is kept only if it is at least 30 bars after the previous kept bar. Each case's outcome is close[t+30]/close[t]-1 minus the coin's mean 30-bar return over all windows (non-overlapping grid). The measure is Welch's t of the mean outcome of the cases above the median forecast minus the cases at or below it.
- Supporting check: none
- Confirm: The high-volume group minus the low-volume group is positive, with Welch t >= 2.
- Reject: The high-volume group minus the low-volume group is negative, with Welch t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. Fewer than 40 kept cases in total, or fewer than 15 in either group, is also inconclusive.
