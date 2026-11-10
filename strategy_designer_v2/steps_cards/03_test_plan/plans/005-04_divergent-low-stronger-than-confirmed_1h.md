---
idea: 005-04_divergent-low-stronger-than-confirmed
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1h
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: a new price low with a higher RSI low -> replaced: no catalogue component compares RSI now with RSI at the earlier price low.
- Comparison: new price lows where RSI also makes a new low -> replaced: telling these lows apart needs the same missing RSI-against-its-earlier-low reading.
- Outcome: price rises more after divergent lows than after confirmed lows -> kept: a long position judged on next returns.
- Verdict transfer: no: without a divergence measure, the forecast would test RSI level or range position, not divergence.
Reason: The idea needs RSI at the current price low compared with RSI at the prior price low, graded and active only near new lows. Closes are enough to compute it. No catalogue component does this. `RSIPullbackComponent` gives only the RSI level and `DonchianBreakoutComponent` only the price's place in its range. A rolling minimum or rank of RSI is not available inside `strategies`, because `percentile` cannot sit beside `standardise`. A regime percentile gate would only switch on and off, not measure the divergence.
