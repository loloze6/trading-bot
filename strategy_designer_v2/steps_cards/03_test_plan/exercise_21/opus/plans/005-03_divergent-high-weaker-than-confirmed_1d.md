---
idea: 005-03_divergent-high-weaker-than-confirmed
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: a new price high reached with RSI below its prior RSI high -> replaced: the catalogue gives RSI's level and the close's range position, but nothing measures RSI against its own earlier high.
- Comparison: new price highs where RSI also makes a new high -> kept: same new-high bars, graded by how far RSI falls short of its high.
- Outcome: weaker returns after divergent highs than after confirmed ones -> adapted: forward returns of a position graded by the RSI shortfall at new highs.
- Verdict transfer: no: RSI level at a new high is not RSI's shortfall from its own prior high, so neither verdict would carry to the idea.
Reason: The new price high is available (`DonchianBreakoutComponent` at +sf, usable as a regime rule). No component or allowed composition computes RSI relative to its own rolling high: `standardise` must be the only history op, and there is no rolling-max op. RSI level alone would replace the divergence with an RSI-extreme reading, and the brief rules that out explicitly.
