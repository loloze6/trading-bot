---
idea: 005-03_divergent-high-weaker-than-confirmed
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
outcome: missing-components
---
Fidelity:
- Situation: close makes a new price high -> kept: a regime rule on DonchianBreakoutComponent at +sf (close is the highest of the window).
- Comparison: the RSI high is lower than the RSI high at the prior price high -> replaced: no catalogue component compares RSI with its own earlier high.
- Outcome: weaker (lower) returns after divergent highs than after confirmed highs -> kept: a graded position, short as the RSI shortfall grows.
- Verdict transfer: no: any catalogue stand-in, such as the RSI level, measures a different quantity from RSI against its own prior peak.
Reason: All the idea needs is in the coin's own closes. The new-high gate fits a regime rule on DonchianBreakoutComponent, but no component measures how far RSI falls short of its own prior high. RSIPullbackComponent (RSI level), MomentumDivergenceComponent (agreement between two horizons) and price-range or EMA-distance measures, alone or combined, compare RSI with 50 or price with price, never RSI with its earlier peak.
