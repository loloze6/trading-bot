---
idea: 005-04_divergent-low-stronger-than-confirmed
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: new price low while RSI makes a higher low -> replaced: no component gives the RSI at the prior price low, so only RSI level or the close's range position could stand in.
- Comparison: new price lows where RSI also makes a new low -> replaced: the same missing RSI-at-prior-low reading is needed to tell confirming lows from diverging ones.
- Outcome: stronger (upward) returns after diverging lows than after confirming lows -> kept: the portfolio's value after the position can measure it.
- Verdict transfer: no: a test built from RSI level and range position would test oversold or range reversion, not divergence.
Reason: The idea needs the RSI on the current new low compared with the RSI at the previous price low, and the catalogue has no such reading. RSI comes only as a level (RSIPullbackComponent), and `percentile` cannot stand in for RSI's own rolling low because `standardise` must be the only history op. Composing it with Donchian range position or a regime veto still gives "oversold at a range low", not "RSI higher than at the prior low".
