---
idea: 003-01_low-volume-up-move-reverts
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
---
Config: 003-01_low-volume-up-move-reverts_config.json
Confirm: The horizon is 1 bar. Take the bars where the config is short, that is, up days with volume below the 20-day average. On those bars, BTC's next-day return must average below its unconditional mean next-day return (t ≤ -2). The short's next-day gain, before costs, must also grow with position size: the top size tercile earns more per bar than the bottom tercile.
Reject: Over the same 1-bar horizon, the mean next-day return after short bars is at or above BTC's unconditional mean next-day return. Rejection also holds if the next-day gain does not grow with position size, or shrinks with it.
Inconclusive: The mean next-day return after short bars is below the unconditional mean, but not significantly (-2 < t < 0). Also inconclusive: it is significant, but the size terciles show no ordering. Also inconclusive: fewer than 30 bars carry a position large enough to trade (|forecast| ≥ 2).
Deviation: "Unusually low volume" becomes "the day's volume is below its 20-day average (including today)", which is a milder condition than "unusual". "Followed by falling back" becomes a short held for one day only, sized by that day's rise. Any give-back that comes after the first day is not captured. The brief's contrast with high-volume moves is not part of this test.
