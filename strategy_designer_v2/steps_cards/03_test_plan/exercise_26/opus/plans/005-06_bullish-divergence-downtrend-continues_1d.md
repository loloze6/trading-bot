---
idea: 005-06_bullish-divergence-downtrend-continues
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new low -> adapted: graded as where the close sits in its recent range (Donchian), most negative at the range low.
- Comparison: RSI makes a higher low than at the prior price low -> replaced: no component reads RSI at the earlier price low, so no catalogue quantity measures it.
- Outcome: price keeps falling to further lows -> kept: a short position gains when price falls over the next bars.
- Verdict transfer: no: without RSI at the prior low, the test could not tell divergent new lows from plain new lows, which is exactly what the idea is about.
Reason: The divergence compares current RSI with RSI at the previous price low. No catalogue component keeps or returns RSI at an earlier swing low. Combining components does not fix this: RSIPullbackComponent gives only the current RSI, and adding it to DonchianBreakoutComponent in a weighted sum measures "price low while RSI is not low", not "RSI higher than at the prior low". That sum is also non-zero on every bar, not only at new lows. Everything needed is in one coin's closes, so the config's logic could hold such a component.
