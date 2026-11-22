---
idea: 023-01_flat-range-top-reverts-down
brief: 023_range-reversion-when-no-trend
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: be08f97ea86e
---
Fidelity:
- Situation: the 30-day net move is small relative to the 30-day high-low range -> kept: a regime rule puts a bar in mean_reversion when NetMoveToRangeRatio (30, high_low) is 0.33 or less.
- Comparison: the close against the middle of the 30-day high-low range -> kept: IchimokuCloudPosition with all three periods at 30 and displacement 0 gives (close − (max high + min low)/2) / close x 100.
- Outcome: the further above the middle, the more it falls over the next 5 days -> kept: the forecast is short in proportion to the distance above the middle, and each bet is held 5 bars.
- Verdict transfer: yes: the test measures the idea's own range, middle, flatness condition and 5-day horizon, so its result carries over to the idea.
Forecast: Each bar is checked first. If the 30-bar net close move is at most 0.33 of the 30-bar high-low range, the bar is in the mean_reversion regime; on every other bar the forecast is 0 (flat). On mean_reversion bars, the indicator is the distance of the close from the midpoint of the 30-bar high-low range, in percent of the close. It is standardised against its past 60 values (target 10, cap 20) and then negated. The forecast is therefore short when the close is above the middle and long when it is below. Its size grows linearly with the distance from the middle and is near 0 at the middle.
Config: 023-01_flat-range-top-reverts-down_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Use the non-overlapping 5-bar grid of each window and keep the bars where the forecast is not 0. For each such bar, take (forecast / 10) x (the coin's 5-bar forward return minus its mean 5-bar return over all windows). Report the mean of these values and its t, with the number of cases.
- Supporting check: none
- Confirm: The mean is above 0 with t of 2 or more, on at least 30 cases.
- Reject: The mean is below 0 with t of −2 or less, on at least 30 cases.
- Inconclusive: Any t between −2 and 2 is inconclusive. Fewer than 30 non-zero-forecast grid cases across all coins and windows is also inconclusive.
