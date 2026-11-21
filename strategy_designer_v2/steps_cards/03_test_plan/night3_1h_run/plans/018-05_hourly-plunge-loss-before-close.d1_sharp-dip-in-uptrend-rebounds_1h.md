---
idea: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds
brief: 018_daily-condition-caught-on-the-hour
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: afc0f50f6fe7
---
Fidelity:
- Situation: 24-hour return, read at an hourly close, falls by several times the 30-day average absolute daily return, while the 30-day return is positive -> replaced: no component divides a 24-bar return by the mean absolute 24-bar return over 720 bars.
- Comparison: the coin's normal drift over the next 3 days -> kept: measured against holding the coin, on the recorded closes.
- Outcome: the coin rises over the next 3 days (72 bars), more so the larger its 30-day return in usual 30-day moves -> kept: VolatilityScaledReturnComponent (period 720) grades it, held 72 bars.
- Verdict transfer: no: the drop's size against a std of hourly returns is a different quantity from the idea's multiple of the 30-day mean absolute daily return.
Reason: The idea's trigger is a ratio of two quantities: the 24-bar return divided by the mean absolute 24-bar return over 720 bars. PriceEvolutionComponent (period 24) gives the numerator and MeanAbsReturnComponent (24, 720) gives the denominator, but the config only adds weighted components, and score_product divides only by constants, so no composition yields their ratio. VolatilityScaledReturnComponent scales by a standard deviation of one-bar returns, which is a replacement. All the data is in the coin's own closes, and a regime rule (ratio at or below about -3, plus a 720-bar return above 0) could hold the condition if the ratio were computed.
