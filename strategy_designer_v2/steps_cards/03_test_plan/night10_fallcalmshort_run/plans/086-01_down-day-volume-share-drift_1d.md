---
idea: 086-01_down-day-volume-share-drift
brief: 086_calm-downtrend-down-volume-skew-continues
data-instruments: XRP, DOT, XMR, INJ, FIL, DOGE, BTC, TRX
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: bd33e939b067
---
Fidelity:
- Situation: in a falling, calm market, the share of the last 10 days' volume traded on down days -> replaced: no component or combination computes a down-day share of window volume.
- Comparison: a heavier down-day share against a balanced or up-heavy one, graded ("the larger the share") -> kept: a graded share holds this once it exists.
- Outcome: the coin falls further over the next 5 days (short side) -> kept: a 5-bar horizon on daily bars, short only.
- Verdict transfer: no: without the down-day volume share, no config built from the catalogue measures the idea's situation.
Reason: The idea needs the volume of a coin's down days (close below the prior close) summed over its last 10 bars and divided by those bars' total volume. No catalogue component outputs this. It cannot be composed either: no component outputs a per-bar down-day volume, no config step sums or divides two components over a window, and `ema` cannot sit beside `standardise`.
