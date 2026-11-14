---
idea: 005-06_bullish-divergence-downtrend-continues
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price at a new low while RSI makes a higher low -> replaced: the catalogue gives only RSI's level, not where RSI sits against its own earlier low.
- Comparison: the earlier price low and the RSI value at it -> replaced: no component keeps the prior low or the RSI reading there.
- Outcome: price keeps falling to further lows -> kept: a short position sized by the divergence, judged on the next bars' returns.
- Verdict transfer: no: a test of RSI level against the price range is a different signal, so its verdict would not carry over to the higher-low divergence.
Reason: The divergence compares RSI's current low with its own earlier low, at the bar of the earlier price low. No catalogue component computes that, alone or combined. Pairing `DonchianBreakoutComponent` with `RSIPullbackComponent` measures RSI's level, not a higher low, so it would replace the situation.
