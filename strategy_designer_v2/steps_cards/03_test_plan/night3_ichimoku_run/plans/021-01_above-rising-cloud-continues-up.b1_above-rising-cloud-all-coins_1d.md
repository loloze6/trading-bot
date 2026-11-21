---
idea: 021-01_above-rising-cloud-continues-up.b1_above-rising-cloud-all-coins
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: a31b77de3651
---
Fidelity:
- Situation: the coin closes above its Ichimoku cloud and the cloud is rising -> kept: a regime rule needs both the close above the cloud top (9/26/52 spans, displaced 26) and a positive 26-day cloud slope.
- Comparison: none -> kept
- Outcome: the return over the next 26 days is positive, and larger the faster the cloud rose over the past 26 days -> kept: a 26-bar hold, with the long size growing with the 26-day cloud slope.
- Verdict transfer: yes: the test measures the same condition, horizon and gradation, so its result carries over to the idea.
Forecast: The regime detector computes two values on each daily bar. The first is the close's percent distance above the cloud top: `IchimokuCloudPositionComponent` with tenkan 9, kijun 26, senkou 52, displacement 26 and edge "top". The second is the cloud's 26-day percent slope: `IchimokuCloudSlopeComponent` with the same spans and lookback 26. A bar is "trending" only when both are above 0, meaning the close is above a rising cloud. Every other bar is "unknown", which is flat. In the trending regime the forecast is the 26-day cloud slope, standardised against its own past 104 values (target 10, cap 20) and clipped at 0. It is therefore long only and grows continuously with how fast the cloud has risen: a slow rise gives a small long, a fast rise gives a large one, up to 20. It is zero whenever the close is not above a rising cloud.
Config: 021-01_above-rising-cloud-continues-up.b1_above-rising-cloud-all-coins_1d_config.json
Criterion:
- Horizon: 26 bars
- Main measure: The cases are the bars where the forecast is positive, read on the non-overlapping 26-bar grid of each window. For each case, take the coin's 26-bar forward return minus the coin's mean 26-bar return over all its windows (holding the coin). The measure is the mean of these excess returns weighted by the forecast, with a t-statistic on the forecast-weighted excess returns.
- Supporting check: Across the cases, the Spearman rank correlation between the forecast (the cloud-slope size) and the 26-bar excess return is above 0.
- Confirm: The idea is confirmed when the forecast-weighted mean excess return is positive with t ≥ 2 over at least 50 independent cases, and the supporting check passes (rank correlation > 0).
- Reject: The idea is rejected when the forecast-weighted mean excess return is negative with t ≤ -2 over at least 50 independent cases.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is t ≥ 2 when the rank correlation is not above 0, and so is any result with fewer than 50 independent grid cases.
