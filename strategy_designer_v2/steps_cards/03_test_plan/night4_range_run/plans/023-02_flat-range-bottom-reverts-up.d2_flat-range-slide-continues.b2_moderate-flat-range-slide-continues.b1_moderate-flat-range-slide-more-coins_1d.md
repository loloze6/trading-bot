---
idea: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b2_moderate-flat-range-slide-continues.b1_moderate-flat-range-slide-more-coins
brief: 023_range-reversion-when-no-trend
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: be08f97ea86e
---
Fidelity:
- Situation: a 30-day net move small against the 30-day high-low range, the close below that range's middle, and a negative 10-day return -> adapted: "small" and "below the middle" become regime conditions, and the 10-day return sets the size; but no available component gives the close's place in the high-low range.
- Comparison: the fall is moderate, not extreme, against the coin's own recent 10-day moves -> adapted: a veto on the 10-day return measured in usual 10-day moves.
- Outcome: the price falls over the next 5 days (short) -> kept: the 5-bar horizon on daily bars.
- Verdict transfer: no: without the close's place in the 30-day high-low range, the situation cannot be built as the idea states it.
Reason: The flatness (`NetMoveToRangeRatioComponent`, `source` "high_low") and the 10-day fall in usual moves (`MeanAbsScaledReturnComponent`) exist. No allowed component gives where the close sits against the middle of the 30-day high-low range: `DonchianBreakoutComponent` accepts only the closing range, and regime rules cannot combine `DistanceFromHighComponent`'s high and low readings into one midpoint test.
