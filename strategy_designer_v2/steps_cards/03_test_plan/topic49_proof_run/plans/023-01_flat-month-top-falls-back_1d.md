---
idea: 023-01_flat-month-top-falls-back
brief: 023_range-reversion-when-no-trend
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 051b3422f169
---
Fidelity:
- Situation: close far above the middle of the 30-day high-low range, as a share of its width, in a choppy market -> replaced: the only listed Donchian params give the 30-day closing range, not the high-low range.
- Comparison: distance from the range middle, scaled by the range width -> replaced: the middle and width would come from closes, not highs and lows.
- Outcome: price falls back toward the middle over the next 5 days -> kept
- Verdict transfer: no: a test on the closing range does not measure the high-low range the idea names.
Reason: The listed `DonchianBreakoutComponent` takes only `period` and `scaling_factor`, so its range uses closes only. `FlatnessWeightedRangePositionComponent` ("high_low") multiplies the position by a flatness factor the idea does not have. No composition gives the close's signed position in the 30-day high-low range.
