---
idea: 018-05_hourly-plunge-loss-before-close.d2_ten-day-rebound-after-plunge
brief: 018_daily-condition-caught-on-the-hour
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: afc0f50f6fe7
---
Fidelity:
- Situation: the 24-hour return at an hourly close falls by several times the 30-day average absolute daily return -> adapted: "several times" becomes a graded drop multiple, but no component computes that multiple.
- Comparison: the coin's normal drift over the next 10 days -> kept: measured against holding the coin.
- Outcome: the coin rises over the next 10 days (240 bars), more when its 30-day return before the drop was larger -> kept: a 240-bar hold, sized up by the prior 30-day return.
- Verdict transfer: no: without the drop multiple, the test cannot select or grade the idea's situation as the idea states it.
Reason: The situation needs the 24-bar return divided by the mean absolute 24-bar return over the last 720 bars. A config can only take weighted sums of components, so it cannot divide `PriceEvolutionComponent` by `MeanAbsReturnComponent`. `VolatilityScaledReturnComponent` divides by the hourly standard deviation times sqrt(24), which is a different quantity, and `VolScaledBreakAboveHighComponent` uses the right divisor only for breaks above a high.
