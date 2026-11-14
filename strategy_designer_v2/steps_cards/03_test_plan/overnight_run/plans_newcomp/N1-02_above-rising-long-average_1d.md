---
idea: N1-02_above-rising-long-average
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: close above its 200-day SMA, and that SMA has risen over the last 20 bars -> adapted: "SMA risen over 20 bars" is kept exactly as a regime rule (20-bar slope of SMA200 > 0); "close above SMA200" is made graded as the percent distance above the SMA, clipped at 0.
- Comparison: rising-SMA cases against falling-SMA cases, where trades are refused -> kept: the regime is flat whenever the SMA's 20-bar slope is not positive.
- Outcome: price keeps rising over the next weeks -> kept: the forward return over 20 bars after long bars, against holding the coin.
- Verdict transfer: yes: the test longs exactly the idea's situation, scaled by how far the close sits above the SMA, and judges the following rise against holding.
Forecast: The forecast is flat unless the 200-bar SMA is higher than it was 20 bars ago. That condition is a regime rule on MovingAverageSlopeComponent (sma, period 200, lookback 20) with slope > 0. Inside that regime, the forecast is MovingAverageDistanceComponent (sma, period 200), the percent distance of the close above its 200-day SMA. It is standardised over its past 200 values (min_periods 50) and clipped at 0. So it is positive and grows with the distance while the close is above a rising SMA. It is 0 when the close is at or below the SMA, and 0 whenever the SMA is not rising. It never goes short.
Config: N1-02_above-rising-long-average_1d_config.json
Criterion:
- Horizon: 20 bars
- Main measure: The mean 20-bar forward log return of the coin on bars where the forecast is above 0, minus the coin's mean 20-bar return over all bars of all windows pooled (holding). The t-statistic counts overlapping returns once: use non-overlapping 20-bar blocks, or a HAC estimate with 19 lags. Pool across coins, before costs.
- Supporting check: Among active bars, the slope of the 20-bar forward return regressed on the forecast's size is positive, so gains grow with the position.
- Confirm: The excess mean forward return over holding is positive with t ≥ 2.
- Reject: The excess mean forward return over holding is negative with t ≤ -2: price after a rising-SMA, above-SMA state underperforms holding or reverses.
- Inconclusive: Any t between -2 and 2, including estimates near zero. The test also needs at least 30 non-overlapping 20-bar active cases pooled across coins and windows; with fewer it is inconclusive.
