---
idea: 005-01_bearish-rsi-divergence-reversal
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Untestable: The idea compares RSI at the current price high with RSI at the previous price high, which needs a memory of past swing highs. No catalogue component finds swing highs or records RSI at them; the closest composition, a Donchian range position combined with RSI level, drops that peak-to-peak comparison and becomes a plain range-fade. The brief's own test, divergent new highs against non-divergent new highs, cannot be built either, because the detector has no rule that can flag a divergence.
