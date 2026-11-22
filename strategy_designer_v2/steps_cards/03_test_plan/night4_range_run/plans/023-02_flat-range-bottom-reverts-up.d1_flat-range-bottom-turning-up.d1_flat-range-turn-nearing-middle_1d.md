---
idea: 023-02_flat-range-bottom-reverts-up.d1_flat-range-bottom-turning-up.d1_flat-range-turn-nearing-middle
brief: 023_range-reversion-when-no-trend
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: be08f97ea86e
---
Fidelity:
- Situation: the 30-day net move is small against the 30-day high-low range, the close sits below the range's middle, and there has been a 10-day rise that brought the close near the middle -> adapted: "small" and "below the middle" become a regime gate; the rise and the nearness to the middle should be graded, but no component measures that nearness.
- Comparison: larger 10-day rises and closes nearer the middle, against small turns or closes still deep in the range -> kept: this is the grading of the forecast.
- Outcome: the coin rises over the next 5 days (5 bars) -> kept.
- Verdict transfer: no: a forecast that grows as the close nears the range middle from below cannot be built, so the test would not measure the idea's main comparison.
Reason: Flatness and "below the middle" fit a regime: `NetMoveToRangeRatioComponent` (30) and `DonchianBreakoutComponent` (high_low, sf 1, below 0). The forecast must then grow with the 10-day rise and with nearness to the middle, but every range-position component grows with distance from the middle. Two workarounds fail: a weighted sum turns short when the close is deep and the rise is small, and the only offset that would fix this, a constant, is forbidden inside a regime.
