---
idea: 017-06_settlement-volume-rises-with-trend
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: untestable
catalogue: 4e6cc97f57e5
---
Fidelity:
- Situation: hours around 00:00, 08:00 and 16:00 UTC, and the size of the absolute 3-day return -> replaced: no component reads the hour of day, and none gives an absolute 72-bar return.
- Comparison: the coin's own volume in the other hours of the day -> replaced: the config cannot group bars by clock hour.
- Outcome: volume is raised around settlement, more so after larger 3-day moves; no price direction -> replaced: a position earns only from price moves, so a volume outcome cannot be scored.
- Verdict transfer: no: no position's gain or loss can confirm or reject a claim about volume levels by clock hour.
Reason: The idea predicts a rise in volume, not a price move in any direction. A forecast sets a long or short position that gains or loses only with price, so no config can bet on this outcome. Separately, the situation needs the hour of day, and no component computes it; but the volume outcome alone already rules out a test.
