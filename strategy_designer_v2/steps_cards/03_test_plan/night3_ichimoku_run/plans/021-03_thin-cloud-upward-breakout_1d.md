---
idea: 021-03_thin-cloud-upward-breakout
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: a31b77de3651
---
Fidelity:
- Situation: a daily close that crosses up from below the cloud to above it -> replaced: the catalogue gives only where the close sits against the cloud now, so "came from below" would be dropped.
- Comparison: a thinner cloud at the cross, as width relative to price, gives a larger rise -> kept: `IchimokuCloudWidthComponent` measures it, in percent of the close.
- Outcome: the coin rises over the next 26 days, more so after a thin cloud -> kept: a 26-bar hold on 1d bars.
- Verdict transfer: no: being above the cloud also covers dips into the cloud from above, and plain long stays above it, so neither verdict would be about crosses from below.
Reason: The cross needs the side of the cloud the close was on before it entered or jumped the cloud. That is computable from the coin's own high, low and close, but no catalogue component keeps it, and no composition can: there is no lag op, and `IchimokuCloudPositionComponent` and `MovingAverageAgeComponent` give only the current side. With such a measure, a regime rule ("crossed up within the last bar") would gate a graded component built from the negated, standardised cloud width plus a constant offset.
