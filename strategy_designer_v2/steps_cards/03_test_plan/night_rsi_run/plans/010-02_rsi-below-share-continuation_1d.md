---
idea: 010-02_rsi-below-share-continuation
brief: 010_rsi-midline-regime-direction
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 70a362722b07
---
Fidelity:
- Situation: the share of the past 30 days the coin's 14-day RSI spent below 50 -> kept
- Comparison: a larger share against a smaller share (the more time below, the lower the return) -> kept
- Outcome: lower return over the next 14 days -> kept
- Verdict transfer: yes: the forecast is the share itself, signed and graded, and it is judged on the 14-day return the idea names.
Forecast: The forecast uses one indicator, `RsiAboveMidlineShareComponent` with RSI period 14, a 30-bar window, rsi_window 100 and side "below". Its raw value is the share of the last 30 daily bars with RSI below 50, minus 0.5, so it runs from -0.5 to +0.5. It is standardised over its past 130 values, with 32 needed before it starts, and then negated. The forecast is short and grows as RSI has spent more than half of the 30 days below 50. It is long and grows as RSI has spent less than half of them below 50. It is 0 at exactly half. Its size follows the share step by step, with no threshold, and the run is ungated.
Config: 010-02_rsi-below-share-continuation_1d_config.json
Criterion:
- Horizon: 14 bars
- Main measure: Use the non-overlapping 14-bar grid of each window, all coins together. At each grid bar t, take forecast[t]/10 × (the coin's 14-bar return from t, minus that coin's mean 14-bar return over all windows). The measure is the mean of this product and its t-statistic, before costs.
- Supporting check: The Spearman correlation between the raw share below (`last_history_value`) and the coin's excess 14-bar return, on the same grid, is negative in at least 2 of the 3 coins.
- Confirm: Confirm only when the mean signed excess return is above 0 with t ≥ 2.0, and the supporting check passes.
- Reject: Reject when the mean signed excess return is below 0 with t ≤ -2.0. This means returns run with the RSI side rather than against it.
- Inconclusive: Any t between -2.0 and 2.0 is inconclusive, as is t ≥ 2.0 with the supporting check failing. A result needs at least 300 independent grid cases in total; there are about 24 × 8 × 3 ≈ 570 available.
