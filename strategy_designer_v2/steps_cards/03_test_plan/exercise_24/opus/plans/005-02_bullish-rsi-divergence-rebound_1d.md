---
idea: 005-02_bullish-rsi-divergence-rebound
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new low -> adapted: graded as the close's position in its 48-bar range (DonchianBreakoutComponent), most bullish at the bottom.
- Comparison: RSI makes a higher low than at the previous price low -> replaced: no component records the RSI at the previous price low, so only the current RSI level could be used.
- Outcome: price then rebounds, recovering part of the decline -> adapted: the forecast goes long while the divergence holds, and the holding period is dropped.
- Verdict transfer: no: a test of "price at a range low with RSI not oversold" does not test a higher RSI low against the previous price low.
Reason: The divergence needs the RSI value at the previous price low, compared with the RSI at the current new low. No catalogue component records it, and no combination can: the components only give the RSI level now and the price's range position now. Everything needed comes from one coin's closes, and a graded per-bar value could hold it.
