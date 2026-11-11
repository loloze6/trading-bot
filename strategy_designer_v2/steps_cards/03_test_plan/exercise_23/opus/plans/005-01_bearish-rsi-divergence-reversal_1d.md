---
idea: 005-01_bearish-rsi-divergence-reversal
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new high while RSI makes a lower high -> replaced: no catalogue component gives RSI's high at past price peaks, only RSI's current level.
- Comparison: RSI now against RSI at the previous price high -> replaced: the nearest is RSI against 50, a different quantity.
- Outcome: price falls back and retraces part of the run-up -> adapted: a graded short while the divergence shows, with no holding period.
- Verdict transfer: no: a Donchian-plus-RSI-level proxy tests "high price with soft RSI", not a lower RSI high at a new price high.
Reason: The idea needs RSI compared with its value at the previous price high, or with its own recent peak, alongside price at its range top. That uses only the coin's own closes and fits a graded forecast, but no catalogue component computes it. Strategies only take weighted sums, so "price high AND RSI not high" cannot be built from DonchianBreakoutComponent and RSIPullbackComponent.
