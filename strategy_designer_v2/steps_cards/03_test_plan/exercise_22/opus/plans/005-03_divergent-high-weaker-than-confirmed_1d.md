---
idea: 005-03_divergent-high-weaker-than-confirmed
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: a new price high whose RSI peak is below the prior RSI peak -> replaced: no catalogue component measures RSI against its own earlier high.
- Comparison: returns after divergent new highs versus after RSI-confirmed new highs -> kept: a forecast signed by the divergence size compares the two groups.
- Outcome: weaker or lower price after divergent highs -> kept: measured by gains from shorting in proportion to the divergence.
- Verdict transfer: no: the RSI level alone (RSIPullback) cannot tell a lower RSI high from a confirming one, so the result would not decide the idea.
Reason: The divergence needs RSI's current value measured against its own recent peak, at the bar where price sits at the top of its range. This uses only the coin's closes, and a graded component could hold it. The catalogue has `DonchianBreakoutComponent` for price, but nothing gives RSI's position in its own range. RSIPullback with `standardise` scales by mean size, not by the peak, and percentile ops cannot sit beside `standardise`.
