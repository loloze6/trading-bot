---
idea: 005-06_bullish-divergence-downtrend-continues
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: price makes a new low while RSI makes a higher low -> replaced: no component compares RSI at the new low with RSI at the prior low.
- Comparison: the current RSI low against the earlier RSI low, at the earlier price low -> replaced: RSI can only be read as a level or ranked inside `percentile`, which `standardise` blocks in strategies.
- Outcome: price then keeps falling to further lows -> kept: a graded short sized by the divergence, judged on the forward return.
- Verdict transfer: no: RSI level or a whole-history RSI rank joined to the price's range position is a different quantity from the divergence, so neither verdict would carry over.
Reason: The divergence needs RSI's position within its own recent range, set against the close's position within its range. Both can be computed from closes, and a graded difference fits the config's logic. The catalogue only has the close's range position (`DonchianBreakoutComponent`) and the RSI level (`RSIPullbackComponent`), and no transform can rank RSI against its own window inside a strategies component.
