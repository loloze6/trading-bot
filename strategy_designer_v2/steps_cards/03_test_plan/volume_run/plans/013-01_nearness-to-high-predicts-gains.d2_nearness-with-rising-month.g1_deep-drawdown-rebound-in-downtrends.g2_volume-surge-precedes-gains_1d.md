---
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g2_volume-surge-precedes-gains
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: the coin's volume over the past day relative to its 20-day average -> kept: VolumeRatioComponent(20), whose average includes today's bar.
- Comparison: higher volume ratio against lower, down to unusually thin volume -> adapted: the comparison is graded, so the position grows with the ratio and is small when volume is thin.
- Outcome: higher return over the next 7 days, long side -> kept: horizon of 7 bars on 1d bars.
- Verdict transfer: yes: the forecast grows only with the volume ratio, and the measure asks whether the 7-day return grows with it.
Forecast: The forecast is today's volume divided by its 20-day mean volume (VolumeRatioComponent, period 20), standardised against its own last 60 values (min_periods 20). It is about +10 at average volume, near +3 when volume is thin and up to +20 on volume bursts. It is never negative and never short: the long position grows with relative volume and shrinks toward nothing when volume is thin.
Config: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g2_volume-surge-precedes-gains_1d_config.json
Criterion:
- Horizon: 7 bars
- Main measure: On a non-overlapping 7-bar grid in each window, take each coin's 7-bar forward return minus that coin's mean 7-bar return over all windows. Pool all coins and regress this excess return on the bar's forecast. The measure is the slope's t-statistic (the excess return is judged against holding the coin).
- Supporting check: Across the 6 coins, the per-coin slope of excess 7-bar return on forecast is positive in at least 4.
- Confirm: The pooled slope has t ≥ 2 and the supporting check passes.
- Reject: The pooled slope has t ≤ -2, meaning higher relative volume is followed by lower 7-day excess return.
- Inconclusive: The idea is neither confirmed nor rejected if -2 < t < 2, or if t ≥ 2 while the supporting check fails. The test needs at least 300 non-overlapping 7-bar cases pooled across coins.
