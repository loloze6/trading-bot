---
idea: 011-01_weekend-rise-reverses-monday.g1_volatile-day-selloffs-bounce-next.g1_falls-closing-near-low-bounce
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: a coin falls on a day by a large amount in units of its usual 60-day daily move -> adapted: graded as the one-day return over the 60-day return deviation (VolatilityScaledReturnComponent, period 1, vol_period 60), negated and clipped to falls only.
- Comparison: the closer the close sits to the day's low, as a share of the high-low range, the larger the rise -> replaced: no catalogue component reads where the close sits in the bar's own high-low range, and a weighted sum cannot scale the fall by it.
- Outcome: price rises over the next 1 day (1 bar) -> kept.
- Verdict transfer: no: without the close-in-range scaling, a test of the fall alone would neither confirm nor reject the idea's claim that the bounce grows as the close nears the low.
Reason: The idea needs the close's position in the day's own high-low range, computed from that bar's high, low and close, and it needs that position to scale the size of the fall. No catalogue component reads the bar's high-low range this way (DonchianBreakoutComponent reads closes only; Keltner and ADX smooth over many bars). The config can only take weighted sums of components, so it also cannot multiply the fall by that position.
