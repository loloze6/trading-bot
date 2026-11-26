---
idea: 066-01_falling-agitated-sixty-day-scaled-fall-rebound
brief: 066_longer-swing-yardstick-agitated-fall-rebound
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 4510fe2da56d
---
Fidelity:
- Situation: a one-day fall, large against the 60-day swing, in a falling agitated market -> adapted: the fall in 60-day standard deviations is graded, exactly 0 on up days, with the strongest graded dead zone; the profile is added by code.
- Comparison: the fall measured against the 60-day standard deviation of daily returns -> kept
- Outcome: a rise the next day, larger the larger the scaled fall -> kept
- Verdict transfer: yes: the forecast is the idea's scaled fall, only on falling days inside the profile, and it is judged on the next day's return.
Forecast: The forecast starts from the day's return divided by the standard deviation of the last 60 daily returns (`VolatilityScaledReturnComponent`, `period` 1, `vol_period` 60). This is put on the forecast scale with `standardise` (window 61, min_periods 20), then negated, so a fall reads positive. It is clipped at 0, so it is long only and exactly 0 on up or flat days. A `signed_power` with exponent 3 and pivot 20 then damps small falls towards 0: a fall of about half a usual move gives roughly 0.6, one usual move about 5, and about 1.6 usual moves or more reaches the cap of 20. The forecast is never negative, and it grows with the depth of the fall against the 60-day swing. The book is flat outside the falling agitated profile, which step 3's code adds.
Config: 066-01_falling-agitated-sixty-day-scaled-fall-rebound_1d_config.json
Profile: falling agitated (the idea): no position outside it, by step 3's code (common/market_profile.md)
Criterion:
- Horizon: 1 bars
- Main measure: On bars with forecast > 0, the next day's return minus the coin's mean daily return over all its windows. Its mean is weighted by the forecast, and its t is computed with cases of the same day summed together.
- Supporting check: Over the same bars, the least-squares slope of that excess next-day return on the forecast is above 0.
- Confirm: The forecast-weighted mean excess return is above 0 with t >= 2, and the slope is positive.
- Reject: The forecast-weighted mean excess return has t <= -2.
- Inconclusive: A t between -2 and 2, or t >= 2 with a slope at or below 0. At least 100 cases on at least 50 distinct days are needed, otherwise the result is inconclusive.
