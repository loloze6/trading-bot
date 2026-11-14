---
idea: 005-04_divergent-low-stronger-than-confirmed
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: a new price low on BTC, ETH or BNB where RSI makes a higher low -> replaced: the catalogue has the RSI level only, not RSI against its own prior low.
- Comparison: against new price lows where RSI also makes a new low -> replaced: the same missing RSI-versus-prior-low reading is needed to tell the two groups apart.
- Outcome: returns after the higher-RSI-low case are stronger, that is, the price rises more -> adapted: "after the new low" becomes "while at the new low", sized by the strength of the divergence.
- Verdict transfer: no: a test built on the RSI level would judge oversold extremes, which the brief excludes, not divergence.
Reason: A divergence compares the RSI now with the RSI at the earlier price low. `DonchianBreakoutComponent` gives where the close sits in its range, and `RSIPullbackComponent` gives only the current RSI level. No component, alone or combined, gives where the RSI sits relative to its own recent lows, so "higher RSI low" and "new RSI low" cannot be told apart.
