---
idea: 005-01_bearish-rsi-divergence-reversal
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: price makes a new high while RSI makes a lower high -> replaced: no component holds RSI's value at a past price high.
- Comparison: current RSI against RSI at the previous price high -> replaced: only RSI's current level or its rank in its history is computable.
- Outcome: price falls back, retracing part of the run-up -> kept: a short position gains when price falls.
- Verdict transfer: no: a test that swaps the swing-high RSI comparison for RSI level or rank would test an RSI-extreme or overbought idea, which the brief explicitly excludes.
Reason: A divergence needs RSI at the previous price swing high, compared with RSI at the current new high, alongside the new high in price. No catalogue component, alone or in any weighted, negated or regime composition, remembers RSI at a past price extreme. Summing a range position (Donchian) and RSI only gives "high price, low RSI", not a lower RSI high at a higher price high.
