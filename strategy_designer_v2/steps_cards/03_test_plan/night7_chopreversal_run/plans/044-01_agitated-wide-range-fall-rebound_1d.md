---
idea: 044-01_agitated-wide-range-fall-rebound
brief: 044_agitated-wide-range-fall-rebound
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: e8f4c1171351
---
Fidelity:
- Situation: in an agitated market, a day the coin closes lower -> kept: the component is 0 unless the day closed down; the code adds the agitated profile.
- Comparison: the fall against the 30-day std of daily returns, times the range against the 30-day mean range -> kept: `ScaledFallRangeMultipleComponent` computes this product exactly (period 1, window 30, "std").
- Outcome: the next day's rise grows with that product -> adapted: "after the fall" becomes "while the fall bar is the latest bar", held for 1 day and sized by the product.
- Verdict transfer: yes: the forecast is the idea's product, active only on falling days in the agitated profile and held over the next day, so its next-day gains test the claim directly.
Forecast: The forecast uses one component, `ScaledFallRangeMultipleComponent` with period 1, lag 0, window 30 and scale "std". On each day it is the day's fall divided by the 30-day standard deviation of daily returns, times the day's high-low range divided by its 30-day mean range. It is standardised against its own 60 past values, so a typical reading is +10, capped at 20. It is exactly 0 on up and flat days. It is positive on down days and grows continuously with the depth of the fall and the width of the day. It is never negative, so the book is long only. The code keeps it flat outside the agitated profile. It is held for 1 day.
Config: 044-01_agitated-wide-range-fall-rebound_1d_config.json
Profile: agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bar
- Main measure: Use the bars with forecast > 0, in every coin and window, one case per bar. The dependent value is the next-day return close[t+1]/close[t] - 1 minus the coin's mean daily return over all its windows. Regress it on the forecast and read the slope, with its t clustered by day (cases on the same day count as one).
- Supporting check: The forecast-weighted mean of that next-day excess return over the forecast > 0 bars is above 0.
- Confirm: The slope is positive with t ≥ 2, and the forecast-weighted mean excess return is above 0.
- Reject: The slope is negative with t ≤ -2.
- Inconclusive: Any slope t between -2 and 2 is inconclusive. A positive slope with t ≥ 2 but a weighted mean ≤ 0 is also inconclusive. The test needs at least 100 cases with forecast > 0, falling on at least 60 distinct days; fewer is inconclusive.
