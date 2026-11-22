---
idea: 026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue.b1_turbulent-weekend-falls-continue
brief: 026_weekend-moves-reverse-in-the-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 2a96c3272007
---
Fidelity:
- Situation: the coin fell over the weekend, Saturday 00:00 to Monday 00:00 UTC -> kept: a regime rule selects the bar that closes at Monday 00:00 (`WeekdayComponent` 0 and `HourOfDayComponent` 0), with the 48-bar `PriceEvolutionComponent` below 0.
- Comparison: the weekend's hourly volatility against the coin's previous week, grading the bet by that alone and not by the fall's size -> replaced: the catalogue offers only a ratio whose base includes the weekend itself (`VolatilityRatioToAverageComponent`), or one multiplied by the fall's size (`RecentToPriorVolatilityWeightedReturnComponent`).
- Outcome: the coin keeps falling over Monday and Tuesday (short, 48 bars) -> kept: a short bet opened on the Monday 00:00 bar and held 48 bars.
- Verdict transfer: no: grading by a substitute volatility measure, or by one mixed with the fall's size, would not test the idea's claim that the fall grows with this volatility comparison alone.
Reason: The weekend fall, the Monday–Tuesday window and the 48-bar short hold can all be built. No catalogue component, alone or combined, gives the weekend's hourly return volatility divided by the volatility of the week before it, with the fall's size left out.
