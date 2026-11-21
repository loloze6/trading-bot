---
idea: 018-02_hourly-breakout-multiday-continuation
brief: 018_daily-condition-caught-on-the-hour
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: hourly close first rises above the highest price of the prior 20 days -> adapted: "first rises" made "while above", graded by DistanceFromHighComponent (period 480, source "high", exclude_current 1, clip min 0).
- Comparison: the break measured in multiples of the 30-day average absolute daily return -> replaced: no component divides the break by that scale, so it would be the percent break standardised against its own past values.
- Outcome: price keeps rising over the next 5 days (120 bars), more than the coin's usual 5-day return -> kept: a 120-bar hold, judged against holding the coin.
- Verdict transfer: no: a test on the percent break would not judge the idea's claim that the rise grows with the break in units of the coin's usual daily move.
Reason: The forecast must size the break above the prior 20-day high by the coin's 30-day average absolute daily return. That scale is in the coin's own bars, but no component computes it. A config cannot divide one component by another: weights only add. `standardise` scales by the component's own past values, and `vol_normalize` divides by the 24-bar standard deviation of price levels, which is a different quantity.
