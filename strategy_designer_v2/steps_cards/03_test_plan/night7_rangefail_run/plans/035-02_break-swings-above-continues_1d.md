---
idea: 035-02_break-swings-above-continues
brief: 035_nearness-to-high-drift-any-market
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: f090b5ff5633
---
Fidelity:
- Situation: a daily close above the coin's 20-day high -> kept: a regime holds the book only while the close is above the prior 20-day highest high.
- Comparison: how many daily swings the close stands above that high -> kept: the excess over the high divided by the mean absolute daily return over 20 days.
- Outcome: the price rises over the next 5 days, more the further above -> kept: 5-bar hold, long position graded by that distance.
- Verdict transfer: yes: the test measures the breakout, its size in daily swings, and the 5-day rise exactly as the idea states them.
Forecast: Bars with a close at or below the prior 20-day high are a null regime, so the forecast is 0 there. On a bar whose close is above the highest high of the prior 20 days, the forecast is long. Its size comes from VolScaledBreakAboveHighComponent (period 20, step 1, steps 20), which is the excess of the close over that high, as a fraction of the close, divided by the mean absolute daily return over the last 20 days. That value is standardised over its last 60 values (min_periods 20). The forecast is 0 at the high and grows with the number of daily swings above it, capped at 20. It is never negative.
Config: 035-02_break-swings-above-continues_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The measure uses cases, which are bars on each window's non-overlapping 5-bar grid with forecast > 0. For each case, take the coin's 5-day return from the close, minus the coin's mean 5-day return over all windows. The measure is the mean of this excess return, with a t-statistic that takes the cases of one day together.
- Supporting check: Across the cases, the Spearman correlation between the forecast and the 5-day excess return is above 0.
- Confirm: The idea is confirmed when the mean excess return is above 0 with t ≥ 2 and the Spearman correlation is above 0.
- Reject: The idea is rejected when the mean excess return is below 0 with t ≤ -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. A t ≥ 2 with a correlation at or below 0 is also inconclusive. At least 100 cases, falling on at least 60 distinct days, are needed; with fewer the result is inconclusive.
