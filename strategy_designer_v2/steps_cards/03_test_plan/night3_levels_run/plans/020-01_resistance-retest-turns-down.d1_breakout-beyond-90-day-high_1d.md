---
idea: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: e48527ec0eac
---
Fidelity:
- Situation: a daily close above the highest close of the previous 90 days, larger the further above -> kept
- Comparison: the highest close of the previous 90 days, bar t excluded -> kept
- Outcome: the coin rises more over the next 5 days the further the close stands above that high -> kept
- Verdict transfer: yes: the forecast is the idea's own breakout distance, and the test looks at the idea's own 5-day outcome.
Forecast: The forecast uses DistanceFromHighComponent with period 90, source close and exclude_current 1. Its raw value is the percent distance of today's close from the highest close of the 90 prior days. Standardise rescales it against the mean absolute size of its last 90 values (window 90, min_periods 22). A clip at min 0 then removes everything below the prior high. The forecast is 0 whenever the close is at or below the 90-day high. Above the high it is positive and grows in proportion to how far the close stands beyond it, up to the cap of 20. It is never negative, so there is no short against a breakout.
Config: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Use the non-overlapping 5-bar grid of each window and keep the bars with forecast > 0 (the breakout cases). For each case, take the coin's 5-bar return from that close minus the coin's mean 5-bar return over all its windows. Pool all coins and regress this drift-removed return on the forecast (post_pipeline_value). Report the t of the slope.
- Supporting check: Across the same cases, the mean drift-removed 5-bar return must be above 0.
- Confirm: The slope t must be 2 or more, and the supporting check must pass. This requires at least 30 cases.
- Reject: The slope t is -2 or less, with at least 30 cases.
- Inconclusive: The idea is neither confirmed nor rejected in three situations: - the slope t lies between -2 and 2; - the slope t is 2 or more but the mean drift-removed return is 0 or below; - there are fewer than 30 breakout cases on the grid.
