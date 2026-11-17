---
idea: 012-02_volume-burst-fall-reversal
brief: 012_liquidation-flush-partial-rebound
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: a bar that falls sharply -> adapted: graded by the size of the one-bar fall in usual moves (VolatilityScaledReturnComponent, period 1), active while it happens.
- Comparison: the larger the bar's volume relative to the coin's 30-day average volume -> replaced: no catalogue component grades volume against its 30-bar average.
- Outcome: a larger price rise over the next 3 days -> kept: 3 bars on daily bars, long.
- Verdict transfer: no: without a graded volume ratio, the test cannot show that bigger volume bursts on falling bars give bigger rebounds.
Reason: The idea sizes the bet by the bar's volume over its 30-bar average volume, but no catalogue component outputs that ratio. VolumeExpansionHedgeComponent fires only on low-volume up bars and is on/off. The volume_filter op is an on/off dead zone, so it would turn the graded volume relation into a threshold, which no allowed adaptation permits.
