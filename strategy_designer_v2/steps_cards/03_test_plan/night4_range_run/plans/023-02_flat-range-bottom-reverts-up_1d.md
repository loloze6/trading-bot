---
idea: 023-02_flat-range-bottom-reverts-up
brief: 023_range-reversion-when-no-trend
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: 30-day net move small relative to the 30-day high-low range -> replaced: no component computes net move over high-low range; the efficiency ratio divides by path length instead.
- Comparison: how far the close sits below the middle of the 30-day high-low range -> replaced: DonchianBreakoutComponent locates the close in its range of closes, not of highs and lows.
- Outcome: the coin rises over the next 5 days -> kept: 5 bars on daily bars.
- Verdict transfer: no: a test gated on path efficiency and a close-only range would judge a different "flat month" and a different middle.
Reason: The no-trend condition needs the absolute 30-bar net close change divided by the 30-bar high-low range. The graded signal needs the close's position against the midpoint of the 30-bar high and low. Both come from one coin's own bars, and a regime rule plus a graded component could hold them. No catalogue component computes either, and no weighted sum, product or regime rule over existing components forms the needed ratio.
