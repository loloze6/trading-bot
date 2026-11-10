---
idea: 005-02_bullish-rsi-divergence-rebound
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price closes at a new low below its previous swing low -> adapted: the close's position in its recent range (DonchianBreakoutComponent) gives a graded "near a new low".
- Comparison: RSI now is higher than RSI at the previous price low -> replaced: no component recalls RSI at a past swing low; RSI level vs 50 or RSI's own range is a different quantity.
- Outcome: price rebounds, recovering part of the decline (up) -> kept: a long forecast scored on the forward return over the next bars.
- Verdict transfer: no: without RSI at the prior low, the test measures "new low with RSI not oversold", not a divergence, so neither result would settle the idea.
Reason: The idea needs RSI at the current low compared with RSI at the previous swing low of the closes. That is in one coin's closes and could be held as a graded, stateless value, but no catalogue component picks out a past swing low or keeps an indicator's value at it. Combining RSIPullbackComponent, DonchianBreakoutComponent and PriceEvolutionComponent cannot give it, since weights and transforms only combine values from the current bar.
