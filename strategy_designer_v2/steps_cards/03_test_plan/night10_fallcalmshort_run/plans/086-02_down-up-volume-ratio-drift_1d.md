---
idea: 086-02_down-up-volume-ratio-drift
brief: 086_calm-downtrend-down-volume-skew-continues
data-instruments: XRP, DOT, XMR, INJ, FIL, DOGE, BTC, TRX
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: bd33e939b067
---
Fidelity:
- Situation: falling calm market, 20-day average down-day volume exceeding average up-day volume -> replaced: no catalogue component splits volume by up and down days, so only a different volume measure could stand in.
- Comparison: down-day share heavier than a balanced or up-heavy share -> replaced: it rests on the same missing up and down volume averages.
- Outcome: the coin falls further over the next 5 days (5 bars), short -> kept
- Verdict transfer: no: any stand-in volume measure would test a different quantity, not the up and down volume skew.
Reason: The idea needs a coin's average volume on down-close days compared with its average on up-close days over 20 bars. No catalogue component computes this. The weighted means, negative weights, offsets and history ops the guide allows cannot build a conditional average by bar direction, because no component outputs sign(return) x volume.
