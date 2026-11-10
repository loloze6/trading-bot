---
idea: 005-01_bearish-rsi-divergence-reversal
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price closes at a new recent high -> kept: DonchianBreakoutComponent gives +sf when the close is the highest of its window.
- Comparison: RSI now is below RSI at the previous price high -> replaced: no component stores RSI at a past price pivot, and RSI rank against its own history is a different quantity.
- Outcome: price falls and retraces part of the run-up -> adapted: a negative forecast sized by divergence strength, judged over a fixed horizon.
- Verdict transfer: no: without RSI measured at the previous price high, the test would judge "high price with weak RSI", not divergence.
Reason: The idea compares today's RSI with RSI at the previous price high. That needs a pivot-anchored memory, which is computable from one coin's closes, but no catalogue component computes it. I tried a weighted sum of DonchianBreakout and negated RSIPullback, and a score_product regime of Donchian times RSI percentile. Both measure RSI against its average or its own history, not against its value at the prior high, so they replace the comparison.
