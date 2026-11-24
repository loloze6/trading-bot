---
idea: 032-02_calm-fall-below-high-continues
brief: 032_calm-decline-keeps-falling
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 59f1baae24fe
---
Fidelity:
- Situation: a falling, calm market, with the close below its highest close of the past 30 days -> kept: the profile is added by code, and the 30-day percent distance below the closing high is measured as stated
- Comparison: a further distance below the high against a nearer one -> kept: the short position is graded by the depth below the 30-day high
- Outcome: the coin falls more over the next three days the deeper it sits -> kept: the short is held for a 3-bar horizon
- Verdict transfer: yes: the forecast is the idea's depth below the high, shorted in proportion, inside the idea's own profile and over its own horizon.
Forecast: The forecast uses one indicator, DistanceFromHighComponent with period 30, source close and form percent. It measures the close's percent distance below the highest close of the last 30 days, including the current bar. This value is 0 at a new high and negative below it. It is standardised against its own past 60 values (min_periods 20), which keeps its sign. The forecast is therefore 0 at the 30-day high and short otherwise. The short grows linearly as the close sits deeper below the high, at about -10 for the usual depth and capped at -20. It is never positive. Outside the falling calm profile the code's vetoes keep the forecast at 0.
Config: 032-02_calm-fall-below-high-continues_1d_config.json
Profile: falling calm (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 3 bars
- Main measure: Use the non-overlapping 3-bar grid of each window, on bars with a non-zero forecast. Regress the coin's 3-bar forward return, minus its mean 3-bar return over all windows, on the forecast (post_pipeline_value of depth). The measure is the slope and its t, with cases of the same day pooled.
- Supporting check: Over the same grid cases, the mean unusual 3-bar move in the short direction (minus the coin's drift) is above 0.
- Confirm: The slope is positive with t ≥ 2, so a deeper short forecast is followed by lower returns against holding the coin. The supporting check must also pass.
- Reject: The slope is negative with t ≤ -2, meaning deeper distances below the high are followed by higher returns (rebounds).
- Inconclusive: These results are inconclusive: - any slope with |t| < 2; - a slope with t ≥ 2 whose supporting check fails; - fewer than 100 independent grid cases in a position across all coins and windows.
