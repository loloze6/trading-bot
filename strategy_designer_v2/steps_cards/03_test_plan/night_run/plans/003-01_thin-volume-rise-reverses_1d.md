---
idea: 003-01_thin-volume-rise-reverses
brief: 003_volume-separates-reversal-from-continuation
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: a sharp one-day rise on volume well below average, graded by rise size and thinness -> replaced: the rise is computable, but no graded component measures thinness of volume.
- Comparison: the day's volume against the coin's own 30-day average daily volume -> replaced: no catalogue component computes volume relative to its average.
- Outcome: price gives back part of the rise over the next 5 days (down), more for larger, thinner rises -> kept: a short position sized by the forecast, judged over 5 bars on 1d bars.
- Verdict transfer: no: without the volume measure the test would only check one-day rises reversing, not thin-volume rises.
Reason: The one-day rise is available (`VolatilityScaledReturnComponent`, period 1). The idea also needs a graded measure of the day's volume against its 30-day average, and no component computes one. The only volume readers are `VolumeExpansionHedgeComponent` (on/off, refused) and the `volume_filter` op (a dead zone, not allowed in strategies). A regime gate on `volume_filter` would only give thin or not thin, which drops "the thinner its volume, the larger the giveback".
