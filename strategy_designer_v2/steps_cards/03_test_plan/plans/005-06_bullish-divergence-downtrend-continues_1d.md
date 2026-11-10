---
idea: 005-06_bullish-divergence-downtrend-continues
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new low while RSI makes a higher low -> replaced: no catalogue component, alone or combined, compares RSI at the current low with RSI at the prior price low.
- Comparison: divergent new lows against new lows without divergence -> kept: a regime on "close at its range low" with a graded divergence size inside it would hold this, if the divergence measure existed.
- Outcome: price keeps falling to further lows -> kept: a short position graded by divergence strength gains when price falls.
- Verdict transfer: no: without a divergence measure, any proxy (an RSI level, or the range position) tests a different idea.
Reason: The divergence needs the RSI value at the bar of the previous price low, set against the RSI now. No catalogue component stores or compares RSI across two swing lows. I tried composing the range position (`DonchianBreakoutComponent`) with the RSI level (`RSIPullbackComponent`). That only gives "price low, RSI not oversold", which is not a higher RSI low. The data needed is only this coin's own closes, and a regime gate plus a graded component could carry the idea, so the gap is a component.
