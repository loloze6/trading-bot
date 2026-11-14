---
idea: 005-06_bullish-divergence-downtrend-continues
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price makes a new low (close at the bottom of its recent range) while RSI makes a higher low (RSI now above the low it made at the earlier price low) -> replaced: the catalogue can see the price side (DonchianBreakoutComponent, where the close sits in its range) and the RSI level against 50 (RSIPullbackComponent). Nothing computes where RSI sits against its own earlier low. A weighted sum of price range position and RSI level measures "price low while RSI is not far below 50", which is a different quantity from an RSI higher low.
- Comparison: new price lows with an RSI higher low, against new price lows without one (the brief's test of whether divergence adds anything) -> adapted: graded, so a position that grows as the price low gets deeper while RSI holds further above its own recent low. This is only possible once the divergence itself can be measured.
- Outcome: price keeps falling to further lows after the divergence (short, continuation) -> kept: a short position, judged on the coin's next returns against holding the coin.
- Verdict transfer: no: without a measure of RSI against its own earlier low, a test built from price range position and RSI level would judge "oversold-looking lows" and not RSI divergence, so neither its confirmation nor its rejection would carry over to the idea.
Reason: The divergence needs RSI to be compared with its own earlier low over the same window in which price makes its new low. Every input is in the coin's own closes, and a graded "price range position minus RSI range position" fits the config's weighted-mean logic. However, no catalogue component outputs RSI's position within its own recent range. Linear combinations of DonchianBreakoutComponent (price range position) and RSIPullbackComponent (RSI level against 50) cannot reconstruct RSI's distance from its prior low.
