---
idea: 005-02_bullish-rsi-divergence-rebound
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new low -> adapted: graded as where the close sits in its recent range (Donchian position, negated).
- Comparison: RSI at this low is higher than RSI at the previous price low -> replaced: no component recalls RSI at the previous swing low, so only the current RSI level is available.
- Outcome: price rebounds and recovers part of the decline -> kept: long position, gains when price rises over the next bars.
- Verdict transfer: no: without the RSI value at the previous low, the test would check "price low, RSI not oversold", which is not a divergence.
Reason: The divergence needs the RSI value at the previous price low. That can be computed from the coin's own closes, and a graded value would fit the config's logic. No catalogue component, alone or combined, computes it. `RSIPullbackComponent` gives only the current RSI level, and `DonchianBreakoutComponent` gives only where price sits in its range. Neither gives RSI's own swing lows or the RSI value at the bar of a previous price low.
