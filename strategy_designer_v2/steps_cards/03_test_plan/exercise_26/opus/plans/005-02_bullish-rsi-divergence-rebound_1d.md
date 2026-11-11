---
idea: 005-02_bullish-rsi-divergence-rebound
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new low -> adapted: graded as how close the close sits to the bottom of its recent range (Donchian position).
- Comparison: RSI makes a higher low than at the previous price low -> replaced: no catalogue component reads RSI at the previous price low, so it has no measure.
- Outcome: price rebounds, recovering part of the decline into that low -> kept: a long forecast, judged on the following return.
- Verdict transfer: no: without the RSI-at-prior-low comparison, the test measures new lows rather than divergent new lows.
Reason: The idea compares RSI now with RSI at the bar of the previous price low. That needs a remembered swing-low bar and the RSI value on it. All of this is in the coin's own closes, but no catalogue component gives RSI at a prior low, RSI's rolling minimum, or RSI's position in its own range. Weighted sums of the RSI, Donchian and price-evolution components only add the two readings; they cannot express "price lower but RSI higher".
