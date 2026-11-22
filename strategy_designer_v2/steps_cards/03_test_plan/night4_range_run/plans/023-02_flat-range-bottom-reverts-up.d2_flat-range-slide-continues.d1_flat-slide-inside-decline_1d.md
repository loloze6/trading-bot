---
idea: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.d1_flat-slide-inside-decline
brief: 023_range-reversion-when-no-trend
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 10d8cbead801
---
Fidelity:
- Situation: a flat 30-day coin (small net move against its high-low range), closing below the range's middle, with a 10-day fall, while its 60-day return is negative -> replaced: the flat and below-middle parts can be regime rules (NetMoveToRangeRatio 30 high_low; IchimokuCloudPosition with all periods 30 and displacement 0 for the high-low midpoint), but no component computes the 10-day fall graded jointly with the 60-day fall; a weighted sum would short on a 60-day fall alone.
- Comparison: the deeper the 60-day fall, the larger the effect; none when the 60-day return is positive -> replaced: no component interacts the two falls; only a sum is available, and a sum is a different quantity.
- Outcome: the coin falls over the next 5 days (short) -> kept: a 5-bar horizon on daily bars.
- Verdict transfer: no: a sum of the 10-day and 60-day falls is not the idea's product, so neither a confirm nor a reject would carry over to the idea.
Reason: The idea's size is the 10-day fall scaled by the depth of the 60-day fall, and it is zero when either fall is absent. The config can only add standardised components, and score_product only selects a regime, so no catalogue component or combination computes this product from the closes.
