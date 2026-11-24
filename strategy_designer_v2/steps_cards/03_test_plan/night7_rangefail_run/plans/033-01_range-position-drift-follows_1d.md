---
idea: 033-01_range-position-drift-follows
brief: 033_range-position-predicts-drift
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 59f1baae24fe
---
Fidelity:
- Situation: the daily close's place within its own 20-day high-to-low range -> kept: the close's position between the highest and lowest of the last 20 closes, graded from bottom to top.
- Comparison: higher in the range against lower in the range, graded through the whole range -> kept: the forecast's size and sign grow with the position from bottom to top.
- Outcome: the coin rises over the next 5 days after high closes and falls after low closes -> kept: 5-day forward return beyond the coin's usual drift, long high in the range and short low in it.
- Verdict transfer: yes: the forecast is the idea's graded range position, and the measure is the idea's 5-day graded drift.
Forecast: Uses DonchianBreakoutComponent with period 20, on closes. Its raw value is (2 x pos - 1) x 20, where pos is where the close sits between the lowest and the highest of the last 20 closes, bar t included. It is standardised over its past 60 values with min_periods 20. The forecast is positive when the close is in the upper half of the range and negative in the lower half. It is 0 at the middle. It grows smoothly and is largest in size at the top (long) or at the bottom (short). No regime is used: the idea holds on every bar.
Config: 033-01_range-position-drift-follows_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The slope of the 5-bar forward return on the forecast (post_pipeline_value). The return is close[t+5]/close[t] - 1 minus the coin's mean 5-bar return over all windows. It is read on the non-overlapping 5-bar grid of each window, all coins pooled, with the t of the slope.
- Supporting check: The mean drift-removed 5-bar return of grid cases with forecast in the top fifth, minus that of the bottom fifth, must be above 0.
- Confirm: The slope is positive with t >= 2, and the supporting check passes.
- Reject: The slope is negative with t <= -2. Closes high in the range are then followed by below-drift returns, and closes low in the range by above-drift returns.
- Inconclusive: Any slope with t between -2 and 2, or a confirming slope whose supporting check fails. At least 500 grid cases across the coins are needed, otherwise the result is inconclusive.
