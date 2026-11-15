---
idea: 002-04_price-cross-below-long-sma.d1_below-average-fall-not-stretched
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: close below its long average, and whether it has fallen sharply and far beneath its recent high -> replaced: depth below the long average can be kept (graded, read as "while"), but no component gives the fall from the recent high, so a proxy would be needed.
- Comparison: an orderly decline judged against a deep, fast fall below the recent high -> replaced: only Donchian range position or the distance from a short EMA could stand in for depth below the high.
- Outcome: keeps falling more the deeper below the average, and rebounds more strongly the deeper and faster the fall -> kept: a short graded by depth below the average, and a long graded by the depth and speed of the fall.
- Verdict transfer: no: a proxy for the fall from the recent high would test a different quantity, so neither result would carry over to the idea.
Reason: The rebound exception needs how far the close sits beneath its recent highest close, and how fast it got there. No catalogue component or combination computes this. Donchian position is scaled to the range, not to the depth from the high, and PriceEvolution measures from a fixed past bar, not from the high. Everything else could be held in a "below the long average" regime with graded short and long parts.
