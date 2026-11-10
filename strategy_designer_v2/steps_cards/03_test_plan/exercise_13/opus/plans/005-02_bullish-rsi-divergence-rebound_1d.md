---
idea: 005-02_bullish-rsi-divergence-rebound
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: price closes at a new low (below the previous swing low) while RSI(14) at this low is higher than RSI was at that previous price low -> replaced: no catalogue component, alone or combined, compares RSI at the current low with RSI at the earlier price low. The closest build would add a price-range position (DonchianBreakoutComponent, negated) to a contrarian RSI level (RSIPullbackComponent). That measures "price near its low and RSI low", which is the RSI-extreme question the brief explicitly excludes, not a divergence.
- Comparison: RSI at the current price low against RSI at the previous price low (a higher low), and, per the brief, moves after divergent new lows against moves after non-divergent new lows -> replaced: the weighted mean of standardised components is additive and has no memory of a past bar's RSI. A `percentile` of RSI ranks it against all past RSI values, not against the RSI reading at the prior price low. Score_product can multiply two current readings but cannot look up the earlier one.
- Outcome: price rebounds after the divergent low and recovers part of the decline into it (upward) -> adapted: the holding period and the "part of the decline" target are dropped. The outcome becomes the coin's forward return over a fixed horizon while the forecast is long, judged against holding the coin.
- Verdict transfer: no: without a measure of RSI at the previous price low, any buildable forecast tests whether oversold new lows rebound, not whether fading momentum behind a new low does. A confirmation or rejection would therefore say nothing about divergence.
Reason: The idea needs the RSI value at the previous price low, compared with the RSI value at the current new low. Both come from the coin's own closes, and a graded forecast could carry the result (zero when there is no new low, growing with the RSI higher-low margin, long only). No catalogue component records RSI at a past swing low. No composition of current-bar readings (Donchian position, RSI level, percentile ranks) can express that comparison.
