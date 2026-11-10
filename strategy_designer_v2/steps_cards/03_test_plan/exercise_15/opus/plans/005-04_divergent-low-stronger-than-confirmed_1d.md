---
idea: 005-04_divergent-low-stronger-than-confirmed
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: a new price low reached with a higher RSI low -> replaced: the catalogue has nothing that compares the current RSI with its earlier lows.
- Comparison: the same returns after new lows where RSI also makes a new low -> kept: the forecast record can split new-low bars by the size of the RSI divergence.
- Outcome: price rises more after divergent lows (a reversal up) -> kept: forward returns from the forecast record.
- Verdict transfer: no: no catalogue combination measures "RSI above its prior low while price is at its low". A sum of range position and RSI level is long on any low or any high RSI, not on the divergence.
Reason: The idea needs RSI's own rolling minimum set against price's rolling minimum on the same bar. No catalogue component outputs RSI's rolling extreme, and the strategy forecast cannot multiply or condition one component on another. `DonchianBreakoutComponent` covers price's range position, and `RSIPullbackComponent` covers only RSI's current level, not its prior low.
