---
idea: 016-07_up-volume-burst-reversal
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 4e6cc97f57e5
---
Fidelity:
- Situation: coin has risen over the past 3 days, with a larger share of that period's volume in its few busiest hours -> replaced: no component or combination measures the share of the 72-bar volume traded in its top hours.
- Comparison: larger versus smaller busiest-hours volume share among rises -> kept: a graded size on the concentration, if it could be computed.
- Outcome: the coin gives back more of the rise over the next 3 days (down) -> adapted: "after X" becomes "while X", held as a graded short over 72 bars.
- Verdict transfer: no: without the concentration measure, the test could only judge rises in general, not burst-volume rises.
Reason: The "has risen over 72 bars" condition is available: it is `PriceEvolutionComponent` with period 72, used in a regime rule. The idea's core measure is the share of the 72-bar volume traded in its few busiest hours, and nothing in the catalogue computes it. `VolumeRatioComponent` compares only the latest bars' volume with a base, and no op ranks volumes inside a window and sums the largest ones, so no combination can rebuild it.
