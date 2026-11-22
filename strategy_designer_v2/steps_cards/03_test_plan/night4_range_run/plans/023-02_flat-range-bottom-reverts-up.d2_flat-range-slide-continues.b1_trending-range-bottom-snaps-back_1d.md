---
idea: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b1_trending-range-bottom-snaps-back
brief: 023_range-reversion-when-no-trend
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: be08f97ea86e
---
Fidelity:
- Situation: the 30-day net move is large against the 30-day high-low range, the close sits below the middle of that high-low range, and the past 10-day fall is large -> replaced: the catalogue has no listed component for the close's position in the high-low range, only in the closing range.
- Comparison: the 10-day fall graded within the condition, larger fall against smaller fall -> kept: a negated 10-bar return, standardised, inside a regime.
- Outcome: price rises over the next 5 days -> kept: the book holds 5 bars on 1d bars.
- Verdict transfer: no: with the range middle taken from closes rather than highs and lows, the test would gate on a different set of bars.
Reason: The "below the middle of its 30-day high-low range" condition needs the close's position inside the window's max-high and min-low range. `DonchianBreakoutComponent` lists only `period` and `scaling_factor`, which give the closing range, and no rule or score combination of the high and low distance components gives close against (H + L) / 2 exactly. The other parts are buildable: `NetMoveToRangeRatioComponent` (period 30, high_low) can be a regime rule, and a negated `PriceEvolutionComponent` (period 10) can be the graded forecast.
