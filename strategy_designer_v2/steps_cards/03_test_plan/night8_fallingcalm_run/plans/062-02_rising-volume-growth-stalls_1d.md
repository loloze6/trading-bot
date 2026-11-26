---
idea: 062-02_rising-volume-growth-stalls
brief: 062_rising-market-volume-dry-up-continues
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: ca7c09a81ba4
---
Fidelity:
- Situation: in a rising market, volume over the past 30 days against the 30 days before -> kept: the profile "rising" is added by code, and the 30-day over prior 30-day log volume ratio is measured inside it.
- Comparison: the more volume has grown, the smaller the rise -> kept: the position is graded by the size of the volume change, from shrink to growth.
- Outcome: smaller rise over the next 5 days the more volume grew -> kept: 5-day forward return, judged net of the coin's drift.
- Verdict transfer: yes: the relation is measured exactly as stated, inside the stated profile, over the stated horizon.
Forecast: One component, `VolumeRatioComponent` with `period` 30, `exclude_current` 30, `short_period` 30 and `form` "log". It gives ln(mean volume of the last 30 days / mean volume of the 30 days before). It is standardised over its past 60 values and then negated. The forecast is positive (long) when volume has shrunk, and larger the more it shrank. It is negative (short) when volume has grown, and larger in size the more it grew. It is near 0 when volume held steady. It exists only inside the rising profile, which code adds.
Config: 062-02_rising-volume-growth-stalls_1d_config.json
Profile: rising (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 5 bars
- Main measure: On each window's non-overlapping 5-bar grid, take the bars with a non-zero forecast. On those bars, regress the coin's 5-day forward return minus its mean 5-day return over all windows (holding the coin) on the forecast. The measure is the slope's t, with cases of the same day taken together.
- Supporting check: none
- Confirm: The slope is positive with t >= 2. Rises are larger after shrinking volume and smaller after growing volume, beyond the coin's drift.
- Reject: The slope is negative with t <= -2. Rises are larger after growing volume.
- Inconclusive: A t between -2 and +2 is inconclusive. Fewer than 200 non-overlapping in-profile cases is also inconclusive, whatever the t.
