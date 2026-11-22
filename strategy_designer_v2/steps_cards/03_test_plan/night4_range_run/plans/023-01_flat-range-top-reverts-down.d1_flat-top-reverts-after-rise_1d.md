---
idea: 023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise
brief: 023_range-reversion-when-no-trend
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: be08f97ea86e
---
Fidelity:
- Situation: a close above the middle of a flat 30-day range, while the 90-day return is positive -> kept: graded 30-bar range position times flatness, active only while the 90-bar return is at or above 0; the range is read from closing highs and lows.
- Comparison: the 30-day net move small against the 30-day high-low range -> adapted: the threshold "small" made graded by the flatness factor, 1 minus net move over range.
- Outcome: the price falls over the next 5 days, more the further above the middle -> kept: short position growing with the distance above the middle, held 5 bars.
- Verdict transfer: yes: the forecast is the idea's graded situation inside its own 90-day-rise condition, judged on the 5-day move.
Forecast: A regime rule on the 90-bar percent return selects `mean_reversion` when that return is 0 or more; every other bar is `unknown`, which is flat. In `mean_reversion`, the forecast uses FlatnessWeightedRangePositionComponent(30). It is the close's position in its 30-bar closing range, from -1 at the bottom to +1 at the top, times 1 minus |30-bar net move| over that range. It is standardised over 60/20 and then negated. It is clipped at max 0, so it is short only. It is 0 at or below the middle and grows more negative the higher the close sits above the middle and the flatter the month.
Config: 023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The cases are bars on the non-overlapping 5-bar grid of each window where the forecast is -2 or lower. For each case, take the coin's 5-bar return minus its normal 5-bar drift (holding the coin, over all windows), in the short direction. The measure is the mean of these unusual moves and its t, before costs.
- Supporting check: Split the cases at their median forecast. The stronger half, with the more negative forecast, must have a larger mean unusual move than the weaker half (difference above 0).
- Confirm: The idea is confirmed when the mean unusual move is positive (price fell versus drift) with t ≥ 2 over at least 30 cases, and the supporting check passes.
- Reject: The idea is rejected when the mean unusual move is negative (price rose versus drift) with t ≤ -2 over at least 30 cases.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is t ≥ 2 when the stronger half does not show the larger move, and so is any result with fewer than 30 cases.
