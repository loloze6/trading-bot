---
idea: N7-01_drift-only-near-high
brief: 002_moving-average-cross-trend-persistence
data-instruments: ADA, AVAX, DOGE, LINK, SOL, TRX, UNI, AAVE, INJ
data-bar: 1d
data-period: folds A, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: a new 20-day closing high, then close near that high and above its 20-day average -> adapted: "after the high" made "while" a recency score (bars since the high, fading over 20 bars); "within a small distance" made graded as the close's position near the top of its 20-day range; "above the 20-day average" kept as a regime condition.
- Comparison: excess rise over the coin's average return, and returns at or below average once below the 20-day average -> kept: active-bar returns judged against holding the coin, and below-average bars are flat.
- Outcome: price rises more than average over the following days -> adapted: the holding period is dropped and the long is held only while the situation lasts.
- Verdict transfer: yes: the forecast is long only while all three conditions hold and grows with nearness to the high and recency, so its excess return tests the idea directly.
Forecast: A regime gate sets the bar to "trending" only while the close is above its 20-day SMA (MovingAverageDistance 20 sma > 0) and a new 20-day closing high happened within the last 20 bars (BarsSinceHigh lookback 20, max_bars 20, > 0). Every other bar is flat. Inside the gate the forecast is the equal-weight mean of two graded long-only parts: - the close's position in its 20-day close range (Donchian 20), standardised over 60 bars and clipped at 0, so it is largest at the high; - the recency of the new high (BarsSinceHigh), standardised over 60 bars: 20 on the day of the high, one less each bar after. The forecast is never negative. It is largest right after a fresh high with the close at the top of its range. It shrinks as the close slips from the high or the high ages, and it is zero once the close is below the 20-day average.
Config: N7-01_drift-only-near-high_1d_oos_sized_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The forward 5-bar return after each active bar, minus the coin's mean 5-bar return over all 24 windows together, weighted by the forecast. Cases are pooled across coins in non-overlapping 5-bar blocks, so overlapping returns count once. The result is the t-statistic of the mean weighted excess return.
- Supporting check: On flat bars where a new high is within 20 bars but the close is below SMA20, the mean forward 5-bar excess return over holding should be at or below 0.
- Confirm: The forecast-weighted mean excess return is positive with t >= 2.
- Reject: The forecast-weighted mean excess return is negative with t <= -2.
- Inconclusive: Any t strictly between -2 and 2 is inconclusive, as is any test with fewer than 100 non-overlapping active 5-bar blocks across all coins and windows.
