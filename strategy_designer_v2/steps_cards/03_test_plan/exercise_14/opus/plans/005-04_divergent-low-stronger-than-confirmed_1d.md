---
idea: 005-04_divergent-low-stronger-than-confirmed
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: the close makes a new low over a recent window, while RSI stays above the low it made at the earlier price low (a higher RSI low) -> replaced: no catalogue component, alone or combined, measures RSI against its own earlier low. `DonchianBreakoutComponent` can mark the new price low (a regime rule on its raw value at -sf). But `RSIPullbackComponent` only gives the RSI level (50 - RSI), and an RSI level at a new low is not the same as RSI being above its earlier low.
- Comparison: new price lows where RSI also makes a new low (confirming momentum) -> replaced: this needs the same RSI-against-its-own-earlier-low measure, so it cannot be separated from divergent lows with the existing components.
- Outcome: price rises more after divergent new lows than after confirming new lows -> adapted: "after the low" becomes "while the new-low regime is active", with the long position graded by the divergence strength and no holding period.
- Verdict transfer: no: using the RSI level at a new low in place of RSI against its prior low tests whether oversold lows bounce, which the brief explicitly says is not its question, so neither a confirmation nor a rejection would carry over to the divergence idea.
Reason: The idea needs RSI compared with its own value at the previous price low, which comes from one coin's closes and fits the config's logic. That logic would be a regime on "close at its window low" (Donchian raw at -sf) plus a graded long component sized by how far RSI sits above its window low. No catalogue component gives RSI's position within its own recent range, and no composition of the existing components (RSI level, price range position, the transforms) produces it.
