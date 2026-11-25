---
idea: 058-02_calm-range-bottom-drifts-up
brief: 058_choppy-calm-range-edge-reversion
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 088be9d08c17
---
Fidelity:
- Situation: in a choppy calm market, the close's nearness to the bottom of its 20-day high-low range -> replaced: no listed component gives the close's position in the high-low range; Donchian reads only the closing range.
- Comparison: nearer the bottom against farther from it (graded pull) -> kept: a graded position in the range, larger nearer the low.
- Outcome: a larger rise over the next 5 days -> kept: 5 bars on daily bars, long side.
- Verdict transfer: no: a test on the closing range measures a different edge than the 20-day high-low range the idea names.
Reason: The idea needs where the close sits inside the 20-day high-low range. The listed `DonchianBreakoutComponent` params are only `period` and `scaling_factor`, so it uses the closing range only. No sum or difference of the listed components (for example `DistanceFromHighComponent` against the high or the low) gives (close − L) / (H − L).
