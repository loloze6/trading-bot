---
idea: 023-03_flatter-range-stronger-reversion
brief: 023_range-reversion-when-no-trend
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: be08f97ea86e
---
Fidelity:
- Situation: the close sits some distance from the middle of its 30-day range, and the 30-day net move is small relative to that range -> kept: `FlatnessWeightedRangePositionComponent` (period 30) is the range position times (1 - net move / closing range).
- Comparison: for the same distance from the middle, smaller net move against larger net move -> adapted: graded as a product, so the position grows as the net move shrinks at any given distance, instead of comparing separate groups.
- Outcome: over the next 5 days the price moves back toward the middle (down from above, up from below) -> kept: `negate` makes the forecast short above the middle and long below it, held for 5 bars.
- Verdict transfer: yes: the forecast's size is the idea's distance-times-flatness, and the supporting check isolates the flatness part, so a confirm or a reject carries over to the idea.
Forecast: One component, FlatnessWeightedRangePositionComponent with period 30, computed on daily closes. Its raw value is (2 x pos - 1) x (1 - |close[t] - close[t-30]| / (H - L)), where pos is where the close sits in its 30-day closing range [L, H]. It is standardised over 60 bars (min_periods 20) and negated. The forecast is short when the close is above the range's middle and long when it is below. It is near zero when the close is at the middle or when the 30 days moved strongly one way. Its size grows with the distance from the middle and with the flatness of the 30 days, capped at ±20. The strategy is ungated and has no dead zone, because the idea is a steady relation and not a rare extreme.
Config: 023-03_flatter-range-stronger-reversion_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Use the non-overlapping 5-bar grid of each window. For each grid bar, multiply the forecast / 10 by the coin's 5-day return minus its normal drift (the coin's mean 5-day return over all its windows). Take the mean of these products over all coins and windows, with the t of that mean.
- Supporting check: Recompute from prices, on the same grid, the reversion return per unit of distance: the 5-day return in the direction of the middle, divided by |2 x pos - 1|. Split the bars into a flatter half and a less-flat half at the median of the flatness factor. The check is the mean of the flatter half minus the mean of the less-flat half. It passes when this difference is above 0.
- Confirm: The main mean is positive with t ≥ 2, and the supporting difference is positive.
- Reject: The main mean is negative with t ≤ -2, or the supporting difference is negative with Welch t ≤ -2.
- Inconclusive: Any other result is inconclusive, as is a count below 300 grid cases with a nonzero forecast across all coins and windows.
