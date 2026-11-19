---
idea: 017-04_postsettle-decline-after-downtrend
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 4e6cc97f57e5
---
Fidelity:
- Situation: a strong 3-day run down, in the 2 hours after a funding settlement (00:00, 08:00, 16:00 UTC) -> replaced: the 72-bar fall can be kept, but no component gives the hour of day, so the settlement clock is lost.
- Comparison: the stronger the 3-day fall, the larger the post-settlement decline -> kept: a graded short that grows with the negated 72-bar return.
- Outcome: the return over the 2 hours after each settlement is negative -> kept: a 2-bar horizon on 1h bars, short in that window.
- Verdict transfer: no: without the settlement clock, a test would short every hour after a fall and could not show anything specific to the post-settlement hours.
Reason: The 3-day fall is in the catalogue (`PriceEvolutionComponent`, period 72), but no component reads the hour of day from `timestamp`, so a regime rule cannot pick the two bars after each settlement. `WeekdayComponent` gives only the weekday, and `FundingRateMeanReversionComponent` gives an on/off funding sign that misses the 00:00–01:00 bar, so combining components does not cover it.
