---
idea: 005-04_divergent-low-stronger-than-confirmed
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new low while RSI makes a higher low -> replaced: no component compares RSI with its own earlier low; RSI level or range position would stand in for it.
- Comparison: divergent new lows against new lows where RSI also makes a new low -> replaced: needs the same missing RSI-against-its-prior-low reading to split the two groups.
- Outcome: stronger (upward) returns after divergent lows -> kept: forward returns of a long position, judged against holding the coin.
- Verdict transfer: no: with RSI level or Donchian position in place of the divergence, the test would measure oversold or range-bottom effects, which the brief explicitly excludes.
Reason: The idea needs RSI's position against its own recent low at the bar where price sets a new low. The catalogue has RSI only as a level (50 - RSI), and the one history op allowed in a forecast (`standardise`) cannot rank RSI against its own range. A Donchian-bottom regime plus the RSI level would give "oversold at a new low", not "RSI higher low at a new low".
