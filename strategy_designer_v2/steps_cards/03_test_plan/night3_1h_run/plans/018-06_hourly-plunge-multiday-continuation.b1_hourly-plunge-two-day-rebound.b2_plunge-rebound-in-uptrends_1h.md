---
idea: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends
brief: 018_daily-condition-caught-on-the-hour
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: afc0f50f6fe7
---
Fidelity:
- Situation: the 24-hour return, read at an hourly close, falls by a large multiple of the 30-day average absolute daily return -> adapted: graded as the fall in multiples of that average (`standardise`, window 720, on the 24-bar return), with a graded dead zone instead of a "large multiple" threshold.
- Comparison: only while the 30-day return is positive, and the larger that rise the larger the rebound -> replaced: no component or composition multiplies the plunge by the 30-day rise; a weighted sum would buy on a month's rise with no plunge.
- Outcome: the price rises over the next 4 days (96 bars) by more than the coin's usual 4-day drift -> kept.
- Verdict transfer: no: without the product, the position cannot grow with the month's rise and cannot be zero when there is no plunge, so neither result would settle the idea.
Reason: The config averages components by weight and has no op that multiplies one component by another. The idea needs the size of the plunge scaled by the size of the positive 30-day rise, and that position must be zero when either one is absent. Gating the 30-day rise as a regime would keep its sign but drop its gradation, and adding it as a weighted component would open positions with no plunge.
