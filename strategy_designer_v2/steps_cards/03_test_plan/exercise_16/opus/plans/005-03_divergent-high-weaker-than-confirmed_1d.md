---
idea: 005-03_divergent-high-weaker-than-confirmed
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: a new price high whose RSI is below its prior RSI high -> adapted: the new close high becomes a regime rule, and the divergence becomes a graded RSI shortfall; no catalogue component computes that shortfall.
- Comparison: divergent new highs against confirming new highs (RSI also at a new high) -> kept: the shortfall's sign and size separate the two cases.
- Outcome: weaker returns after divergent highs, towards a reversal down -> adapted: the forecast is graded short with the shortfall, so the hold lasts only while the situation does.
- Verdict transfer: no: without a component that compares RSI with its own recent high, the divergence cannot be measured, so no config can carry the verdict.
Reason: The bars hold everything the idea needs (closes give both the price high and RSI). The config's logic could hold it: a regime on `DonchianBreakoutComponent` at +sf for the new close high, plus a graded component inside it. But no component measures RSI against its own maximum over the lookback. `RSIPullbackComponent` gives only the RSI level. `percentile` cannot be used: it ranks against the whole stored history, not the divergence window, and as a second history op next to `standardise` V15 refuses it.
