---
idea: 002-03_price-cross-above-long-sma.g1_saturday-crypto-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: untestable
---
Fidelity:
- Situation: the coming day is a UTC Saturday -> adapted: "while" the coming bar is stamped Saturday (WeekdayComponent, regime rule between 4.5 and 5.5)
- Comparison: Saturday's return against the other days' returns -> kept: other days are flat, so Saturday's gain is measured against them
- Outcome: the next 1-day return is larger, upward -> replaced: a graded forecast needs a strength the idea lacks, so it would size the position on another indicator
- Verdict transfer: no: a test sized by any graded indicator measures that indicator's timing, not the Saturday effect.
Reason: The idea is a calendar condition with no strength. It calls for a fixed long position on Saturday bars and none on other days. Only a constant inside a regime can do that, and the guide forbids it, because every forecast must be graded and no constant may sit in a regime. Any graded component in the Saturday regime would replace the idea's situation with a different quantity.
