---
idea: N8-01_near-high-drift-rising-average
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: after a new 20-day closing high, close near that high and above its 20-day average -> adapted: "after" becomes "while" the new high is recent, and nearness and recency are graded (range position and bars since the high).
- Comparison: rises more than its average, only while the 20-day average has risen over the last few bars -> kept: the rising average is a regime condition (5-bar slope above 0), and the average is the coin's mean return over all windows.
- Outcome: the coin rises over the following days -> kept: measured as the forward return over 5 bars on in-situation bars.
- Verdict transfer: yes: the graded forecast is long only inside the idea's own conditions, so its forward excess return confirms or rejects the idea itself.
Forecast: The regime gate is "trending". It is active only when all three of these hold: - the SMA20 5-bar slope is above 0; - the close is above its SMA20; - a new 20-day closing high has occurred within the last 19 bars (BarsSinceHigh(20, 20) above 0). On every other bar the forecast is zero. Inside the gate the forecast is the equal-weight mean of two standardised components (window 60, min_periods 20): - the 20-bar Donchian range position, clipped at 0; - BarsSinceHigh(20, 20), which is 20 on the day of the new high and falls by 1 each bar after it. The forecast is never negative. It is largest when the high is fresh and the close sits at the top of its 20-day range. It shrinks as the close drifts down from the high or the high ages.
Config: N8-01_near-high-drift-rising-average_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: On bars with forecast > 0, the 5-bar forward close-to-close return minus the holding benchmark. The benchmark is the coin's mean 5-bar return over all 24 windows pooled. Results are pooled across coins, and the t-stat uses non-overlapping returns (every 5th in-situation bar, or the equivalent HAC adjustment).
- Supporting check: Within in-situation bars, the slope of excess 5-bar forward return on forecast size is positive.
- Confirm: The mean excess 5-bar return is above 0 with t ≥ 2.
- Reject: The mean excess 5-bar return is below 0 with t ≤ -2.
- Inconclusive: Any t between -2 and 2 is neither a confirm nor a reject. So are fewer than 30 non-overlapping in-situation cases pooled across coins and windows.
