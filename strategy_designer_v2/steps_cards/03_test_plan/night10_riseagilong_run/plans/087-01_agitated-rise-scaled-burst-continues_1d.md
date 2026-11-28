---
idea: 087-01_agitated-rise-scaled-burst-continues
brief: 087_rising-agitated-short-push-continues
data-instruments: LTC, ETH, XMR, INJ, GRT, DOGE, XRP, TRX
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: bd33e939b067
---
Fidelity:
- Situation: rising agitated market, 3-day return large against the 30-day daily return std -> kept: the profile is added by code, and "large" is a regime at 2 daily swings, graded inside.
- Comparison: the coin's usual daily swing, the 30-day std of daily returns -> kept: the 3-day return is divided by the 30-day std (times sqrt 3, a constant).
- Outcome: keeps rising over the next 3 days, more for a larger scaled rise -> kept: long held 3 bars, sized by the scaled rise.
- Verdict transfer: yes: the test measures the 3-day rise after large swing-scaled 3-day rises in the profile, and whether larger ones rise more.
Forecast: The indicator is VolatilityScaledReturnComponent with period 3 and vol_period 30. It gives the 3-day return divided by (the 30-day std of daily returns x sqrt 3). The regime detector selects "trending" only when this value is at least 1.1547, which is a 3-day rise of 2 daily swings or more. In "trending", the forecast is the same value standardised over its past 60 values and clipped at 0. It is positive and grows with the swing-scaled rise, from about 14 at the threshold to the cap of 20. On every other bar the forecast is zero, and it is never short. The profile's vetoes, added by code, also keep the forecast at zero outside rising agitated bars.
Config: 087-01_agitated-rise-scaled-burst-continues_1d_config.json
Side: long only (the brief): each component's forecast capped at 0 by step 3's code
Profile: rising agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 3 bars
- Main measure: The cases are the bars with forecast > 0 on each window's non-overlapping 3-bar grid. For each case, take the coin's 3-bar forward return minus the coin's mean 3-bar return over all windows (holding the coin). Measure the mean of this excess, with a t that pools the cases of one day.
- Supporting check: Across the cases, the least-squares slope of the excess 3-bar return on the forecast is above 0.
- Confirm: The mean excess return is above 0 with t >= 2, and the slope is above 0.
- Reject: The mean excess return is below 0 with t <= -2.
- Inconclusive: Any other result is inconclusive, including a t between -2 and 2, or a confirming mean with a slope at or below 0. At least 30 independent case-days are needed, else the test is inconclusive.
