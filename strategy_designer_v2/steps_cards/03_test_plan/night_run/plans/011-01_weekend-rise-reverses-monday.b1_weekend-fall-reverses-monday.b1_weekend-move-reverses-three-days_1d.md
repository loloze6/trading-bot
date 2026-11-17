---
idea: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.b1_weekend-move-reverses-three-days
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: a coin's Saturday-to-Sunday close-to-close return, which must still be readable at the Monday and Tuesday closes -> replaced: at those closes, catalogue components see only returns that end on the current bar, never the weekend bar alone.
- Comparison: the weekend return relative to the coin's usual daily move -> kept: a return divided by the coin's recent typical one-day move (`VolatilityScaledReturnComponent`, or `standardise` of a one-day return).
- Outcome: the Monday-to-Wednesday 3-day return runs opposite to the weekend move, and more so for a larger move -> adapted: a regime on `WeekdayComponent` could hold the forecast while the coming bar is Monday, Tuesday or Wednesday.
- Verdict transfer: no: without a lagged weekend return, the Monday and Tuesday forecasts would mix in the outcome days' own returns, so the result would not be about the weekend move.
Reason: The forecast must equal minus the vol-scaled weekend return on the Sunday, Monday and Tuesday closes. No component returns a past bar's return, and differences of `PriceEvolutionComponent` horizons stop being exact once each is standardised separately. The weekday regimes and the graded sign flip can be built; the lagged return cannot.
