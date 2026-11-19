---
idea: 017-01_presettle-drop-after-uptrend
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 4e6cc97f57e5
---
Fidelity:
- Situation: a coin with a strong 3-day run up, in the 2 hours before a funding settlement (00:00, 08:00, 16:00 UTC) -> adapted: the 72-bar rise is graded, not a "strong" threshold; the clock window needs a time-of-day regime that no component provides.
- Comparison: none (the idea grades by the strength of the rise only) -> kept
- Outcome: the return over the 2 hours before settlement is negative, larger the stronger the rise -> kept: a short sized by the 72-bar rise, held only in those 2 bars.
- Verdict transfer: no: without a time-of-day measure, the short cannot be confined to the pre-settlement hours, so a result would not be about settlement times.
Reason: The idea is active only in the 2 hourly bars before 00:00, 08:00 and 16:00 UTC. The timestamp is in the bars and a regime rule could hold this condition, but no catalogue component gives the hour of day. `WeekdayComponent` gives only the weekday. `FundingRateMeanReversionComponent` reads the hour but is on/off, refused, and fires on the settlement bar itself. No combination of components yields the hour. The graded part, a 72-bar `PriceEvolutionComponent` with `standardise`, `negate` and a `clip` with `max` 0, is available, so only the clock is missing.
