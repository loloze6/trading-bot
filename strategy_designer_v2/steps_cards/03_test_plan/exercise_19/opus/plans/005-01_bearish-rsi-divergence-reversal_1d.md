---
idea: 005-01_bearish-rsi-divergence-reversal
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new high -> kept: `DonchianBreakoutComponent` gives the close's place in its range, at the top when the close is a new high.
- Comparison: RSI at this high is lower than RSI at the previous price high -> replaced: no component reads RSI at a past price high, or RSI against its own recent peak.
- Outcome: price falls back and retraces part of the run-up -> adapted: a short whose size follows the divergence, held only while it lasts.
- Verdict transfer: no: without the RSI-at-prior-high comparison, the test only checks "price at its high", not "price at its high with fading RSI".
Reason: The divergence needs RSI now compared with RSI at the previous price high, from the coin's own closes. A graded difference of standardised components could hold it, but no catalogue component reads RSI back at a past bar or against its own window. Tried: `RSIPullbackComponent` gives only the current RSI level, `DonchianBreakoutComponent` ranks closes only, and their weighted sum is "high price, low RSI", not a lower RSI high.
