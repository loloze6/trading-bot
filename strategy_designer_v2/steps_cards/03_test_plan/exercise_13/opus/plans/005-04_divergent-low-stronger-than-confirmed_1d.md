---
idea: 005-04_divergent-low-stronger-than-confirmed
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: a new price low (the close is the lowest close of the recent window) where RSI makes a higher low than at the previous price low -> replaced: the new price low can be built (the raw `DonchianBreakoutComponent` value at -sf, as a regime rule). But the catalogue only gives the current RSI level (`RSIPullbackComponent`, 50 - RSI). No component compares today's RSI with its value at the previous price low, or with its own recent minimum. Using the RSI level instead would measure a different quantity.
- Comparison: new price lows where RSI also makes a new low (confirming momentum) -> replaced: this needs the same missing RSI-against-its-prior-low reading. The sign or size of a working divergence component would separate the two kinds of low. With only the RSI level, "confirming" would just mean "low RSI", which is a different quantity.
- Outcome: stronger (upward) returns after the divergent lows than after the confirming lows -> adapted: "after the low" becomes "while the close sits at its new low". A graded long position grows with how far RSI sits above its own prior low. The holding period is dropped.
- Verdict transfer: no: a test built on the RSI level would test "oversold at a new low", which the brief rules out as a different question. Its result would therefore neither confirm nor reject the divergence idea.
Reason: The divergence compares RSI now with RSI at the previous price low (or with its own rolling minimum), and no catalogue component or composition computes it. `RSIPullbackComponent` gives only the current RSI level, and no transform can take a rolling minimum of another component's output inside the window. Everything needed is in the coin's own closes, and a graded RSI-divergence component could be held in a regime gated on the new price low, so the gap is a missing component, not a limit of the config.
