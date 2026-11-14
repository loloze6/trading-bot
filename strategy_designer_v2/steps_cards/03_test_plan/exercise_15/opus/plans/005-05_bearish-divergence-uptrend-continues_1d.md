---
idea: 005-05_bearish-divergence-uptrend-continues
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price at a new high while RSI peaks below its earlier high -> replaced: no component compares RSI with its own earlier peak, so only RSI level or rank would be available.
- Comparison: the RSI high against its prior high, and price above its prior high -> adapted: the price side is kept graded as the close's place in its range (Donchian), but the RSI side has no counterpart.
- Outcome: price keeps rising to further highs (long) -> adapted: a long position held while the divergence lasts, judged on the return over a fixed horizon.
- Verdict transfer: no: a test on RSI level instead of "RSI lower high" would judge weak-momentum highs, not divergences.
Reason: The divergence needs RSI's current value compared with its own highest value over the same lookback in which price sets its high. No catalogue component does this. RSIPullbackComponent gives only the current RSI. Weighted sums, negation and percentile ranks over the detector's fixed history cannot rebuild a windowed RSI maximum. Everything needed is in the coin's own closes, and a regime rule or a graded component could hold the result.
